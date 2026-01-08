from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import declarative_base, Session

from settings import settings


def get_database_session() -> Session:
    """
    Simple function made to handle the selection of sql databases
    Returns: The chosen SQL session
    """
    engine: Engine | None = None
    match settings.db_type:
        case "sqlite":
            engine = create_engine(f"sqlite:///{settings.db_name}.sqlite")
        case _:
            engine = create_engine(f"sqlite:///{settings.db_name}.sqlite")
    session = Session(engine)
    return session


Base = declarative_base()
