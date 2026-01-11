from typing import Optional
from pydantic import BaseModel

from domain.enums import DefaultAction


class PacketAnswer(BaseModel):
    access: DefaultAction
    rule_id: Optional[int] = None
    policy_id: Optional[int] = None
    reason: Optional[str] = None
