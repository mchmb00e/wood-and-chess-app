from sessions.database import connection

def vaciar_carro(usuario_rut: int) -> bool:
    """
    Vacía el carro de compras del usuario con rut usuario_rut.
    """
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM CARRO WHERE CAR_USURUT = %s", (usuario_rut,))
        connection.commit()
        return True
    except Exception as e:
        return False