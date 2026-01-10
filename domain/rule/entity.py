from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from domain.enums import Protocol, DefaultAction


class Rule(BaseModel):
    id: Optional[int] = None
    policy_id: int
    name: str
    source_ip: Optional[str]
    destination_ip: Optional[str]
    protocol: Protocol
    port: Optional[int]
    action: DefaultAction
    enabled: bool
    order: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def to_dict(self):
        """
        Returns:
           The object as a dict
        """
        return {
            "id": self.id,
            "policy_id": self.policy_id,
            "name": self.name,
            "source_ip": self.source_ip,
            "destination_ip": self.destination_ip,
            "protocol": self.protocol,
            "port": self.port,
            "action": self.action,
            "enabled": self.enabled,
            "order": self.order,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at),
        }
