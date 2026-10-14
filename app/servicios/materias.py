import unicodedata

from sqlmodel import Session, select

from app.modelos import Materia, MateriaDatos
from app.servicios.errores import NoEncontrado


def _clave_alfabetica(texto: str) -> str:
    sin_acentos = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    return sin_acentos.casefold()


def listar(session: Session, usuario_id: int) -> list[Materia]:
    """Materias activas del usuario: año más reciente primero, después cuatrimestre y nombre."""
    consulta = select(Materia).where(Materia.usuario_id == usuario_id, Materia.archivada == False)  # noqa: E712
    return sorted(
        session.exec(consulta).all(),
        key=lambda m: (-m.anio, m.cuatrimestre, _clave_alfabetica(m.nombre)),
    )


def crear(session: Session, usuario_id: int, datos: MateriaDatos) -> Materia:
    materia = Materia(usuario_id=usuario_id, **datos.model_dump())
    session.add(materia)
    session.commit()
    session.refresh(materia)
    return materia


def obtener(session: Session, usuario_id: int, materia_id: int) -> Materia:
    materia = session.get(Materia, materia_id)
    if materia is None or materia.usuario_id != usuario_id:
        raise NoEncontrado
    return materia


def editar(session: Session, usuario_id: int, materia_id: int, datos: MateriaDatos) -> Materia:
    materia = obtener(session, usuario_id, materia_id)
    materia.sqlmodel_update(datos.model_dump())
    session.commit()
    session.refresh(materia)
    return materia


def eliminar(session: Session, usuario_id: int, materia_id: int) -> None:
    materia = obtener(session, usuario_id, materia_id)
    session.delete(materia)
    session.commit()
