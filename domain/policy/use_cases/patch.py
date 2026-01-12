from infrastructure.exceptions import NotFoundError
from domain.firewall.repository import FirewallRepository
from domain.policy.repository import PolicyRepository
from domain.policy.ports import PolicyPatch


class PatchPolicyUC:
    def __init__(
        self, repo: PolicyRepository, firewall_repo: FirewallRepository
    ) -> None:
        self.repo = repo
        self.firewall_repo = firewall_repo

    def execute(self, policy_id: int, firewall_id: int, upd: PolicyPatch):

        firewall = self.firewall_repo.get_by_id(firewall_id)
        if not firewall:
            raise NotFoundError(
                f"The firewall id={firewall_id} associated does not exist, can't patch"
            )

        return self.repo.update(policy_id, upd)
