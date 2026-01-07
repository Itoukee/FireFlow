from typing import Optional
from datetime import date


class Firewall:
    def __init__(
        self,
        firewall_id: Optional[int],
        name: str,
        description: str,
        created_at: date,
        updated_at: date,
    ) -> None:
        self.id = firewall_id
        self.name = name
        self.description = description
        self.created_at = created_at
        self.updated_at = updated_at
