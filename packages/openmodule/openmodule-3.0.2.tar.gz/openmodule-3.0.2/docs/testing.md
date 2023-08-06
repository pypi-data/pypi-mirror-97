# Openmodule Testing
We provide multiple Mixins and Util classes for test purposes in openmodule-test.

## Mixin
### OpenModuleCoreTestMixin 
Mixin for automatic core generation including health test utils and zmq utils 
The core can be configured via setting base_config or config_kwargs. There is also some "faked" config for connecting to the message queue.   
The config priority is: config_kwargs -> "fake" config -> base_config
```python
class Test(OpenModuleCoreTestMixin):
    base_config = config
    config_kwargs = dict(bla="bla")
    topics = [b"healthz"]
```

### RPCServerTestMixin
Mixin providing rpc and messaging functionality 
```python
class Test(OpenModuleCoreTestMixin, RPCServerTestMixin):
    base_config = config
    config_kwargs = dict(bla="bla")
    rpc_channels = ["backend"]
    
    def setUp(self):
        super().setUp()
        self.server = RPCServer(config=self.zmq_config(), context=self.zmq_context())
        self.server.run_as_thread()
        self.wait_for_rpc_server(self.server)
    
    def tearDown(self):
        self.server.shutdown()
        super().tearDown()
```

### SQLiteTestMixin 
Mixin that takes a database or creates one and cleans it up after each test.
```python
# base database that gets reset
class Test(SQLiteTestMixin):
    pass

# use other database
class Test(SQLiteTestMixin, OpenModuleCoreTestMixin):
    create_database = False
    config_kwargs = dict(database=True)
    
    def setUp(self):
        super().setUp()
        self.database = self.core.database
```

### AlertTestMixin 
Mixin to for dealing with alerts
```python
class AlertTestCase(AlertTestMixin):
    topics = ["alert"]
```
    
### BackendTestMixin 
Mixin with core creation, backend creation and backend util functions
```python
class Test(BackendTestMixin):
    backend_class = Backend
```

### HealthTestMixin 
Mixin for receiving and checking health status, included in CoreMixin
```python
class Test(HealthTestMixin):
    topics = ["healthz"]
```


## Utils
### ApiMocker 
Base mocker class for simulating http requests
```python
class Mocker(ApiMocker):
    host = config.SERVER_URL
    def mock(self):
        def cb(request, context):
            return {}
        self.mocker.get(self.server_url("abc"), json=cb)

class Test(TestCase):
    @requests_mock.Mocker(real_http=False)
    def test_check_in_out(self, m):
        res = requests.get(config.host+"abc")
```

### MockEvent 
Check if function was called, i.e. in a listener -> do not forget resetting
```python
event = MockEvent()
some_event_listener.append(event)
do_trigger_event()
event.wait_for_call()
event.reset_call_count()
```

### VehicleBuilder 
Util class for generating vehicles
```python
vehicle = VehicleBuilder().lpr("A", "G ARIVO1")
```

### PresenceSimulator 
Util class for simulating presence messages
```python
presence_sim = PresenceSimulator("gate_in", Direction.IN, lambda x: self.zmq_client.send(b"presence", x))
presence_listener = PresenceListener(core.messages)
on_enter = MockEvent()
presence_listener.on_enter.append(on_enter)
presence_sim.enter(self.presence_sim.vehicle().lpr("A", "G ARIVO1"))
on_enter.wait_for_call()
```