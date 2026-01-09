from domain.policy.repository import PolicyRepository
from domain.policy.ports import PolicyPatch


class PatchPolicyUC:
    def __init__(self, repo: PolicyRepository) -> None:
        self.repo = repo

    def execute(self, policy_id: int, firewall_id: int, upd: PolicyPatch):
        return self.repo.update(policy_id, firewall_id, upd)
