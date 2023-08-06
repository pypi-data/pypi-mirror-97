from unittest import TestCase

from openmodule.alert import AlertHandler, AlertHandleType
from openmodule.core import OpenModuleCore
from openmodule_test.alert import AlertTestMixin


class AlertTestCase(AlertTestMixin, TestCase):
    topics = ["alert"]

    def setUp(self):
        super().setUp()
        self.core = OpenModuleCore(self.zmq_context(), self.zmq_config())
        self.core.start()

    def tearDown(self):
        super().tearDown()
        self.core.join()

    def test_value_is_required_for_state(self):
        alert_handler = AlertHandler(self.core)
        alert_handler.send("pin1", "some_alert", AlertHandleType.state, value=10)
        self.assertAlert()

        with self.assertRaises(ValueError) as e:
            alert_handler.send("pin1", "some_alert", AlertHandleType.state)
        self.assertIn("value must not be none", str(e.exception).lower())

        self.assertNoAlert()

    def test_value_none_is_not_sent(self):
        alert_handler = AlertHandler(self.core)
        alert_handler.send("pin1", "some_alert", AlertHandleType.state_change)
        alert = self.assertAlert(alert_type="some_alert")

        self.assertNotIn("value", alert)
