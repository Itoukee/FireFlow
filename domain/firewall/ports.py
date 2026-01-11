from typing import Optional
from pydantic import BaseModel

from domain.firewall.entity import Firewall
from domain.rule.entity import Rule


class FirewallPatch(BaseModel):
    """
    Update model made to avoid making updates on unwanted properties
    """

    name: Optional[str] = None
    description: Optional[str] = None


class FirewallCreate(BaseModel):
    """
    Create firewall model, type safe
    """

    name: str
    description: Optional[str]


class ChargedPolicy(BaseModel):
    id: int
    name: str
    default_action: str
    priority: Optional[int]
    rules: list[Rule]


class ChargedFirewall(BaseModel):
    id: int
    name: str
    description: Optional[str]
    policies: list[ChargedPolicy]
