from infrastructure.exceptions import NotFoundError
from domain.firewall.repository import FirewallRepository
from domain.policy.repository import PolicyRepository


class DeletePolicyByIdUC:
    def __init__(
        self, repo: PolicyRepository, firewall_repo: FirewallRepository
    ) -> None:
        self.repo = repo
        self.firewall_repo = firewall_repo

    def execute(self, firewall_id: int, policy_id: int):
        """Executes the use case
        Args:
            firewall_id (int)
            policy_id (int)

        Raises:
            NotFoundError


        Returns:
            _type_: True | None
        """
        firewall = self.firewall_repo.get_by_id(firewall_id)
        if not firewall:
            raise NotFoundError(f"The firewall id={firewall_id} doesn't exist")

        succeed = self.repo.delete(policy_id)

        return succeed
