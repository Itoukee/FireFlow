from abc import ABC, abstractmethod
from typing import Any

from sqlalchemy import create_engine


class SqlDatabaseInterface(ABC):
    def __init__(self, db_url: str) -> None:
        self.engine = create_engine(db_url)

        pass

    @abstractmethod
    def connect(self):
        pass
