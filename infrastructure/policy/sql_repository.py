from domain.policy.entity import Policy
from domain.policy.ports import PolicyPatch
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

    def paginate_by_firewall(
        self, firewall_id: int, page: int, limit: int
    ) -> tuple[list[Policy], int]:
        """
        Returns a list of policies with the total count of records
        Uses pagination for optimization

        Args:
            page (int)
            limit (int)

        Returns:
            tuple[list[Policy], int]
        """
        query = self.session.query(PolicyModel).filter_by(firewall_id=firewall_id)
        total_records = query.count()

        # Starts at page 0
        items = query.offset(page * limit).limit(limit).all()

        policies = [self.__to_entity(item) for item in items]

        return policies, total_records

    def get_by_id(self, policy_id: int, firewall_id: int) -> Policy | None:
        """Gets a policy by id

        Args:
            policy_id: unique id

        Returns:
            Policy | None
        """
        row = (
            self.session.query(PolicyModel)
            .filter_by(id=policy_id, firewall_id=firewall_id)
            .first()
        )

        if row:
            return self.__to_entity(row)
        return None

    def update(self, policy_id: int, firewall_id: int, upd: PolicyPatch):
        """Patches a policy

        Args:
            policy_id (int): unique id
            upd (PolicyPatch): potential rows to update

        Raises:
            ValueError: If not found

        Returns:
            Policy: the patched row
        """
        row = (
            self.session.query(PolicyModel)
            .filter_by(id=policy_id, firewall_id=firewall_id)
            .first()
        )
        if not row:
            raise ValueError(
                f"The policy id={policy_id} and firewall_id id={firewall_id} to update was not found"
            )

        if upd.name:
            row.name = upd.name
        if upd.default_action:
            row.default_action = upd.default_action
        if upd.priority:
            row.priority = upd.priority

        self.session.commit()
        self.session.refresh(row)

        return self.__to_entity(row)

    def delete(self, firewall_id: int, policy_id: int) -> bool:
        """Delete a policy

        Args:
            firewall_id (int): unique id
            policy_id (int): unique id

        Raises:
            ValueError: If not found

        Returns:
            bool: True | error raised
        """
        row = (
            self.session.query(PolicyModel)
            .filter_by(id=policy_id, firewall_id=firewall_id)
            .first()
        )
        if not row:
            raise ValueError(
                f"The policy id={policy_id} and firewall id={firewall_id} to delete was not found"
            )

        self.session.delete(row)
        self.session.commit()

        return True
