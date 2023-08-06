import logging
import os
import shutil
import threading
from typing import Optional

import zmq

from openmodule.alert import AlertHandler
from openmodule.config import validate_config_module
from openmodule.database.database import Database
from openmodule.dispatcher import SubscribingMessageDispatcher
from openmodule.health import HealthHandlerType, Healthz, HealthPingMessage
from openmodule.logging import init_logging
from openmodule.messaging import get_pub_socket, get_sub_socket, receive_message_from_socket
from openmodule.models.base import ZMQMessage
from openmodule.sentry import init_sentry
from openmodule.threading import get_thread_wrapper


class OpenModuleCore(threading.Thread):
    database = None

    def __init__(self, context, config):
        super().__init__(target=get_thread_wrapper(self._run))
        self.context = context
        self.config = config

        self.pub_lock = threading.Lock()
        self.sub_lock = threading.Lock()

        self.pub_socket = get_pub_socket(self.context, self.config, linger=1000)
        self.sub_socket = get_sub_socket(self.context, self.config)
        self.messages = SubscribingMessageDispatcher(self._subscribe)

        self.log = logging.getLogger(self.__class__.__name__)
        self.health = Healthz(self)
        self.alerts = AlertHandler(self)
        self.messages.register_handler(b"healthz", HealthPingMessage, self.health.process_message,
                                       filter={"type": "ping"})

    def _subscribe(self, topic: bytes):
        with self.sub_lock:
            self.sub_socket.subscribe(topic)

    def init_database(self):
        if self.config.TESTING:
            self.database = Database(self.config.DATABASE_FOLDER, self.config.NAME, alembic_path="../src/database")
        else:
            self.database = Database(self.config.DATABASE_FOLDER, self.config.NAME)

    def _run(self):
        try:
            while True:
                topic, message = receive_message_from_socket(self.sub_socket)
                self.messages.dispatch(topic, message)
        except zmq.ContextTerminated:
            self.log.debug("context terminated, core shutting down")
        finally:
            self.pub_socket.close()
            self.sub_socket.close()

    def publish(self, message: ZMQMessage, topic: bytes):
        with self.pub_lock:
            message.publish_on_topic(self.pub_socket, topic)


_core_thread: Optional[OpenModuleCore] = None


def init_dsgvo_config():
    if os.path.exists("/data") and os.path.exists("/data/config.yml"):
        shutil.copyfile("/data/config.yml", "/data/tmp.yml")
        shutil.move("/data/tmp.yml", "/data/dsgvo-config.yml")
    if os.path.exists("/data") and os.path.exists("dsgvo-default.yml"):
        shutil.copyfile("dsgvo-default.yml", "/data/tmp.yml")
        shutil.move("/data/tmp.yml", "/data/dsgvo-default.yml")


def print_environment(core: OpenModuleCore):
    core.log.info(f"Service: {core.config.NAME} (version:{core.config.VERSION})")
    if core.config.DEBUG:
        core.log.warning(
            "\n"
            "       DEBUG MODE is active.\n"
            "       Deactivate by setting environment variable DEBUG=False.\n"
            "       Debug is disabled per default when a version string is set or ran inside docker.\n"
        )


def init_openmodule(config, sentry=True, logging=True, dsgvo=True,
                    health_handler: Optional[HealthHandlerType] = None,
                    context=None, database=False) -> OpenModuleCore:
    context = context or zmq.Context()
    validate_config_module(config)

    global _core_thread
    assert not _core_thread, "openmodule core already running"
    _core_thread = OpenModuleCore(context, config)
    _core_thread.start()

    if logging:
        init_logging(_core_thread)
    print_environment(_core_thread)

    if sentry:
        init_sentry(_core_thread)

    if dsgvo:
        init_dsgvo_config()

    if health_handler:
        _core_thread.health.health_handler = health_handler

    if database:
        _core_thread.init_database()

    return _core_thread


def core() -> OpenModuleCore:
    return _core_thread


def shutdown_openmodule():
    global _core_thread
    assert _core_thread, "core thread is not running, did you call init_openmodule(...)?"

    current_cure = _core_thread
    _core_thread = None

    shutdown_done = threading.Event()

    def last_will():
        if not shutdown_done.wait(timeout=1):
            os._exit(99)

    if not (current_cure.config.TESTING or current_cure.config.DEBUG):
        last_will_thread = threading.Thread(target=last_will)
        last_will_thread.setDaemon(True)
        last_will_thread.start()

    if current_cure.database:
        current_cure.database.shutdown()

    current_cure.context.term()
    current_cure.join()
    shutdown_done.set()
