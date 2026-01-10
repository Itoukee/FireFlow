from domain.exceptions import NotFoundError, ForbiddenError
from domain.policy.repository import PolicyRepository
from domain.rule.ports import PatchRule
from domain.rule.repository import RuleRepository


class PatchRuleUC:
    def __init__(self, repo: RuleRepository, policy_repo: PolicyRepository) -> None:
        self.repo = repo
        self.policy_repo = policy_repo

    def execute(self, rule_id: int, firewall_id: int, policy_id: int, upd: PatchRule):
        policy = self.policy_repo.get_by_id_and_firewall(policy_id, firewall_id)
        if not policy:
            raise NotFoundError(
                f"The policy id={policy_id} associated does not exist, can't patch"
            )

        rule = self.repo.get_by_id_and_policy(rule_id, policy_id)
        if not rule:
            raise NotFoundError(
                f"The rule id={rule_id} to patch does not exist for this policy"
            )

        return self.repo.patch(rule_id, upd)
