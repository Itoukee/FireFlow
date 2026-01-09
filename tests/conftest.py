from pytest import fixture
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from infrastructure.databases.sql import Base


@fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    session = Session(engine)

    yield session

    session.close()
