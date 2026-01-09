from domain.policy.repository import PolicyRepository


class GetPolicyByIdUC:
    def __init__(self, repo: PolicyRepository) -> None:
        self.repo = repo

    def execute(self, firewall_id: int, policy_id: int):
        """Executes the use case

        if the policy does not belong to the firewall, won't be returned
        Args:
            firewall_id (int)
            policy_id (int)

        Raises:
            ValueError

        Returns:
            _type_: Policy | None
        """
        policy = self.repo.get_by_id(policy_id)

        if policy and policy.firewall_id != firewall_id:
            raise ValueError("Policy does not belong to this Firewall")
        return policy
