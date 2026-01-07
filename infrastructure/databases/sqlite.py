import sqlite3
from typing import Any

from settings import settings
from ports.sql_database import SqlDatabaseInterface


class SqliteDatabase(SqlDatabaseInterface):
    def __init__(self):
        self.db_path = f"{settings.db_name}.sqlite"
        self.con = None

    def connect(self):
        self.con = sqlite3.connect(self.db_path)
        self.con.row_factory = sqlite3.Row

    def disconnect(self):
        if self.con:
            self.con.close()

    def execute(self, query: str, params: tuple = ()) -> None:
        if self.con:
            self.con.execute(query, params)

    def fetch_one(self, query: str, params: tuple = ()) -> dict[str, Any] | None:
        if self.con:
            cursor = self.con.cursor()
            cursor.execute(query, params)
            row = cursor.fetchone()
            return dict(row) if row else None

        raise Exception("Can't fetch_one without a database connection")

    def fetch_all(self, query: str, params: tuple = ()) -> list[dict[str, Any]]:
        if self.con:
            cursor = self.con.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

        raise Exception("Can't fetch_all without a database connection")
