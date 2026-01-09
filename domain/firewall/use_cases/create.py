from domain.firewall.entity import Firewall
from domain.firewall.ports import FirewallCreate
from domain.firewall.repository import FirewallRepository


class CreateFirewallUC:
    def __init__(self, repo: FirewallRepository) -> None:
        self.repo = repo

    def execute(self, create_firewall: FirewallCreate):
        exists = self.repo.name_exists(create_firewall.name)
        if exists:
            raise ValueError("Firewall with this name already exists")

        firewall = Firewall(
            name=create_firewall.name, description=create_firewall.description
        )

        return self.repo.create(firewall)
