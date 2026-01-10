from typing import Optional
from pydantic import BaseModel

from domain.enums import DefaultAction


class PolicyCreate(BaseModel):
    firewall_id: int
    name: str
    default_action: Optional[DefaultAction]
    priority: Optional[int] = 0


class PolicyPatch(BaseModel):
    name: Optional[str] = None
    default_action: Optional[DefaultAction] = None
    priority: Optional[int] = None
