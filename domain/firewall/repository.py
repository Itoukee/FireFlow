from abc import ABC, abstractmethod
from typing import Optional

from domain.firewall.entity import Firewall
from domain.firewall.ports import FirewallPatch


class FirewallRepository(ABC):
    """
    Interface to interact with the firewalls
    """

    def __init__(self) -> None:
        pass

    @abstractmethod
    def create(self, firewall: Firewall) -> Firewall:
        pass

    @abstractmethod
    def paginate(self, page: int, limit: int) -> tuple[list[Firewall], int]:
        pass

    @abstractmethod
    def get_by_id(self, firewall_id: int) -> Optional[Firewall]:
        pass

    @abstractmethod
    def patch(self, firewall_id: int, upd: FirewallPatch) -> Firewall:
        pass

    @abstractmethod
    def delete(self, firewall_id: int) -> bool:
        pass
