from typing import Optional
from pydantic import BaseModel


class FirewallUpdate(BaseModel):
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


class GetFirewalls(BaseModel):
    page: Optional[int] = 0
    limit: int
