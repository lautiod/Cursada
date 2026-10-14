class NoEncontrado(Exception):
    """El recurso no existe o no pertenece al usuario.

    No se distinguen los dos casos para no revelar qué ids existen.
    """
