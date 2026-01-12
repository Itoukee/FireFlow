from sqlalchemy.orm import joinedload

from infrastructure.exceptions import NotFoundError
from domain.firewall.entity import Firewall
from domain.firewall.ports import ChargedFirewall, FirewallPatch, ChargedPolicy
from domain.firewall.repository import FirewallRepository
from domain.rule.entity import Rule
from infrastructure.firewall.sql_model import FirewallModel
from infrastructure.databases.sql import get_database_session
from infrastructure.policy.sql_model import PolicyModel


class FirewallSQLRepository(FirewallRepository):
    """
    SQL Implementation of the Domain Repository
    """

    def __init__(self) -> None:
        self.session = get_database_session()

    def __to_entity(self, item: FirewallModel):
        """Maps the Sql model to the business entity"""
        return Firewall(
            id=item.id,
            name=item.name,
            description=item.description,
            created_at=item.created_at,
            updated_at=item.updated_at,
        )

    def __to_charged_firewall(self, item: FirewallModel):
        """Maps a firewall to its entire entity
        Surcharged by its children

        Args:
            item (FirewallModel)
        """
        # Should order in db but had an issue with joinedload
        return ChargedFirewall(
            id=item.id,
            name=item.name,
            description=item.description,
            policies=[
                ChargedPolicy(
                    id=p.id,
                    name=p.name,
                    default_action=p.default_action,
                    priority=p.priority,
                    rules=[
                        Rule(
                            id=r.id,
                            policy_id=r.policy_id,
                            name=r.name,
                            source_ip=r.source_ip,
                            destination_ip=r.destination_ip,
                            port=r.port,
                            protocol=r.protocol,
                            action=r.action,
                            enabled=r.enabled,
                            order=r.order,
                        )
                        for r in sorted(p.rules, key=lambda x: x.order)
                    ],
                )
                for p in sorted(item.policies, key=lambda x: x.priority)
            ],
        )

    def __patch_item(self, row: FirewallModel, upd: FirewallPatch):
        """Helper to update the attributes"""
        for key, value in upd.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        return row

    def name_exists(self, name: str):
        """Check if a row already exists with this name
        Args:
            name (str)
        Returns:
            bool
        """
        return bool(self.session.query(FirewallModel).filter_by(name=name).first())

    def create(self, firewall: Firewall) -> Firewall:
        """Creates a new firewall

        Args:
            firewall (Firewall): The firewall object to insert

        Returns:
            Firewall: newly inserted item
        """
        row = FirewallModel(
            name=firewall.name,
            description=firewall.description,
        )

        self.session.add(row)
        self.session.commit()

        # Assign the properties that were missing before the commit()
        firewall.id = row.id
        firewall.created_at = row.created_at.now()
        firewall.updated_at = row.updated_at.now()

        return firewall

    def paginate(self, page: int, limit: int) -> tuple[list[Firewall], int]:
        """
        Returns a list of firewalls with the total count of records
        Uses pagination for optimization

        Args:
            page (int)
            limit (int)

        Returns:
            tuple[list[Firewall], int]
        """
        query = self.session.query(FirewallModel)
        total_records = query.count()

        # Starts at page 0
        items = query.offset(page * limit).limit(limit).all()

        firewall_items = [self.__to_entity(item) for item in items]

        return firewall_items, total_records

    def get_by_id(self, firewall_id: int) -> Firewall | None:
        """Gets a firewall by id

        Args:
            firewall_id: unique id

        Returns:
            Firewall | None
        """
        row = self.session.query(FirewallModel).filter_by(id=firewall_id).first()

        if row:
            return self.__to_entity(row)
        return None

    def patch(self, firewall_id: int, upd: FirewallPatch):
        """Patches a firewall

        Args:
            firewall_id (int): unique id
            upd (FirewallPatch): potential rows to update

        Raises:
            NotFoundError: If not found

        Returns:
            Firewall: the patched row
        """
        row = self.session.query(FirewallModel).filter_by(id=firewall_id).first()
        if not row:
            raise NotFoundError(
                f"The firewall id={firewall_id} to update was not found"
            )

        row = self.__patch_item(row, upd)

        self.session.commit()
        self.session.refresh(row)

        return self.__to_entity(row)

    def delete(self, firewall_id: int) -> bool:
        """Delete a firewall in cascade wih its children relations

        Args:
            firewall_id (int): unique id

        Raises:
            NotFoundErrorrror: If not found

        Returns:
            bool: True | error raised
        """
        row = self.session.query(FirewallModel).filter_by(id=firewall_id).first()
        if not row:
            raise NotFoundError(
                f"The firewall id={firewall_id} to delete was not found"
            )

        self.session.delete(row)
        self.session.commit()

        return True

    def get_policies_and_rules(self, firewall_id: int) -> ChargedFirewall | None:
        """Returns a firewall with its policies and rules loaded

        Args:
            firewall_id (int)
        Returns:
            Firewall
        """
        row = (
            self.session.query(FirewallModel)
            .filter_by(id=firewall_id)
            .options(joinedload(FirewallModel.policies).joinedload(PolicyModel.rules))
        ).first()
        if row:
            return self.__to_charged_firewall(row)
        return None
