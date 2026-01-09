from typing import Literal, Optional
from datetime import date, datetime

from pydantic import BaseModel
from enum import Enum


class DefaultAction(str, Enum):
    ALLOW = "ALLOW"
    DENY = "DENY"


class Policy(BaseModel):
    id: Optional[int] = None
    firewall_id: int
    name: str
    default_action: DefaultAction
    priority: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def to_dict(self):
        """
        Returns:
           The object as a dict
        """
        return {
            "id": self.id,
            "firewall_id": self.firewall_id,
            "name": self.name,
            "default_action": self.default_action,
            "priority": self.priority,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at),
        }
