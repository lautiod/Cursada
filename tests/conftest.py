import pytest
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine

import app.modelos  # noqa: F401  (registra las tablas)
from app.modelos import Usuario


@pytest.fixture
def session():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    engine.dispose()


def _crear_usuario(session: Session, email: str) -> Usuario:
    usuario = Usuario(email=email, password_hash="x", nombre=email.split("@")[0])
    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    return usuario


@pytest.fixture
def usuario_a(session) -> Usuario:
    return _crear_usuario(session, "ana@test.com")


@pytest.fixture
def usuario_b(session) -> Usuario:
    return _crear_usuario(session, "beto@test.com")
