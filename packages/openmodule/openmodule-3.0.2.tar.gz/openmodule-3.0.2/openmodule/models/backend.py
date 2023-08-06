from datetime import datetime
from enum import Enum
from typing import List, Optional

from dateutil import rrule

from openmodule import config
from pydantic import validator
from openmodule.models.base import OpenModuleModel, ZMQMessage, Gateway


class Medium(str, Enum):
    LPR = "lpr"
    NFC = "nfc"
    PIN = "pin"
    QR = "qr"


class Category(str, Enum):
    BOOKED_DIGIMON = "booked-digimon"
    BOOKED_EMPLOYEE = "booked-employee"
    BOOKED_VISITOR = "booked-visitor"
    PERMANENT_DIGIMON = "permanent-digimon"
    PERMANENT_EMPLOYEE = "permanent-employee"
    FILLER_EMPLOYEE = "filler-employee"
    FILLER_DIGIMON = "filler-digimon"
    FILLER_VISITOR_BUTTON = "filler-visitor-button"
    FILLER_VISITOR_UNEXPECTED = "filler-visitor-unexpected"
    UNKNOWN_CATEGORY = "unknown-category"


class AccessRequest(OpenModuleModel):
    name: str
    gateway: Optional[Gateway] = None
    medium_type: Medium
    id: str


def check_recurrence(cls, recurrence, values, **kwargs):
    if recurrence == "":
        return recurrence
    if recurrence:
        if not values.get("duration"):
            raise ValueError("set duration when using recurrence")
        if not values.get("start"):
            raise ValueError("set start timestamp when using recurrence")
    try:
        rrule.rrulestr(recurrence)
    except Exception as e:
        raise ValueError(f"recurrence is not valid {e}")
    return recurrence


class Access(OpenModuleModel):
    category: Category
    start: datetime
    end: Optional[datetime] = None
    duration: Optional[int]
    recurrence: Optional[str]
    zone: Optional[str]
    occupant_check: bool = False
    infos: Optional[dict]
    user: str

    _check_recurrence = validator("recurrence", allow_reuse=True)(check_recurrence)

    def dict(self, **kwargs):
        data = super().dict(**kwargs)
        if "start" in data:
            data["start"] = data["start"].timestamp()
        if "end" in data:
            if data["end"] is not None:
                data["end"] = data["end"].timestamp()
        return data


class MediumAccesses(OpenModuleModel):
    accesses: List[Access]
    id: str
    type: str


class AccessResponse(OpenModuleModel):
    success: bool = False
    medium: MediumAccesses


class CountMessage(ZMQMessage):
    resource: str = config.resource()
    user: str
    gateway: Gateway
    medium_type: Medium
    id: str
    count: int
    transaction_id: str
    zone: str
    category: Category
    real: bool
    access_data: Optional[dict]
    error: Optional[str]
    previous_transaction_id: Optional[List[str]]  # double_entry, choose_random error
    previous_user: Optional[str]  # user_changed error
    previous_medium_type: Optional[str]  # medium_changed, medium_id_changed error
    previous_id: Optional[str]  # medium_changed, medium_id_changed error
    chosen: Optional[dict]  # choose_random error
