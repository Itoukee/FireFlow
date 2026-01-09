from domain.firewall.repository import FirewallRepository
from domain.firewall.ports import FirewallPatch


class PatchFirewallUC:
    def __init__(self, repo: FirewallRepository) -> None:
        self.repo = repo

    def execute(self, firewall_id: int, upd: FirewallPatch):
        return self.repo.patch(firewall_id, upd)
