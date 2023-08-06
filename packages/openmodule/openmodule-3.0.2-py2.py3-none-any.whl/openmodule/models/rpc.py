from typing import Optional, Dict, Any
from uuid import UUID

from openmodule.models.base import ZMQMessage


class RPCRequest(ZMQMessage):
    rpc_id: UUID
    request: Optional[Dict]


class RPCResponse(ZMQMessage):
    rpc_id: Optional[UUID]
    response: Any
