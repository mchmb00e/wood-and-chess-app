from sessions.database import connection

def obtener_rol(usuario_rut: int) -> str:
    """
    Obtiene el rol del usuario.
    Retorna 'ADM', 'USR' o None si no existe.
    """
    cursor = connection.cursor()
    try:
        cursor.execute(
            "SELECT USU_ROL FROM USUARIO WHERE USU_RUT = %s",
            (usuario_rut,)
        )
        usuario = cursor.fetchone()
        
        if usuario:
            return usuario["USU_ROL"]
        return None
    except Exception as e:
        return None
    finally:
        cursor.close()