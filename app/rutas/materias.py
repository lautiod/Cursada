from datetime import date

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from pydantic import ValidationError
from sqlmodel import Session

from app.db import get_session
from app.dependencias import usuario_actual
from app.modelos import Materia, MateriaDatos, Usuario
from app.rutas.plantillas import plantillas
from app.servicios import materias

router = APIRouter(prefix="/materias")

MENSAJES_ERROR = {
    "nombre": "Ingresá un nombre de hasta 100 caracteres.",
    "anio": "Ingresá un año entre 2000 y 2100.",
    "cuatrimestre": "Elegí 1.er cuatrimestre, 2.º cuatrimestre o anual.",
    "docente": "El docente puede tener hasta 100 caracteres.",
    "link_drive": "El link tiene que empezar con http:// o https://",
    "link_moodle": "El link tiene que empezar con http:// o https://",
}


async def _leer_formulario(request: Request) -> tuple[MateriaDatos | None, dict, dict]:
    """Devuelve (datos válidos o None, valores cargados, errores por campo)."""
    valores = dict(await request.form())
    try:
        return MateriaDatos.model_validate(valores), valores, {}
    except ValidationError as error:
        campos = {e["loc"][0] for e in error.errors() if e["loc"]}
        return None, valores, {campo: MENSAJES_ERROR[campo] for campo in campos}


def _formulario(request: Request, materia: Materia | None, valores=None, errores=None, **opciones):
    if valores is None:
        valores = materia.model_dump() if materia else {"anio": date.today().year, "cuatrimestre": "1"}
    return plantillas.TemplateResponse(
        request,
        "materias/_formulario.html",
        {"materia": materia, "valores": valores, "errores": errores or {}, "oob": False},
        **opciones,
    )


@router.get("", response_class=HTMLResponse)
def lista(
    request: Request,
    session: Session = Depends(get_session),
    usuario: Usuario = Depends(usuario_actual),
):
    return plantillas.TemplateResponse(
        request,
        "materias/lista.html",
        {
            "materias": materias.listar(session, usuario.id),
            "valores": {"anio": date.today().year, "cuatrimestre": "1"},
            "errores": {},
        },
    )


@router.post("", response_class=HTMLResponse)
async def crear(
    request: Request,
    session: Session = Depends(get_session),
    usuario: Usuario = Depends(usuario_actual),
):
    datos, valores, errores = await _leer_formulario(request)
    if datos is None:
        # El formulario con errores reemplaza al formulario, no a la lista.
        return _formulario(
            request, None, valores, errores,
            status_code=422,
            headers={"HX-Retarget": "#form-nueva", "HX-Reswap": "outerHTML"},
        )
    materias.crear(session, usuario.id, datos)
    # Devuelve la lista ordenada y, fuera de banda, un formulario vacío.
    return plantillas.TemplateResponse(
        request,
        "materias/_creada.html",
        {
            "materias": materias.listar(session, usuario.id),
            "valores": {"anio": datos.anio, "cuatrimestre": datos.cuatrimestre},
            "errores": {},
        },
    )


@router.get("/{materia_id}", response_class=HTMLResponse)
def ficha(
    request: Request,
    materia_id: int,
    session: Session = Depends(get_session),
    usuario: Usuario = Depends(usuario_actual),
):
    materia = materias.obtener(session, usuario.id, materia_id)
    return plantillas.TemplateResponse(request, "materias/ficha.html", {"materia": materia})


@router.get("/{materia_id}/editar", response_class=HTMLResponse)
def formulario_edicion(
    request: Request,
    materia_id: int,
    session: Session = Depends(get_session),
    usuario: Usuario = Depends(usuario_actual),
):
    materia = materias.obtener(session, usuario.id, materia_id)
    return _formulario(request, materia)


@router.put("/{materia_id}", response_class=HTMLResponse)
async def editar(
    request: Request,
    materia_id: int,
    session: Session = Depends(get_session),
    usuario: Usuario = Depends(usuario_actual),
):
    materia = materias.obtener(session, usuario.id, materia_id)
    datos, valores, errores = await _leer_formulario(request)
    if datos is None:
        return _formulario(request, materia, valores, errores, status_code=422)
    materia = materias.editar(session, usuario.id, materia_id, datos)
    return plantillas.TemplateResponse(request, "materias/_tarjeta.html", {"materia": materia})


@router.delete("/{materia_id}", response_class=HTMLResponse)
def eliminar(
    materia_id: int,
    session: Session = Depends(get_session),
    usuario: Usuario = Depends(usuario_actual),
):
    materias.eliminar(session, usuario.id, materia_id)
    # Respuesta vacía con 200: HTMX reemplaza la tarjeta por nada.
    return HTMLResponse("")
