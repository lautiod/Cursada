from fastapi import Depends
from sqlmodel import Session, select

from app.db import get_session
from app.modelos import Usuario

EMAIL_DEMO = "demo@cursada.local"


def usuario_actual(session: Session = Depends(get_session)) -> Usuario:
    """Usuario logueado.

    STUB hasta C1: siempre devuelve el usuario demo y lo crea si no existe.
    Con C1 se reemplaza por la lectura de la cookie de sesión firmada,
    sin cambiar la firma, así las rutas y los servicios no se tocan.
    """
    usuario = session.exec(select(Usuario).where(Usuario.email == EMAIL_DEMO)).first()
    if usuario is None:
        usuario = Usuario(email=EMAIL_DEMO, password_hash="!sin-login", nombre="Demo")
        session.add(usuario)
        session.commit()
        session.refresh(usuario)
    return usuario
