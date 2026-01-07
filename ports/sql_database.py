from abc import ABC, abstractmethod
from typing import Any


class SqlDatabaseInterface(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self) -> None:
        pass

    @abstractmethod
    def execute(self, query: str, params: tuple = ()) -> None:
        pass

    @abstractmethod
    def fetch_one(self, query: str, params: tuple = ()) -> dict[str, Any] | None:
        pass

    @abstractmethod
    def fetch_all(self, query: str, params: tuple = ()) -> list[dict[str, Any]]:
        pass
