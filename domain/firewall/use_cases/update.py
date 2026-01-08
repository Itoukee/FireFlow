from domain.firewall.repository import FirewallRepository
from domain.firewall.ports import FirewallUpdate


class UpdateFirewallUC:
    def __init__(self, repo: FirewallRepository) -> None:
        self.repo = repo

    def execute(self, firewall_id: int, upd: FirewallUpdate):
        return self.repo.update(firewall_id, upd)
