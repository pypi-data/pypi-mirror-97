from functools import partial
from unittest import TestCase
from uuid import uuid4

from pydantic.types import conint

from openmodule.models.base import OpenModuleModel
from openmodule.rpc import server
from openmodule.rpc.common import channel_to_response_topic, channel_to_request_topic
from openmodule.rpc.server import RPCServer, RPCRequest
from openmodule_test.rpc import RPCServerTestMixin
from openmodule_test.zeromq import ZMQTestMixin


def _fake_request(gate=..., direction=...):
    gateway = {}
    if gate != Ellipsis:
        gateway["gate"] = gate
    if direction != Ellipsis:
        gateway["direction"] = direction

    request = {}
    if gateway:
        request["gateway"] = gateway

    return request


class RPCCommonTestCase(TestCase):
    def test_topics(self):
        self.assertEqual(b"rpc-rep-test", channel_to_response_topic(b"test"))
        self.assertEqual(b"rpc-req-test", channel_to_request_topic(b"test"))

    def test_gateway_filter(self):
        filter_full = server.gateway_filter("gate1", "in")
        self.assertTrue(filter_full(_fake_request(gate="gate1", direction="in"), None, None))
        self.assertFalse(filter_full(_fake_request(gate="gate1", direction="out"), None, None))
        self.assertFalse(filter_full(_fake_request(gate="gate2", direction="in"), None, None))
        self.assertFalse(filter_full(_fake_request(gate="gate2", direction="out"), None, None))
        self.assertFalse(filter_full(_fake_request(gate="gate2"), None, None))
        self.assertFalse(filter_full(_fake_request(gate="gate2"), None, None))
        self.assertFalse(filter_full(_fake_request(direction="in"), None, None))
        self.assertFalse(filter_full(_fake_request(direction="out"), None, None))
        self.assertFalse(filter_full(_fake_request(), None, None))

        filter_direction = server.gateway_filter(direction="in")
        self.assertTrue(filter_direction(_fake_request(gate="gate1", direction="in"), None, None))
        self.assertFalse(filter_direction(_fake_request(gate="gate1", direction="out"), None, None))
        self.assertTrue(filter_direction(_fake_request(gate="gate2", direction="in"), None, None))
        self.assertFalse(filter_direction(_fake_request(gate="gate2", direction="out"), None, None))
        self.assertFalse(filter_direction(_fake_request(gate="gate2"), None, None))
        self.assertFalse(filter_direction(_fake_request(gate="gate2"), None, None))
        self.assertTrue(filter_direction(_fake_request(direction="in"), None, None))
        self.assertFalse(filter_direction(_fake_request(direction="out"), None, None))
        self.assertFalse(filter_direction(_fake_request(), None, None))

        filter_gate = server.gateway_filter(gate="gate1")
        self.assertTrue(filter_gate(_fake_request(gate="gate1", direction="in"), None, None))
        self.assertTrue(filter_gate(_fake_request(gate="gate1", direction="out"), None, None))
        self.assertFalse(filter_gate(_fake_request(gate="gate2", direction="in"), None, None))
        self.assertFalse(filter_gate(_fake_request(gate="gate2", direction="out"), None, None))
        self.assertFalse(filter_gate(_fake_request(gate="gate2"), None, None))
        self.assertFalse(filter_gate(_fake_request(gate="gate2"), None, None))
        self.assertFalse(filter_gate(_fake_request(direction="in"), None, None))
        self.assertFalse(filter_gate(_fake_request(direction="out"), None, None))
        self.assertFalse(filter_gate(_fake_request(), None, None))


class TestRPCRequest(OpenModuleModel):
    __test__ = False
    pass


class TestRPCResponse(OpenModuleModel):
    __test__ = False
    pass


class TestRPCResponse2(OpenModuleModel):
    __test__ = False
    some_payload: str


