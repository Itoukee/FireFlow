from datetime import datetime

from domain.firewall.entity import Firewall
from domain.firewall.ports import FirewallPatch
from domain.firewall.repository import FirewallRepository
from infrastructure.firewall.sql_model import FirewallModel
from infrastructure.databases.sql import get_database_session


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

    def create(self, firewall: Firewall) -> Firewall:
        """Creates a new firewall

        Args:
            firewall (Firewall): The firewall object to insert

        Returns:
            Firewall: newly inserted item
        """

        name_exists = (
            self.session.query(FirewallModel).filter_by(name=firewall.name).first()
        )
        if name_exists:
            raise ValueError("A firewall with this name already exists")

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

    def update(self, firewall_id: int, upd: FirewallPatch):
        """Patch a firewall

        Args:
            firewall_id (int): unique id
            upd (FirewallUpdate): potential rows to update

        Raises:
            ValueError: If not found

        Returns:
            Firewall: the patched row
        """
        row = self.session.query(FirewallModel).filter_by(id=firewall_id).first()
        if not row:
            raise ValueError(f"The firewall id={firewall_id} to update was not found")

        if upd.name:
            row.name = upd.name
        if upd.description:
            row.description = upd.description

        self.session.commit()
        self.session.refresh(row)

        return self.__to_entity(row)

    def delete(self, firewall_id: int) -> bool:
        """Delete a firewall in cascade wih its children relations

        Args:
            firewall_id (int): unique id

        Raises:
            ValueError: If not found

        Returns:
            bool: True | error raised
        """
        row = self.session.query(FirewallModel).filter_by(id=firewall_id).first()
        if not row:
            raise ValueError(f"The firewall id={firewall_id} to delete was not found")

        self.session.delete(row)
        self.session.commit()

        return True
