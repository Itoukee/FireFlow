import ipaddress

from typing import Optional
from pydantic import BaseModel, field_validator


class Packet(BaseModel):
    source_ip: str
    destination_ip: str
    port: Optional[int] = None
    protocol: Optional[str] = None

    @field_validator("source_ip", "destination_ip")
    @classmethod
    def validate_ip(cls, value):
        if value is None:
            return value
        ipaddress.ip_address(value)
        return value

    @field_validator("port")
    @classmethod
    def validate_port(cls, value):
        if value is None:
            return value
        if not 1 <= value <= 65535:
            raise ValueError("Port must be between 1 and 65535")
        return value
