from domain.policy.repository import PolicyRepository


class DeletePolicyByIdUC:
    def __init__(self, repo: PolicyRepository) -> None:
        self.repo = repo

    def execute(self, firewall_id: int, policy_id: int):
        """Executes the use case
        Args:
            firewall_id (int)
            policy_id (int)

        Raises:
            ValueError

        Returns:
            _type_: Policy | None
        """
        policy = self.repo.delete(firewall_id=firewall_id, policy_id=policy_id)

        return policy
