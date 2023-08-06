from typing import Dict

from openmodule.core import init_openmodule, shutdown_openmodule, OpenModuleCore
from openmodule_test.health import HealthTestMixin


class OpenModuleCoreTestMixin(HealthTestMixin):
    """
    Mixin which creates a core, zmq, and health mixin
    config-priority: config_kwargs -> zmq_config -> base_config, afterwards always use core.config
    """

    init_kwargs: Dict = {}
    config_kwargs: Dict = {}
    base_config = None

    core: OpenModuleCore

    def get_config_kwargs(self):
        return self.config_kwargs

    def get_init_kwargs(self):
        return self.init_kwargs

    def _fake_config(self):
        conf = self.zmq_config(**self.get_config_kwargs())
        if self.base_config:
            for key in vars(self.base_config):
                if not key.startswith("_") and key not in vars(conf):
                    setattr(conf, key, getattr(self.base_config, key))
        return conf

    def setUp(self):
        super().setUp()
        self.init_kwargs.setdefault("sentry", False)
        self.init_kwargs.setdefault("dsgvo", False)
        self.core = init_openmodule(
            config=self._fake_config(),
            context=self.zmq_context(),
            **self.get_init_kwargs()
        )
        self.zmq_client.subscribe(b"healthz")
        self.wait_for_health(self.core.config.NAME)

    def tearDown(self):
        try:
            super().tearDown()
        finally:
            shutdown_openmodule()
