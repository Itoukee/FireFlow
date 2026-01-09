from domain.policy.entity import Policy
from domain.policy.repository import PolicyRepository
from infrastructure.databases.sql import get_database_session
from infrastructure.firewall.sql_model import FirewallModel
from infrastructure.policy.sql_model import PolicyModel


class PolicySQLRepository(PolicyRepository):
    def __init__(self) -> None:
        self.session = get_database_session()

    def __to_entity(self, item: PolicyModel) -> Policy:
        """Maps the Sql model to the business entity"""
        return Policy(
            id=item.id,
            firewall_id=item.firewall_id,
            name=item.name,
            default_action=item.default_action,
            priority=item.priority,
            created_at=item.created_at,
            updated_at=item.updated_at,
        )

    def create(self, firewall_id: int, policy: Policy) -> Policy:
        """Creates a new policy associated to a firewall

        Args:
            firewall_id
            policy (Policy)

        Returns:
            Policy
        """

        firewall_parent = (
            self.session.query(FirewallModel).filter_by(id=firewall_id).first()
        )
        if not firewall_parent:
            raise ValueError("Can't create a policy without an existing firewall")

        row = PolicyModel(
            firewall_id=policy.firewall_id,
            name=policy.name,
            default_action=policy.default_action,
            priority=policy.priority,
        )
        self.session.add(row)
        self.session.commit()

        policy.id = row.id
        policy.created_at = row.created_at.now()
        policy.updated_at = row.updated_at.now()

        return policy
