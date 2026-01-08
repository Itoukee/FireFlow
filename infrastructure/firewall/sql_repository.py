from domain.firewall.entity import Firewall
from domain.firewall.repository import FirewallRepository
from infrastructure.firewall.sql_model import FirewallModel

from infrastructure.databases.sql import get_database_session


class FirewallSQLRepository(FirewallRepository):
    """
    SQL Implementation of the Domain Repository
    """

    def __init__(self) -> None:
        self.session = get_database_session()

    def create(self, firewall: Firewall) -> Firewall:
        row = FirewallModel(
            name=firewall.name,
            description=firewall.description,
        )

        self.session.add(row)
        self.session.commit()

        # Assign the properties that were missing before the commit()
        firewall.id = row.id
        firewall.created_at = row.created_at.date()
        firewall.updated_at = row.updated_at.date()

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

        firewall_items = [
            Firewall(
                id=item.id,
                name=item.name,
                description=item.description,
                created_at=item.created_at.date(),
                updated_at=item.updated_at.date(),
            )
            for item in items
        ]

        return firewall_items, total_records

    def get_by_id(self, firewall_id: int) -> Firewall | None:
        """Gets a firewall by id

        Args:
            firewall_id (int)

        Returns:
            Firewall | None
        """
        row = self.session.query(FirewallModel).filter_by(id=firewall_id).first()

        if row:
            return Firewall(id=row.id, name=row.name, description=row.description)
        return None
