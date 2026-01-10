from typing import Optional
from pydantic import BaseModel

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


class PatchRule(BaseModel):
    name: Optional[str] = None
    action: Optional[DefaultAction] = None
    order: Optional[int] = None
    enabled: Optional[bool] = None
    source_ip: Optional[str] = None
    destination_ip: Optional[str] = None
    protocol: Optional[Protocol] = None
