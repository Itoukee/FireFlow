import ipaddress

from typing import Optional
from pydantic import BaseModel, ValidationError, field_validator
from domain.enums import DefaultAction, Protocol


class CreateRule(BaseModel):
    policy_id: int
    name: str
    action: DefaultAction
    order: int
    enabled: bool
    source_ip: Optional[str] = None
    destination_ip: Optional[str] = None
    protocol: Optional[Protocol] = None
    port: Optional[int] = None

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


class PatchRule(BaseModel):
    name: Optional[str] = None
    action: Optional[DefaultAction] = None
    order: Optional[int] = None
    enabled: Optional[bool] = None
    source_ip: Optional[str] = None
    destination_ip: Optional[str] = None
    port: Optional[int] = None
    protocol: Optional[Protocol] = None

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
