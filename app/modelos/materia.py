from typing import Literal

from pydantic import ConfigDict, field_validator
from sqlmodel import Field, SQLModel

Cuatrimestre = Literal["1", "2", "anual"]


class Materia(SQLModel, table=True):
    __tablename__ = "materias"

    id: int | None = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key="usuarios.id", index=True)
    nombre: str = Field(max_length=100)
    anio: int  # año calendario en que se cursa, por ejemplo 2026
    cuatrimestre: str = Field(max_length=5)  # "1", "2" o "anual"
    docente: str | None = Field(default=None, max_length=100)
    link_drive: str | None = Field(default=None, max_length=500)
    link_moodle: str | None = Field(default=None, max_length=500)
    archivada: bool = Field(default=False)


class MateriaDatos(SQLModel):
    """Datos que el usuario carga al crear o editar una materia."""

    model_config = ConfigDict(str_strip_whitespace=True)

    nombre: str = Field(min_length=1, max_length=100)
    anio: int = Field(ge=2000, le=2100)
    cuatrimestre: Cuatrimestre
    docente: str | None = Field(default=None, max_length=100)
    link_drive: str | None = Field(default=None, max_length=500)
    link_moodle: str | None = Field(default=None, max_length=500)

    @field_validator("docente", "link_drive", "link_moodle", mode="before")
    @classmethod
    def vacio_a_none(cls, valor):
        if isinstance(valor, str) and not valor.strip():
            return None
        return valor

    @field_validator("link_drive", "link_moodle")
    @classmethod
    def link_http(cls, valor: str | None) -> str | None:
        if valor is not None and not valor.startswith(("http://", "https://")):
            raise ValueError("El link tiene que empezar con http:// o https://")
        return valor
