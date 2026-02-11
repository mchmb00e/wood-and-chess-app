from sessions.database import get_db_connection

def obtener_sesion(usuario_rut: int) -> dict:
    """
    Obtiene los datos del usuario en sesión.
    Retorna un diccionario con los datos o None si falla.
    """
    conn = None
    cursor = None
    
    try:
        # 1. Abrimos conexión fresca y dedicada
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """
            SELECT USU_RUT, USU_NOMBRE, USU_APELLIDO, USU_EMAIL, USU_ROL, USU_TELEF
            FROM USUARIO
            WHERE USU_RUT = %s
            """,
            (usuario_rut,)
        )
        usuario = cursor.fetchone()
        
        if not usuario:
            return None
        
        return {
            "rut": usuario["USU_RUT"],
            "nombre": usuario["USU_NOMBRE"],
            "apellido": usuario["USU_APELLIDO"],
            "email": usuario["USU_EMAIL"],
            "rol": usuario["USU_ROL"],
            "telefono": usuario["USU_TELEF"]
        }

    except Exception as e:
        print(f"Error obteniendo sesión: {e}")
        return None
        
    finally:
        # 2. Cerramos todo para no saturar el pool de conexiones
        if cursor:
            cursor.close()
        if conn:
            conn.close()