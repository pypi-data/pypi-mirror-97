from unittest import TestCase

from openmodule.alert import AlertHandleType
from openmodule.core import core, init_openmodule, shutdown_openmodule
from openmodule_test.alert import AlertTestMixin
from openmodule_test.core import OpenModuleCoreTestMixin
from openmodule_test.health import HealthTestMixin


class OpenModuleCoreTest(AlertTestMixin, HealthTestMixin, TestCase):
    topics = ["healthz", "sentry", "alert"]
    protocol = "tcp://"

    def test_core_init_and_shutdown(self):
        self.assertIsNone(core())

        init_openmodule(self.zmq_config(NAME="x123x"))
        try:
            self.assertIsNotNone(core())
            self.wait_for_health(name="x123x")
        finally:
            shutdown_openmodule()

    def test_core_sentry_error_logging(self):
        # sentry is not active during unittests / debug
        init_openmodule(self.zmq_config(DEBUG=False, TESTING=False))
        self.wait_for_health()

        try:
            core().log.error("some-error-message")
            sentry_message = self.zmq_client.wait_for_message_on_topic("sentry")
            self.assertIn("some-error-message", str(sentry_message))
        finally:
            shutdown_openmodule()

    def test_core_alerts(self):
        init_openmodule(self.zmq_config())
        self.wait_for_health()

        try:
            core().alerts.send("some-source", "some_type", AlertHandleType.state_change)
            self.assertAlert(alert_type="some_type")
        finally:
            shutdown_openmodule()
