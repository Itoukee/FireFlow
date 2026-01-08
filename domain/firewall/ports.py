from typing import Optional
from pydantic import BaseModel


class FirewallUpdate(BaseModel):
    """
    Update model made to avoid making updates on unwanted properties
    """

    name: Optional[str]
    description: Optional[str]
