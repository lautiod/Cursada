# Importar todos los modelos acá para que SQLModel.metadata los conozca (Alembic y tests).
from app.modelos.materia import Materia, MateriaDatos
from app.modelos.usuario import Usuario

__all__ = ["Materia", "MateriaDatos", "Usuario"]
