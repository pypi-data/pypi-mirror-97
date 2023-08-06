from datetime import datetime
from typing import Optional

from pydantic import Field

from openmodule.models.base import ZMQMessage, OpenModuleModel, Gateway
from openmodule.models.vehicle import Medium, LPRMedium


class PresenceMedia(OpenModuleModel):
    lpr: Optional[LPRMedium]
    qr: Optional[Medium]
    nfc: Optional[Medium]
    pin: Optional[Medium]


class PresenceBaseMessage(ZMQMessage):
    vehicle_id: int
    unsure: bool = False
    source: str
    present_area_name: str = Field(..., alias="present-area-name")
    last_update: datetime
    gateway: Gateway
    medium: PresenceMedia


class PresenceBackwardMessage(PresenceBaseMessage):
    type: str = "backward"
    leave_time: str = Field(..., alias="leave-time")


class PresenceForwardMessage(PresenceBaseMessage):
    type: str = "forward"
    leave_time: str = Field(..., alias="leave-time")


class PresenceLeaveMessage(PresenceBaseMessage):
    type: str = "leave"


class PresenceEnterMessage(PresenceBaseMessage):
    type: str = "enter"


class PresenceChangeMessage(PresenceBaseMessage):
    type: str = "change"
    change_vehicle_id: Optional[bool]
