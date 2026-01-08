from domain.firewall.repository import FirewallRepository


class DeleteFirewallUC:
    def __init__(self, repo: FirewallRepository) -> None:
        self.repo = repo

    def execute(self, firewall_id: int):
        return self.repo.delete(firewall_id)
