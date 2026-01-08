from datetime import date
from typing import Literal, Optional
from pydantic import BaseModel


class Rule(BaseModel):
    id: Optional[int] = None
    policy_id: int
    name: str
    source_ip: int
    destination_ip: int
    protocol: Literal["tcp", "udp", "any"]
    port: int
    action: Literal["allow", "deny"]
    enabled: bool
    order: int
    created_at: date
    updated_at: date

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
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
