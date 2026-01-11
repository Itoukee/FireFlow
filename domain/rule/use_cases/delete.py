from domain.exceptions import NotFoundError
from domain.policy.repository import PolicyRepository
from domain.rule.repository import RuleRepository


class DeleteRuleByIdUC:
    def __init__(self, repo: RuleRepository, policy_repo: PolicyRepository) -> None:
        self.repo = repo
        self.policy_repo = policy_repo

    def execute(self, rule_id: int, firewall_id: int, policy_id: int):
        """Executes the use case
        Args:
            rule_id (int)
            policy_id (int)

        Raises:
            NotFoundError


        Returns:
            _type_: True | None
        """
        policy = self.policy_repo.get_by_id_and_firewall(policy_id, firewall_id)
        if not policy:
            raise NotFoundError(
                f"The policy id={policy_id} doesn't exist for this firewall"
            )

        succeed = self.repo.delete(rule_id)

        return succeed
