from domain.policy.entity import DefaultAction, Policy
from domain.policy.ports import PolicyCreate
from domain.policy.repository import PolicyRepository


class CreatePolicyUC:
    def __init__(self, repo: PolicyRepository) -> None:
        self.repo = repo

    def execute(self, firewall_id: int, create_policy: PolicyCreate):
        """Use case of creating the policy

        Args:
            firewall_id (int): _description_
            create_policy (PolicyCreate): _description_

        Returns:
            New Policy
        """
        policy = Policy(
            firewall_id=firewall_id,
            name=create_policy.name,
            default_action=create_policy.default_action or DefaultAction.DENY,
            priority=create_policy.priority or 0,
        )

        return self.repo.create(firewall_id, policy)
