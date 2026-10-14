# CLAUDE.md

## Proyecto

Cursada: app web para estudiantes universitarios. Reúne las fechas de entrega de todas las materias, los links de cada materia y un espacio de estudio con IA. El *qué* está en `docs/PRD.md` (funcionalidades con IDs: C1, M1, F2…) y el *cómo* en `docs/DISENO.md` (stack, modelo de datos, endpoints y decisiones D1–D5). Leelos antes de agregar una funcionalidad y mantené `DISENO.md` al día si cambia una tabla o una ruta. El código, los nombres y los mensajes están en español.

Si existe `docs/plan-faseN.md`, es el plan de la fase en curso: marcá cada checkbox al completar el paso.

## Comandos

El entorno virtual está en `.venv` (Windows). Si no está activado, usá `.venv/Scripts/python.exe -m ...`.

```powershell
pip install -e ".[dev]"                     # instalar
pytest                                      # todos los tests
pytest tests/test_servicio_materias.py::test_editar   # un solo test
alembic upgrade head                        # aplicar migraciones (crea datos/cursada.db)
alembic revision --autogenerate -m "..."    # después de cambiar un modelo
uvicorn app.main:app --reload               # http://localhost:8000
```

No hay linter configurado.

## Arquitectura

- **Las rutas (`app/rutas/`) no tienen lógica.** Leen el pedido, llaman a un servicio y renderizan una plantilla. Toda la lógica vive en `app/servicios/`, porque en la fase 6 un servidor MCP va a reutilizar esos servicios.
- **Aislamiento por usuario:** cada función de servicio recibe `usuario_id` de forma explícita y filtra por él. Si el recurso no existe o es de otro usuario, `obtener` lanza `NoEncontrado` (`app/servicios/errores.py`); a propósito, no distingue los dos casos. `app/main.py` convierte esa excepción en un 404. Cada servicio nuevo necesita tests que intenten leer, editar y borrar datos de otro usuario.
- **Usuario actual:** las rutas lo obtienen con `Depends(usuario_actual)` (`app/dependencias.py`). Por ahora es un stub que devuelve o crea `demo@cursada.local`. C1 lo va a reemplazar por la cookie firmada sin cambiar su firma.
- **Modelos:** cada recurso tiene una clase tabla (`Materia`) y una clase de entrada validada (`MateriaDatos`), que recibe el servicio. Los modelos nuevos se importan en `app/modelos/__init__.py` para que Alembic y los tests los registren.
- **Formularios + HTMX:** las rutas leen el form a mano y lo validan con `MateriaDatos`. Si hay errores, re-renderizan el formulario con status 422. `base.html` configura `htmx.config.responseHandling` para que HTMX haga el swap de los 422. Para que la respuesta reemplace otro elemento se usan los headers `HX-Retarget`/`HX-Reswap` o `hx-swap-oob` (ver `POST /materias` y `_creada.html`). Los fragmentos que devuelve HTMX son las plantillas que empiezan con `_`.

## Base de datos y migraciones

- La URL viene de `DATABASE_URL` (`.env`, leída por `app/config.py`). `alembic.ini` deja la URL vacía, así que `alembic/env.py` toma la de la app y usa `render_as_batch=True` para que los ALTER funcionen en SQLite.
- `tests/test_migraciones.py` corre `alembic upgrade head` + `alembic check` sobre una base temporal. Si cambiás un modelo sin generar la migración, ese test falla.
- Los demás tests usan SQLite en memoria creado con `create_all` (`tests/conftest.py`). La fixture `client` sobreescribe `get_session` y `usuario_actual` para que el usuario logueado sea `usuario_a`.
