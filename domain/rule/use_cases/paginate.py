from domain.rule.repository import RuleRepository


class PaginateRulesByPolicyUC:
    def __init__(self, repo: RuleRepository) -> None:
        self.repo = repo

    def execute(self, policy_id: int, page: int, limit: int):
        return self.repo.paginate_by_policy(policy_id, page, limit)
