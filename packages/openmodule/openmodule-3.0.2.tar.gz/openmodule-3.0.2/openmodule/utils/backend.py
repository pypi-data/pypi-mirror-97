import logging
from typing import List

from openmodule.core import OpenModuleCore
from openmodule.models.base import ZMQMessage
from openmodule.rpc.server import RPCServer
from openmodule.models.backend import AccessRequest, AccessResponse, CountMessage, MediumAccesses, Access


class Backend:
    """
    Backend template class
    provides basic functionality used for backups
    * subscribes to BackendMessages and automatically registers backend
    * subscribes to CountMessages and calls check_in/check_out correspondingly
    * provides method for the backend / auth rpc with the check_backend_access method

    """

    def __init__(self, core: OpenModuleCore, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.core = core
        self.log = logging.getLogger()

        self.register_at_controller()
        self.core.messages.register_handler(b"count", CountMessage, self.handle_message)
        self.core.messages.register_handler(b"backend", ZMQMessage, self.handle_backend_message)

    def register_rpcs(self, rpc_server: RPCServer):
        rpc_server.add_filter(self._backend_filter, "backend", "auth")
        rpc_server.register_handler("backend", "auth", request_class=AccessRequest,
                                    response_class=AccessResponse, handler=self.rpc_check_access)

    def _backend_filter(self, request, message, handler) -> bool:
        backend = request.name
        if not backend:
            return False
        return self.core.config.NAME == backend

    def check_access(self, request: AccessRequest) -> List[Access]:
        """
        this method checks if current mediums has access to parking lot
        it should raise an Exception if it fails
        :param request: AccessRequest
        :return: Acesses
        """
        raise NotImplementedError()

    def check_in(self, message: CountMessage):
        """
       this method should check in the user of the message in the backend
        it should raise an Exception if it fails
       :param message: CountMessage
       """
        raise NotImplementedError()

    def check_out(self, message: CountMessage):
        """
        this method should check out the user of the message of the backend
        :param message: CountMessage
        """
        raise NotImplementedError()

    def shutdown(self):
        """
        this method should be used if a shutdown routine is required
        """
        pass

    def handle_message(self, message):
        try:
            if message.gateway.direction == "in":
                self.check_in(message)
            else:
                self.check_out(message)
            self.log.info(f"Sending check_{message.gateway.direction} for {message.user} successful")
            return True
        except Exception as e:
            self.log.exception(f"Sending check_{message.gateway.direction} for {message.user} failed")
            return False

    def rpc_check_access(self, request: AccessRequest, _) -> AccessResponse:
        gate_log_string = f"({request.gateway.gate}/{request.gateway.direction})" if request.gateway else ""

        try:
            accesses = self.check_access(request)
        except Exception as e:
            self.log.exception(f"check access request had an internal error {gate_log_string}")
            return AccessResponse(success=False,
                                  medium=MediumAccesses(accesses=[], id=request.id, type=request.medium_type))

        if accesses:
            self.log.info(f"{request.id}:{request.medium_type} has {len(accesses)} permissions {gate_log_string}")
            return AccessResponse(success=True,
                                  medium=MediumAccesses(id=request.id, type=request.medium_type, accesses=accesses))
        else:
            self.log.info(f"{request.id} medium {request.medium_type} has NO parking permissions {gate_log_string}")
            return AccessResponse(success=True,
                                  medium=MediumAccesses(accesses=[], id=request.id, type=request.medium_type))

    def handle_backend_message(self, message: ZMQMessage):
        if message.type.lower() == "register_request":
            self.register_at_controller()

    def register_at_controller(self):
        message = ZMQMessage(name=self.core.config.NAME, type="register")
        self.core.publish(message, b"backend")
