from pathlib import Path

from fastapi.templating import Jinja2Templates

plantillas = Jinja2Templates(directory=Path(__file__).resolve().parent.parent / "plantillas")
plantillas.env.globals["CUATRIMESTRES"] = {
    "1": "1.er cuatrimestre",
    "2": "2.º cuatrimestre",
    "anual": "Anual",
}
