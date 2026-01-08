from typing import Optional
from pydantic import BaseModel


class FirewallUpdate(BaseModel):
    """
    Update model made to avoid making updates on unwanted properties
    """

    name: Optional[str]
    description: Optional[str]


class FirewallCreate(BaseModel):
    """
    Create firewall model, type safe
    """

    name: str
    description: Optional[str]


class GetFirewalls(BaseModel):
    page: Optional[int] = 0
    count: int
    limit: int
