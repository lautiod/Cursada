# Cursada

Todas las fechas de la facultad en un solo lugar, el acceso a todo lo de cada materia y un espacio de estudio con IA sobre tus apuntes. Más detalles en [`docs/PRD.md`](docs/PRD.md) y [`docs/DISENO.md`](docs/DISENO.md).

## Cómo arrancar

Requiere Python 3.12.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
copy .env.example .env      # y completar los valores
alembic upgrade head        # crea datos/cursada.db
uvicorn app.main:app --reload
```

La app queda en http://localhost:8000.

## Tests

```powershell
pytest
```

Además de la lógica, los tests verifican que un usuario no pueda acceder a datos de otro y que las migraciones de Alembic coincidan con los modelos.

## Migraciones

Después de cambiar un modelo en `app/modelos/`:

```powershell
alembic revision --autogenerate -m "descripción del cambio"
alembic upgrade head
```

## Estado

Todavía no hay login (C1): la app usa un usuario demo, que crea `app/dependencias.py`.
