from domain.firewall.entity import Firewall
from domain.firewall.repository import FirewallRepository
from infrastructure.firewall.sql_model import FirewallModel

from sqlalchemy.orm import Session

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

        firewall.id = row.id
        firewall.created_at = row.created_at
        firewall.updated_at = row.updated_at

        return firewall
