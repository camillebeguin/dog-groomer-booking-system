import logging
from contextlib import contextmanager
from pathlib import Path

import psycopg2
import pytest
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from app.core.config import settings
from app.main import app
from app.model.base import BaseModel

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

APP_FOLDER = Path(__file__).parent.parent

@pytest.fixture(scope="session")
def session():
    suffix = "_test"
    db_name = f"{settings.POSTGRES_DB}{suffix}"
    uri = f"{settings.SQLALCHEMY_DATABASE_URI}{suffix}"

    create_db(db_name)

    engine = create_engine(uri)
    run_migrations(engine, app_folder=APP_FOLDER)

    session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    scoped = scoped_session(session)
    BaseModel.metadata.create_all(engine)  # type: ignore
    return scoped

    # engine = create_engine("sqlite://")

    # with engine.connect() as conn:
    #     BaseModel.metadata.create_all(conn)
    #     yield sessionmaker(bind=engine, expire_on_commit=False)


@pytest.fixture(scope="function")
def api_client(session):
    with TestClient(app) as client:
        yield client

@contextmanager
def get_main_conn(settings):
    conn = psycopg2.connect(
        host=settings.POSTGRES_SERVER,
        database=settings.POSTGRES_MAIN_DB,
        user=settings.POSTGRES_MAIN_USER,
        password=settings.POSTGRES_MAIN_PASSWORD,
    )
    conn.autocommit = True
    yield conn
    conn.close()

def create_db(db_name):
    conn = None
    with get_main_conn(settings) as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                f"SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = '{db_name}'"
            )
            cursor.execute(f"DROP DATABASE IF EXISTS {db_name}")
            cursor.execute(f"CREATE DATABASE {db_name}")

    conn.close()

def drop_db(db_name):
    with get_main_conn(settings) as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                f"SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = '{db_name}'"
            )
            cursor.execute(f"DROP DATABASE IF EXISTS {db_name}")

    conn.close()

def run_migrations(engine, app_folder, rev="head") -> None:
    alembic_config = app_folder / "alembic.ini"
    alembic_folder = app_folder / "alembic"

    logging.info("Running DB migrations in %r", str(alembic_folder))
    alembic_cfg = Config(str(alembic_config))
    alembic_cfg.set_main_option("script_location", str(alembic_folder))
    with engine.begin() as connection:
        alembic_cfg.attributes["connection"] = connection
        command.upgrade(alembic_cfg, rev)


