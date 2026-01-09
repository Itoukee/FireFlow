from abc import ABC, abstractmethod

from domain.policy.entity import Policy


class PolicyRepository(ABC):
    """
    Interface to interact with the policies
    """

    def __init__(self) -> None:
        pass

    @abstractmethod
    def create(self, firewall_id: int, policy: Policy) -> Policy:
        pass


"""TODO implement the other CRUD operations    
@abstractmethod
    def paginate(self, page: int, limit: int) -> tuple[list[Firewall], int]:
        pass

    @abstractmethod
    def get_by_id(self, firewall_id: int) -> Optional[Firewall]:
        pass

    @abstractmethod
    def update(self, firewall_id: int, upd: FirewallPatch) -> Firewall:
        pass

    @abstractmethod
    def delete(self, firewall_id: int) -> bool:
        pass
 """
