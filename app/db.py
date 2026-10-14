from collections.abc import Iterator
from pathlib import Path

from sqlalchemy.engine import make_url
from sqlmodel import Session, create_engine

from app.config import config


def crear_engine(url: str):
    url_parseada = make_url(url)
    if url_parseada.drivername.startswith("sqlite") and url_parseada.database:
        # SQLite no crea la carpeta del archivo por su cuenta.
        Path(url_parseada.database).parent.mkdir(parents=True, exist_ok=True)
    return create_engine(url, connect_args={"check_same_thread": False})


engine = crear_engine(config.database_url)


def get_session() -> Iterator[Session]:
    with Session(engine) as session:
        yield session
