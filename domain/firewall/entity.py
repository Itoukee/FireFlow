from datetime import date
from pydantic import BaseModel
from typing import Optional


class Firewall(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str]
    created_at: Optional[date] = None
    updated_at: Optional[date] = None

    def to_dict(self):
        """
        Returns:
           The object as a dict
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at),
        }