class RPCServerTestCase(RPCServerTestMixin, ZMQTestMixin, TestCase):
    rpc_channels = ["channel", "channel2"]

    server: RPCServer

    def setUp(self):
        super().setUp()
        self.called_types = {}
        self.server = RPCServer(self.zmq_context(), self.zmq_config())
        self.server_thread = self.server.run_as_thread()

    def tearDown(self):
        self.server.shutdown()
        self.server_thread.join()
        super().tearDown()

    def set_called(self, request, message: RPCRequest, value=True):
        self.called_types[message.type] = value

    def set_called_value(self, value):
        return partial(self.set_called, value=value)

    def test_invalid_rpc_request(self):
        self.server.register_handler("channel", "test-type", TestRPCRequest, TestRPCResponse, self.set_called)
        self.wait_for_rpc_server(self.server)

        rpc_request = RPCRequest(name="testclient", type="test-type", rpc_id=uuid4(), request={})
        broken_data = rpc_request.dict()
        del broken_data["rpc_id"]
        self.zmq_client.send(f"rpc-req-channel".encode("ascii"), broken_data)

        _, error_response = self.zmq_client.wait_for_message(
            filter=lambda topic, message: topic == b"rpc-rep-channel" and message.get("type") == "unknown"
        )
        self.assertIsNone(error_response.get("rpc_id"))

    def test_no_filter(self):
        self.server.register_handler("channel", "test-type", TestRPCRequest, TestRPCResponse, self.set_called)
        self.wait_for_rpc_server(self.server)

        self.rpc("channel", "test-type", {})
        self.assertTrue(self.called_types.get("test-type"))

    def test_exception_in_filter_function(self):
        def bad_filter(*args, **kwargs) -> bool:
            raise Exception("Error123")

        self.server.register_handler("channel", "test-type", TestRPCRequest, TestRPCResponse, self.set_called)
        self.wait_for_rpc_server(self.server)
        self.server.add_filter(bad_filter)

        response = self.rpc("channel", "test-type", {})
        self.assertRPCFailure(response, "filter_error")
        self.assertEqual("Error123", response["response"]["exception"])

    def test_filter(self):
        def allow_only_type_test(message: RPCRequest, **kwargs) -> bool:
            return message.type == "test-type"

        self.server.register_handler("channel", "test-type", TestRPCRequest, TestRPCResponse, self.set_called)
        self.server.register_handler("channel", "test-type2", TestRPCRequest, TestRPCResponse, self.set_called)
        self.wait_for_rpc_server(self.server)

        response = self.rpc("channel", "test-type", {})
        self.assertRPCSuccess(response)
        self.assertTrue(self.called_types.get("test-type"))

        response = self.rpc("channel", "test-type2", {})
        self.assertTrue(self.called_types.get("test-type2"))
        self.assertRPCSuccess(response)

        # clear stats, and add the filter
        del self.called_types["test-type"]
        del self.called_types["test-type2"]
        self.server.add_filter(allow_only_type_test)

        # should still work as before
        response = self.rpc("channel", "test-type", {})
        self.assertRPCSuccess(response)
        self.assertTrue(self.called_types.get("test-type"))

        # times out
        with self.assertRaises(TimeoutError):
            self.rpc("channel", "test-type2", {})
        self.assertNotIn("test-type2", self.called_types)

    def test_filter_channel_type(self):
        def f(*args, **kwargs):
            return False

        def check_ok():
            response = self.rpc("channel", "test-type", {})
            self.assertRPCSuccess(response)
            self.assertTrue(self.called_types.get("test-type"))
            self.called_types.clear()

        def check_not_called():
            with self.assertRaises(TimeoutError):
                response = self.rpc("channel", "test-type", {})
            self.assertEqual(None, self.called_types.get("test-type"))
            self.called_types.clear()

        self.server.register_handler("channel", "test-type", TestRPCRequest, TestRPCResponse, self.set_called)
        self.wait_for_rpc_server(self.server)

        self.server.add_filter(f, "abc")
        check_ok()

        self.server.add_filter(f, "channel", "abc")
        check_ok()

        self.server.add_filter(f, "channel")
        check_not_called()

        self.server.filters.clear()
        self.server.add_filter(f, "channel", "test-type")
        check_not_called()

    def test_can_only_register_once(self):
        self.server.register_handler("channel", "test-type", TestRPCRequest, TestRPCResponse, self.set_called)
        self.wait_for_rpc_server(self.server)
        with self.assertRaises(ValueError) as e:
            self.server.register_handler("channel", "test-type", TestRPCRequest, TestRPCResponse, self.set_called)
        self.assertIn("already registered", str(e.exception))

    def test_exception_in_handler(self):
        def handler(*_, **__):
            raise Exception("Error123")

        self.server.register_handler("channel", "test-type", TestRPCRequest, TestRPCResponse, handler)
        self.wait_for_rpc_server(self.server)

        response = self.rpc("channel", "test-type", {})
        self.assertRPCFailure(response, "handler_error")
        self.assertEqual("Error123", response["response"]["exception"])

    def test_handler_returns_none(self):
        def handler(*_, **__):
            return None

        self.server.register_handler("channel", "test-type", TestRPCRequest, TestRPCResponse, handler)
        self.wait_for_rpc_server(self.server)

        response = self.rpc("channel", "test-type", {})
        self.assertRPCSuccess(response)

    def test_handler_returns_dict(self):
        def handler(*_, **__):
            return {}

        self.server.register_handler("channel", "test-type", TestRPCRequest, TestRPCResponse, handler)
        self.wait_for_rpc_server(self.server)

        response = self.rpc("channel", "test-type", {})
        self.assertRPCSuccess(response)

    def test_handler_returns_model(self):
        def handler(*_, **__):
            return TestRPCResponse()

        self.server.register_handler("channel", "test-type", TestRPCRequest, TestRPCResponse, handler)
        self.wait_for_rpc_server(self.server)

        response = self.rpc("channel", "test-type", {})
        self.assertRPCSuccess(response)

    def test_handler_returns_wrong_dict(self):
        def bad_handler(*_, **__):
            return {}

        def good_handler(*_, **__):
            return {"some_payload": "test"}

        self.server.register_handler("channel", "test-type1", TestRPCRequest, TestRPCResponse2, bad_handler)
        self.server.register_handler("channel", "test-type2", TestRPCRequest, TestRPCResponse2, good_handler)
        self.wait_for_rpc_server(self.server)

        response = self.rpc("channel", "test-type1", {})
        self.assertRPCFailure(response, "handler_error")

        response = self.rpc("channel", "test-type2", {})
        self.assertRPCSuccess(response)

    def test_handler_returns_wrong_response_type(self):
        def bad_handler(*_, **__):
            return TestRPCResponse()

        def good_handler(*_, **__):
            return TestRPCResponse2(some_payload="test")

        self.server.register_handler("channel", "test-type1", TestRPCRequest, TestRPCResponse2, bad_handler)
        self.server.register_handler("channel", "test-type2", TestRPCRequest, TestRPCResponse2, good_handler)
        self.wait_for_rpc_server(self.server)

        response = self.rpc("channel", "test-type1", {})
        self.assertRPCFailure(response, "handler_error")

        response = self.rpc("channel", "test-type2", {})
        self.assertRPCSuccess(response)

    def test_handler_returns_additional_data(self):
        """
        additional data is dropped, just as the serializer dictates
        """

        def too_much_handler(*_, **__):
            return {"some_payload": "test", "nobody_wants_you": ":("}

        self.server.register_handler("channel", "test-type1", TestRPCRequest, TestRPCResponse2, too_much_handler)
        self.wait_for_rpc_server(self.server)

        response = self.rpc("channel", "test-type1", {})
        self.assertRPCSuccess(response)
        self.assertDictEqual(response["response"], {"some_payload": "test", "status": "ok"})

    def test_serializer_error(self):
        class SomeValidator(OpenModuleModel):
            max_int: conint(gt=0, lt=10)

        def handler(*_, **__):
            pass

        self.server.register_handler("channel", "test-type", SomeValidator, TestRPCResponse, handler)
        self.wait_for_rpc_server(self.server)

        self.assertRPCSuccess(self.rpc("channel", "test-type", {"max_int": 1}))
        self.assertRPCSuccess(self.rpc("channel", "test-type", {"max_int": 5}))
        self.assertRPCFailure(self.rpc("channel", "test-type", {"max_int": 0}), "validation_error")
        self.assertRPCFailure(self.rpc("channel", "test-type", {"max_int": 10}), "validation_error")

    def test_no_handler_found(self):
        def handler(*_, **__):
            return TestRPCResponse()

        self.server.register_handler("channel", "test-type", TestRPCRequest, TestRPCResponse, handler)
        self.wait_for_rpc_server(self.server)

        response = self.rpc("channel", "test-type", {})  # correct type and channel
        self.assertRPCSuccess(response)

        with self.assertRaises(TimeoutError):  # wrong type
            self.rpc("channel", "test-type-doesnotexist", {})

        with self.assertRaises(TimeoutError):  # wrong channel (correct prefix chosen on purpose)
            self.rpc("channel2", "test-type", {})

        with self.assertRaises(TimeoutError):  # wrong everything
            self.rpc("channel2", "test-type-doesnotexist", {})
