from typing import Literal, Optional
from datetime import date, datetime

from pydantic import BaseModel


class Policy(BaseModel):
    id: Optional[int] = None
    firewall_id: int
    name: str
    default_action: Literal["deny", "access"]
    priority: int
    created_at: datetime
    updated_at: datetime

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
