from abc import ABC, abstractmethod
from typing import Optional

from domain.rule.entity import Rule
from domain.rule.ports import PatchRule


class RuleRepository(ABC):
    """
    Interface to interact with the policies
    """

    def __init__(self) -> None:
        pass

    @abstractmethod
    def create(self, rule: Rule) -> Rule:
        pass

    @abstractmethod
    def paginate_by_policy(
        self, policy_id: int, page: int, limit: int
    ) -> tuple[list[Rule], int]:
        pass

    @abstractmethod
    def name_exists_within_parent(self, name: str, policy_id: int) -> bool:
        pass

    @abstractmethod
    def get_by_id_and_policy(self, rule_id: int, policy_id: int) -> Optional[Rule]:
        pass

    @abstractmethod
    def patch(self, rule_id: int, upd: PatchRule) -> Rule:
        pass

    @abstractmethod
    def delete(self, rule_id: int) -> bool:
        pass
