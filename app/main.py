from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from app.rutas import materias
from app.rutas.plantillas import plantillas
from app.servicios.errores import NoEncontrado

app = FastAPI(title="Cursada")
app.mount(
    "/estaticos",
    StaticFiles(directory=Path(__file__).resolve().parent / "estaticos"),
    name="estaticos",
)
app.include_router(materias.router)


@app.exception_handler(NoEncontrado)
def no_encontrado(request: Request, _: NoEncontrado):
    return plantillas.TemplateResponse(request, "no_encontrado.html", status_code=404)


@app.get("/")
def inicio():
    # Hasta que exista la vista "esta semana" (F2, D3), el inicio es Materias.
    return RedirectResponse("/materias", status_code=303)
