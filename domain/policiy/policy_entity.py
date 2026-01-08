from typing import Literal, Optional
from datetime import date

from pydantic import BaseModel


class Policy(BaseModel):
    id: Optional[int] = None
    firewall_id: int
    name: str
    default_action: Literal["deny", "access"]
    priority: int
    created_at: date
    updated_at: date

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
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
