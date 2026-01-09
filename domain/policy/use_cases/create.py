from domain.enums import DefaultAction
from domain.firewall.repository import FirewallRepository
from domain.policy.entity import Policy
from domain.policy.ports import PolicyCreate
from domain.policy.repository import PolicyRepository


class CreatePolicyUC:
    def __init__(
        self, repo: PolicyRepository, firewall_repo: FirewallRepository
    ) -> None:
        self.repo = repo
        self.firewall_repo = firewall_repo

    def execute(self, firewall_id: int, create_policy: PolicyCreate):
        """Use case of creating the policy

        Args:
            firewall_id (int): _description_
            create_policy (PolicyCreate): _description_

        Returns:
            New Policy
        """

        firewall = self.firewall_repo.get_by_id(firewall_id)
        if not firewall:
            raise ValueError(f"The firewall id={firewall_id} doesn't exist")

        policy = Policy(
            firewall_id=firewall_id,
            name=create_policy.name,
            default_action=create_policy.default_action or DefaultAction.DENY,
            priority=create_policy.priority or 0,
        )

        return self.repo.create(policy)
