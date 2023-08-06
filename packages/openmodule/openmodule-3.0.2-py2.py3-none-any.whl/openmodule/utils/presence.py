import logging
from typing import Optional, Dict, Union


from openmodule.dispatcher import EventListener, MessageDispatcher
from openmodule.models.base import Gateway
from openmodule.models.presence import PresenceBaseMessage, PresenceBackwardMessage, PresenceForwardMessage, \
    PresenceChangeMessage, PresenceLeaveMessage, PresenceEnterMessage
from openmodule.models.vehicle import Vehicle


def vehicle_from_presence_message(message: PresenceBaseMessage):
    return Vehicle(
        id=message.vehicle_id,
        lpr=message.medium.lpr,
        qr=message.medium.qr,
        nfc=message.medium.nfc,
        pin=message.medium.pin,
    )


class PresenceListener:
    on_forward: EventListener[Union[Vehicle, Gateway]]
    on_backward: EventListener[Union[Vehicle, Gateway]]
    on_enter: EventListener[Union[Vehicle, Gateway]]
    on_leave: EventListener[Union[Vehicle, Gateway]]
    on_change: EventListener[Union[Vehicle, Gateway]]

    present_vehicles: Dict[str, Vehicle]

    @property
    def present_vehicle(self) -> Vehicle:
        assert self.gate is not None, (
            "`.present_vehicle` may only be used when listening for a specific gate, this presence listener"
            "listens to all gates, please access the present vehicle per gate via `.present_vehicles[gate]`"
        )
        return self.present_vehicles.get(self.gate)

    def __init__(self, dispatcher: MessageDispatcher, gate: Optional[str] = None):
        self.log = logging.getLogger(self.__class__.__name__)
        self.on_forward = EventListener(log=self.log)
        self.on_backward = EventListener(log=self.log)
        self.on_enter = EventListener(log=self.log)
        self.on_change = EventListener(log=self.log)
        self.on_leave = EventListener(log=self.log)
        self.present_vehicles = dict()
        self.gate = gate

        dispatcher.register_handler(b"presence", PresenceBackwardMessage,
                                    self._on_backward, filter={"type": "backward"})
        dispatcher.register_handler(b"presence", PresenceForwardMessage,
                                    self._on_forward, filter={"type": "forward"})
        dispatcher.register_handler(b"presence", PresenceChangeMessage,
                                    self._on_change, filter={"type": "change"})
        dispatcher.register_handler(b"presence", PresenceLeaveMessage,
                                    self._on_leave, filter={"type": "leave"})
        dispatcher.register_handler(b"presence", PresenceEnterMessage,
                                    self._on_enter, filter={"type": "enter"})

    def _gate_matches(self, message: PresenceBaseMessage):
        return (self.gate is None) or (message.gateway.gate == self.gate)

    def _on_backward(self, message: PresenceBackwardMessage):
        if not self._gate_matches(message):
            return
        vehicle = vehicle_from_presence_message(message)
        self.log.debug("presence backward: %s", vehicle)
        self.on_backward(vehicle, message.gateway)

    def _on_forward(self, message: PresenceForwardMessage):
        if not self._gate_matches(message):
            return
        vehicle = vehicle_from_presence_message(message)
        self.log.debug("presence forward: %s", vehicle)
        self.on_forward(vehicle, message.gateway)

    def _on_leave(self, message: PresenceLeaveMessage):
        if not self._gate_matches(message):
            return
        leaving_vehicle = vehicle_from_presence_message(message)
        self.log.debug("presence leave: %s", leaving_vehicle)
        present_vehicle = self.present_vehicles.get(message.gateway.gate)
        if present_vehicle:
            if present_vehicle.id != leaving_vehicle.id:
                self.log.error("A vehicle left with a different vehicle id than the present one. Tracking is "
                               "inconsistent. We are fake-leaving the currently present vehicle, to ensure consistent "
                               "states.", extra={
                    "present_vehicle": str(present_vehicle),
                    "leaving_vehicle": str(leaving_vehicle)
                })
            self.present_vehicles.pop(message.gateway.gate, None)
            self.on_leave(leaving_vehicle, message.gateway)
        else:
            self.log.error("A vehicle left while non was previously present. Tracking is inconsistent. "
                           "The leave will be ignored, to ensure consistent states.",
                           extra={"leaving_vehicle": str(leaving_vehicle)})

    def _on_enter(self, message: PresenceEnterMessage):
        if not self._gate_matches(message):
            return
        new_vehicle = vehicle_from_presence_message(message)
        self.log.debug("presence enter: %s", new_vehicle)
        present_vehicle = self.present_vehicles.get(message.gateway.gate)
        if present_vehicle:
            self.log.error("A new vehicle entered while one was still present. Tracking is inconsistent. "
                           "A leave will be faked, to ensure consistent states.",
                           extra={
                               "present_vehicle": str(present_vehicle),
                               "new_vehicle": str(new_vehicle)
                           })
            self.present_vehicles.pop(message.gateway.gate, None)
            self.on_leave(present_vehicle, message.gateway)
        self.present_vehicles[message.gateway.gate] = new_vehicle
        self.on_enter(new_vehicle, message.gateway)

    def _on_change(self, message: PresenceChangeMessage):
        if not self._gate_matches(message):
            return
        vehicle = vehicle_from_presence_message(message)

        if message.change_vehicle_id:
            self.log.info(f"Changing vehicle ID from {self.present_vehicles[message.gateway.gate].id} to "
                          f"{message.vehicle_id}")
            self.present_vehicles[message.gateway.gate] = vehicle
        self.log.debug("presence change: %s", vehicle)
        self.on_change(vehicle, message.gateway)
