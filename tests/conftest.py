import os

from fastapi.testclient import TestClient
from pytest import fixture
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.extensions import Base, get_db_session
from src.runner import app

DATABASE = os.getenv("DATABASE_NAME")
SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI") + DATABASE


@fixture(name="session")
def session_fixture():
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    Base.metadata.create_all(engine)

    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = Session()

    session.begin_nested()
    yield session
    session.rollback()


@fixture(name="client")
def client_fixture(session):
    def get_session_override():
        return session

    app.dependency_overrides[get_db_session] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
