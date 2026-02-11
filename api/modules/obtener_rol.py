from sessions.database import get_db_connection

def obtener_rol(usuario_rut: int) -> str:
    """
    Obtiene el rol del usuario.
    Retorna 'ADM', 'USR' o None si no existe.
    """
    conn = None
    cursor = None
    try:
        # 1. Abrimos conexión fresca
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT USU_ROL FROM USUARIO WHERE USU_RUT = %s",
            (usuario_rut,)
        )
        usuario = cursor.fetchone()
        
        if usuario:
            return usuario["USU_ROL"]
        return None

    except Exception as e:
        print(f"Error obteniendo rol: {e}")
        return None
        
    finally:
        # 2. Cerramos el boliche para liberar recursos
        if cursor:
            cursor.close()
        if conn:
            conn.close()