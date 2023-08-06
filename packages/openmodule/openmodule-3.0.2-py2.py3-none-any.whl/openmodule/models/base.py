from enum import Enum

import orjson
import zmq
from datetime import datetime
from pydantic import Field, BaseModel
from pydantic.main import ROOT_KEY


def _donotuse(v, *, default):
    assert False, "please use json_bytes"


class OpenModuleModel(BaseModel):
    class Config:
        validate_assignment = True

        json_loads = orjson.loads
        json_dumps = _donotuse

    def json_bytes(self):
        data = self.dict()
        if self.__custom_root_type__:
            data = data[ROOT_KEY]
        return orjson.dumps(data)

    def dict(self, **kwargs):
        kwargs.setdefault("by_alias", True)
        kwargs.setdefault("exclude_none", True)
        return super().dict(**kwargs)


class EmptyModel(OpenModuleModel):
    pass


class ZMQMessage(OpenModuleModel):
    timestamp: datetime = Field(default_factory=datetime.now)
    name: str
    type: str

    def publish_on_topic(self, pub_socket: zmq.Socket, topic: bytes):
        pub_socket.send_multipart((topic, self.json_bytes()))

    def dict(self, **kwargs):
        data = super().dict(**kwargs)
        if "timestamp" in data:
            data["timestamp"] = data["timestamp"].timestamp()
        return data


class Direction(str, Enum):
    UNKNOWN = ""
    IN = "in"
    OUT = "out"


class Gateway(OpenModuleModel):
    gate: str = ""
    direction: Direction = ""

    def __str__(self):
        return f"{self.gate}/{self.direction}"
