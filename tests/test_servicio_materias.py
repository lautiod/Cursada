import pytest
from pydantic import ValidationError

from app.modelos import MateriaDatos
from app.servicios import materias
from app.servicios.errores import NoEncontrado


def datos(**cambios) -> MateriaDatos:
    base = {
        "nombre": "Redes",
        "anio": 2026,
        "cuatrimestre": "2",
        "docente": "Pérez",
        "link_drive": "https://drive.google.com/drive/folders/abc",
        "link_moodle": "https://moodle.ucc.edu.ar/course/view.php?id=1",
    }
    return MateriaDatos(**(base | cambios))


# --- CRUD ---


def test_crear_y_listar(session, usuario_a):
    creada = materias.crear(session, usuario_a.id, datos())

    assert creada.id is not None
    assert creada.usuario_id == usuario_a.id
    assert creada.link_drive == "https://drive.google.com/drive/folders/abc"
    assert [m.id for m in materias.listar(session, usuario_a.id)] == [creada.id]


def test_listar_ordena_por_anio_desc_cuatrimestre_y_nombre(session, usuario_a):
    for nombre, anio, cuatri in [
        ("Física", 2025, "1"),
        ("Redes", 2026, "2"),
        ("Álgebra", 2026, "1"),
        ("Bases de datos", 2026, "1"),
        ("Inglés", 2026, "anual"),
    ]:
        materias.crear(session, usuario_a.id, datos(nombre=nombre, anio=anio, cuatrimestre=cuatri))

    nombres = [m.nombre for m in materias.listar(session, usuario_a.id)]

    # Los acentos no alteran el orden alfabético ("Álgebra" va antes que "Bases").
    assert nombres == ["Álgebra", "Bases de datos", "Redes", "Inglés", "Física"]


def test_listar_no_incluye_archivadas(session, usuario_a):
    materia = materias.crear(session, usuario_a.id, datos())
    materia.archivada = True
    session.commit()

    assert materias.listar(session, usuario_a.id) == []


def test_obtener(session, usuario_a):
    creada = materias.crear(session, usuario_a.id, datos())

    assert materias.obtener(session, usuario_a.id, creada.id).nombre == "Redes"


def test_obtener_inexistente(session, usuario_a):
    with pytest.raises(NoEncontrado):
        materias.obtener(session, usuario_a.id, 999)


def test_editar(session, usuario_a):
    creada = materias.crear(session, usuario_a.id, datos())

    editada = materias.editar(
        session,
        usuario_a.id,
        creada.id,
        datos(nombre="Redes de datos", cuatrimestre="anual", link_drive="", link_moodle="http://otro"),
    )

    assert editada.nombre == "Redes de datos"
    assert editada.cuatrimestre == "anual"
    assert editada.link_drive is None
    assert editada.link_moodle == "http://otro"
    assert materias.obtener(session, usuario_a.id, creada.id).nombre == "Redes de datos"


def test_eliminar(session, usuario_a):
    creada = materias.crear(session, usuario_a.id, datos())

    materias.eliminar(session, usuario_a.id, creada.id)

    assert materias.listar(session, usuario_a.id) == []
    with pytest.raises(NoEncontrado):
        materias.obtener(session, usuario_a.id, creada.id)


# --- Aislamiento entre usuarios (C2) ---


def test_un_usuario_no_ve_materias_de_otro(session, usuario_a, usuario_b):
    materias.crear(session, usuario_a.id, datos())

    assert materias.listar(session, usuario_b.id) == []


def test_un_usuario_no_obtiene_materia_de_otro(session, usuario_a, usuario_b):
    ajena = materias.crear(session, usuario_a.id, datos())

    with pytest.raises(NoEncontrado):
        materias.obtener(session, usuario_b.id, ajena.id)


def test_un_usuario_no_edita_materia_de_otro(session, usuario_a, usuario_b):
    ajena = materias.crear(session, usuario_a.id, datos())

    with pytest.raises(NoEncontrado):
        materias.editar(session, usuario_b.id, ajena.id, datos(nombre="Hackeada"))
    assert materias.obtener(session, usuario_a.id, ajena.id).nombre == "Redes"


def test_un_usuario_no_elimina_materia_de_otro(session, usuario_a, usuario_b):
    ajena = materias.crear(session, usuario_a.id, datos())

    with pytest.raises(NoEncontrado):
        materias.eliminar(session, usuario_b.id, ajena.id)
    assert materias.obtener(session, usuario_a.id, ajena.id) is not None


# --- Validación de los datos ---


@pytest.mark.parametrize("cuatrimestre", ["1", "2", "anual"])
def test_cuatrimestres_validos(cuatrimestre):
    assert datos(cuatrimestre=cuatrimestre).cuatrimestre == cuatrimestre


@pytest.mark.parametrize(
    "cambios",
    [
        {"nombre": ""},
        {"nombre": "   "},
        {"nombre": "x" * 101},
        {"cuatrimestre": "3"},
        {"anio": 1999},
        {"anio": 2101},
        {"link_drive": "drive.google.com/abc"},
        {"link_moodle": "ftp://moodle"},
    ],
)
def test_datos_invalidos(cambios):
    with pytest.raises(ValidationError):
        datos(**cambios)


def test_campos_opcionales_vacios_quedan_en_none():
    d = datos(docente="  ", link_drive="", link_moodle="")

    assert d.docente is None
    assert d.link_drive is None
    assert d.link_moodle is None


def test_nombre_se_guarda_sin_espacios_extremos():
    assert datos(nombre="  Redes  ").nombre == "Redes"
