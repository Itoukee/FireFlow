from domain.firewall.repository import FirewallRepository


class GetFirewallByIdUC:
    def __init__(self, repo: FirewallRepository) -> None:
        self.repo = repo

    def execute(self, firewall_id: int):
        return self.repo.get_by_id(firewall_id)
