from abc import ABC, abstractmethod
from typing import Optional

from domain.policy.entity import Policy
from domain.policy.ports import PolicyPatch


class PolicyRepository(ABC):
    """
    Interface to interact with the policies
    """

    def __init__(self) -> None:
        pass

    @abstractmethod
    def create(self, firewall_id: int, policy: Policy) -> Policy:
        pass

    @abstractmethod
    def paginate_by_firewall(
        self, firewall_id: int, page: int, limit: int
    ) -> tuple[list[Policy], int]:
        pass

    @abstractmethod
    def get_by_id(self, policy_id: int, firewall_id: int) -> Optional[Policy]:
        pass

    @abstractmethod
    def update(self, policy_id: int, firewall_id: int, upd: PolicyPatch) -> Policy:
        pass


"""TODO implement the other CRUD operations    

    @abstractmethod
    def delete(self, firewall_id: int) -> bool:
        pass
 """
