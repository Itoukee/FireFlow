from sqlalchemy.orm import declarative_base

from settings import settings
from infrastructure.databases.sqlite import SqliteDatabase
from ports.sql_database import SqlDatabaseInterface


def get_database() -> SqlDatabaseInterface | None:
    """
    Simple function made to handle the selection of sql databases
    Returns: The chosen SQL Database
    """
    db: SqlDatabaseInterface | None = None
    match settings.db_type:
        case "sqlite":
            db = SqliteDatabase()
        case _:
            db = None
    return db


Base = declarative_base()
