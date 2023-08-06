from enum import Enum
from pydantic import BaseModel, Field


class HeartbeatEventType(str, Enum):
    NEW = 'NEW'
    LOST = 'LOST'


class HeartbeatEvent(BaseModel):
    event_type: HeartbeatEventType = Field(HeartbeatEventType.NEW)
    namespace: str = Field("namespace")
    service_name: str = Field("service_name")
    host_ip: str = Field("0.0.0.0")
    hostname: str = Field("hostname")
    timestamp: int = Field(0)
