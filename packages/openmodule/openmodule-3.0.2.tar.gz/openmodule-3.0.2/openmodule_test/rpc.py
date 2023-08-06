import random
import string
import threading
import time
from contextlib import suppress
from functools import partial

from pydantic.main import BaseModel

from openmodule_test.zeromq import ZMQTestMixin


class _EmptyModel(BaseModel):
    pass


class RPCServerTestMixin(ZMQTestMixin):
    def wait_for_rpc_server(self, server):
        pending_channels = {}
        lock = threading.Lock()

        def handler(_, __, channel):
            with lock:
                with suppress(KeyError):
                    del pending_channels[channel]

        """
        waits until a rpc server is responding on all channels
        """
        channels = set(x[0] for x in server.handlers)
        random_type = "_test" + "".join(random.choices(string.ascii_letters, k=10))
        for channel in channels:
            server.register_handler(channel, random_type, _EmptyModel, _EmptyModel, partial(handler, channel=channel))
            pending_channels[channel] = None

        for x in range(self.zmq_client.startup_check_iterations):
            with lock:
                channels = list(pending_channels.keys())
            if channels:
                for channel in channels:
                    self.rpc(channel, random_type, {}, receive_response=False)
                time.sleep(self.zmq_client.startup_check_delay)
            else:
                break

        assert not pending_channels, "error during startup and connect"
