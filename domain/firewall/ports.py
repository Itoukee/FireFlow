from typing import Optional
from pydantic import BaseModel


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
