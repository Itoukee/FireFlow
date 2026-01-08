from datetime import date
from pydantic import BaseModel
from typing import Optional


class Firewall(BaseModel):
    id: Optional[int] = None
    name: str
    description: str
    created_at: date
    updated_at: date

    def to_dict(self):
        """
        Returns:
           The object as a dict
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
