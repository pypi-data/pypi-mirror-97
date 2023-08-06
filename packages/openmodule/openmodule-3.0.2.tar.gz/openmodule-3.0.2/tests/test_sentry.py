import logging
from unittest import TestCase

import sentry_sdk

from openmodule.core import OpenModuleCore
from openmodule.sentry import init_sentry
from openmodule_test.zeromq import ZMQTestMixin


class SentryTestCase(ZMQTestMixin, TestCase):
    topics = ["sentry"]

    def setUp(self):
        super().setUp()
        logging.basicConfig(level=logging.INFO)
        self.core = OpenModuleCore(self.zmq_context(), self.zmq_config(DEBUG=False, TESTING=False))
        self.core.start()

    def tearDown(self):
        super().tearDown()
        sentry_sdk.init(dsn=None)  # clears the sentry configuration
        self.core.join()

    def test_sentry_init(self):
        sentry_sdk.capture_message("test message")
        with self.assertRaises(TimeoutError):
            self.zmq_client.wait_for_message_on_topic(b"sentry")

        init_sentry(self.core)
        sentry_sdk.capture_message("test message")

        sentry_message = self.zmq_client.wait_for_message_on_topic(b"sentry")
        self.assertIn("event", sentry_message)

    def test_sentry_logging_integration(self):
        init_sentry(self.core)
        logging.error("Some error, please help!")

        sentry_message = self.zmq_client.wait_for_message_on_topic(b"sentry")
        self.assertIn("event", sentry_message)

    def test_sentry_does_not_run_in_debug(self):
        self.core.config.DEBUG = True
        init_sentry(self.core)
        logging.error("Some error, please help!")
        with self.assertRaises(TimeoutError):
            self.zmq_client.wait_for_message_on_topic(b"sentry")

    def test_extras_are_set(self):
        self.core.config.RESOURCE = "some-test-resource123"
        init_sentry(self.core, extras={"some-more-extras" + "123": True})

        logging.error("Some error, please help!", extra={"even-more-extras" + "123": "yes!"})
        sentry_message = self.zmq_client.wait_for_message_on_topic(b"sentry")

        # we dont know exactly where sentry puts its stuff, so simply check string contains
        event = str(sentry_message["event"])
        self.assertIn("some-test-resource123", event)
        self.assertIn("even-more-extras123", event)
        self.assertIn("some-more-extras123", event)

        # just to be sure, that sentry doesnt put the code here in its event, this would also cause all tests to succeed
        self.assertNotIn("wait_for_message_on_topic", event)
