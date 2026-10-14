from app.modelos import Materia, MateriaDatos
from app.servicios import materias

FORMULARIO = {
    "nombre": "Redes",
    "anio": "2026",
    "cuatrimestre": "2",
    "docente": "Pérez",
    "link_drive": "https://drive.google.com/drive/folders/abc",
    "link_moodle": "https://moodle.ucc.edu.ar/course/view.php?id=1",
}


def crear(session, usuario, **cambios) -> Materia:
    return materias.crear(session, usuario.id, MateriaDatos(**(FORMULARIO | cambios)))


def test_lista_muestra_solo_materias_propias(client, session, usuario_a, usuario_b):
    crear(session, usuario_a, nombre="Redes")
    crear(session, usuario_b, nombre="Química de Beto")

    respuesta = client.get("/materias")

    assert respuesta.status_code == 200
    assert "Redes" in respuesta.text
    assert "Química de Beto" not in respuesta.text


def test_lista_vacia(client):
    respuesta = client.get("/materias")

    assert respuesta.status_code == 200
    assert "Todavía no cargaste materias" in respuesta.text


def test_crear_materia(client, session, usuario_a):
    respuesta = client.post("/materias", data=FORMULARIO)

    assert respuesta.status_code == 200
    assert "Redes" in respuesta.text
    assert 'hx-swap-oob="true"' in respuesta.text  # el formulario vuelve vacío
    [creada] = materias.listar(session, usuario_a.id)
    assert creada.link_moodle == FORMULARIO["link_moodle"]


def test_crear_materia_invalida_devuelve_formulario_con_errores(client, session, usuario_a):
    respuesta = client.post("/materias", data=FORMULARIO | {"nombre": "", "link_drive": "drive.com"})

    assert respuesta.status_code == 422
    assert "Ingresá un nombre" in respuesta.text
    assert "http:// o https://" in respuesta.text
    assert materias.listar(session, usuario_a.id) == []


def test_ficha_muestra_datos_y_links(client, session, usuario_a):
    materia = crear(session, usuario_a)

    respuesta = client.get(f"/materias/{materia.id}")

    assert respuesta.status_code == 200
    assert "Pérez" in respuesta.text
    assert FORMULARIO["link_drive"] in respuesta.text
    assert "https://moodle.ucc.edu.ar/course/view.php?id=1" in respuesta.text.replace("&amp;", "&")


def test_formulario_de_edicion_precargado(client, session, usuario_a):
    materia = crear(session, usuario_a, nombre="Sistemas Operativos")

    respuesta = client.get(f"/materias/{materia.id}/editar")

    assert respuesta.status_code == 200
    assert 'value="Sistemas Operativos"' in respuesta.text


def test_editar_materia(client, session, usuario_a):
    materia = crear(session, usuario_a)

    respuesta = client.put(
        f"/materias/{materia.id}", data=FORMULARIO | {"nombre": "Redes II", "cuatrimestre": "anual"}
    )

    assert respuesta.status_code == 200
    assert "Redes II" in respuesta.text
    session.refresh(materia)
    assert materia.nombre == "Redes II"
    assert materia.cuatrimestre == "anual"


def test_editar_materia_invalida(client, session, usuario_a):
    materia = crear(session, usuario_a)

    respuesta = client.put(f"/materias/{materia.id}", data=FORMULARIO | {"anio": "1990"})

    assert respuesta.status_code == 422
    assert "entre 2000 y 2100" in respuesta.text
    session.refresh(materia)
    assert materia.anio == 2026


def test_eliminar_materia(client, session, usuario_a):
    materia = crear(session, usuario_a)

    respuesta = client.delete(f"/materias/{materia.id}")

    assert respuesta.status_code == 200
    assert materias.listar(session, usuario_a.id) == []


def test_materia_de_otro_usuario_da_404(client, session, usuario_b):
    ajena = crear(session, usuario_b, nombre="Química de Beto")

    assert client.get(f"/materias/{ajena.id}").status_code == 404
    assert client.get(f"/materias/{ajena.id}/editar").status_code == 404
    assert client.put(f"/materias/{ajena.id}", data=FORMULARIO).status_code == 404
    assert client.delete(f"/materias/{ajena.id}").status_code == 404
    assert materias.obtener(session, usuario_b.id, ajena.id).nombre == "Química de Beto"


def test_materia_inexistente_da_404(client):
    assert client.get("/materias/999").status_code == 404
