from domain.policy.repository import PolicyRepository


class PaginatePoliciesByFirewallUC:
    def __init__(self, repo: PolicyRepository) -> None:
        self.repo = repo

    def execute(self, firewall_id: int, page: int, limit: int):
        return self.repo.paginate_by_firewall(firewall_id, page, limit)
