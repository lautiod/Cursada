from datetime import UTC, datetime

from sqlmodel import Field, SQLModel


class Usuario(SQLModel, table=True):
    __tablename__ = "usuarios"

    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(max_length=255, unique=True, index=True)
    password_hash: str = Field(max_length=255)
    nombre: str = Field(max_length=100)
    creado_en: datetime = Field(default_factory=lambda: datetime.now(UTC))
