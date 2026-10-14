from fastapi import FastAPI
from fastapi.responses import RedirectResponse

app = FastAPI(title="Cursada")


@app.get("/")
def inicio():
    # Hasta que exista la vista "esta semana" (F2, D3), el inicio es Materias.
    return RedirectResponse("/materias", status_code=303)
