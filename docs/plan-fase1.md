# Plan fase 1: esqueleto + CRUD de materias (M1, M2)

> Documento de trabajo temporal. Se marca cada paso al completarlo y se elimina cuando se confirma que la fase terminó.

## Contexto

Armamos el esqueleto que define `DISENO.md` (FastAPI + Jinja2 + HTMX + SQLModel + Alembic + pytest) y la primera funcionalidad: crear, editar y eliminar materias (M1) con links a Drive y Moodle (M2). Todo con tests.

**Usuario actual: stub reemplazable.** Los servicios reciben `usuario_id`, así que el aislamiento entre usuarios (C2) ya se puede testear. Las rutas obtienen el usuario con la dependencia `usuario_actual`, que por ahora devuelve un usuario demo. Cuando llegue C1, se reemplaza solo esa dependencia.

**Reglas de trabajo:** un commit al final de cada paso, con un mensaje de una oración. En el paso 5, `CLAUDE.md` se genera con `/init` y se deja así, porque lo edita Lauti.

## Pasos

### 1. Base del proyecto
- [x] `pyproject.toml`. Dependencias: fastapi, uvicorn[standard], sqlmodel, jinja2, python-multipart, alembic y pydantic-settings. En dev: pytest y httpx
- [x] `.gitignore` (`.venv/`, `*.egg-info/`, `.pytest_cache/`) y `.env.example`
- [x] `app/main.py` (`GET /` redirige con 303 a `/materias`), `app/config.py` y `app/db.py`
- [x] Test de humo: `GET /` → 303 a `/materias`
- [x] Commit

### 2. Modelos, migraciones y DISENO
- [x] `app/modelos/usuario.py` y `app/modelos/materia.py` (`Materia` + `MateriaDatos`)
- [x] Alembic: `alembic.ini` y `env.py` (`SQLModel.metadata`, `render_as_batch=True`, URL desde la config)
- [x] Migración `0001_usuarios_y_materias`
- [x] `tests/test_migraciones.py`: `upgrade head` y después `alembic check` sin diferencias
- [x] `DISENO.md` §3: aclarar que `anio` es el año calendario y que `cuatrimestre` puede ser 1, 2 o anual
- [x] Commit

### 3. Servicio de materias (tests primero)
- [ ] `tests/conftest.py`: SQLite en memoria (`StaticPool`) y fixtures `session`, `usuario_a` y `usuario_b`
- [ ] `tests/test_servicio_materias.py` escrito y fallando
- [ ] `app/servicios/errores.py` (`NoEncontrado`) y `app/servicios/materias.py` → tests en verde
- [ ] Commit

### 4. Rutas y plantillas
- [ ] `app/dependencias.py`: stub `usuario_actual` (busca o crea `demo@cursada.local`)
- [ ] Fixture `client` con overrides de `get_session` y `usuario_actual`
- [ ] `tests/test_rutas_materias.py` escrito y fallando
- [ ] `app/rutas/materias.py` + handler 404 para `NoEncontrado`
- [ ] Plantillas (`base.html`, `materias/lista.html`, `_tarjeta.html`, `_formulario.html`, `ficha.html`) y `estilos.css` → tests en verde
- [ ] Commit

### 5. Documentación
- [ ] `README.md`: cómo arrancar
- [ ] `DISENO.md` §4: sumar `GET /materias/{id}/editar`
- [ ] Commit
- [ ] Generar `CLAUDE.md` con `/init` y **parar** (lo edita Lauti)

### 6. Cierre
- [ ] Verificación manual en el navegador (ver abajo)
- [ ] Lauti confirma que la fase terminó → eliminar este archivo

## Detalle

### Modelo `Materia`
Campos: id, usuario_id (FK, indexado) y nombre (obligatorio, 1 a 100 caracteres). **anio**: año calendario en que se cursa (por ejemplo, 2026), entero entre 2000 y 2100. **cuatrimestre**: `"1"`, `"2"` o `"anual"`. Además: docente (opcional), link_drive y link_moodle (opcionales, deben empezar con http:// o https://) y archivada (bool, default False; sin funcionalidad hasta M4). Los strings vacíos que llegan del formulario se guardan como `None`.

### Servicio `app/servicios/materias.py`
Todas las funciones reciben `usuario_id`:
- `listar`: solo las activas, ordenadas por año descendente, cuatrimestre y nombre
- `crear`
- `obtener`: lanza `NoEncontrado` si la materia no existe **o es de otro usuario**
- `editar` y `eliminar`: usan `obtener`

### Rutas (sin lógica)
| Método | Ruta | Respuesta |
| --- | --- | --- |
| GET | `/` | Redirige (303) a `/materias` |
| GET | `/materias` | Página: tarjetas + formulario de nueva materia |
| POST | `/materias` | Fragmento `_tarjeta.html` |
| GET | `/materias/{id}` | Ficha básica: datos y links |
| GET | `/materias/{id}/editar` | Fragmento del formulario precargado |
| PUT | `/materias/{id}` | Fragmento de la tarjeta actualizada |
| DELETE | `/materias/{id}` | Respuesta vacía |

`NoEncontrado` → 404. Si la validación falla: 422 con el formulario y los errores (HTMX configurado con `responseHandling` para hacer el swap). HTMX se carga con versión fija: `htmx.org@2.0.4`.

### Tests
- **Servicio:** CRUD, orden del listado y aislamiento (usuario_b no ve ni modifica las materias de usuario_a). Validación: nombre vacío, cuatrimestre `"3"` inválido y `"anual"` válido, anio fuera de rango, link sin http y links vacíos → `None`.
- **Rutas:** la lista muestra solo las propias, POST válido e inválido (422), la ficha muestra los links, PUT y DELETE funcionan, una materia ajena da 404 y `/` redirige.
- **Migraciones:** `alembic check` sin diferencias entre modelos y migraciones.

## Verificación

```powershell
.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
pytest -v
alembic upgrade head
uvicorn app.main:app --reload
```

En http://localhost:8000: comprobar que `/` lleva a `/materias`. Crear una materia anual y otra del 2.º cuatrimestre, ambas con links. Editar, abrir la ficha, eliminar y enviar un formulario inválido.
