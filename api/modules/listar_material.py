from sessions.database import connection

def listar_materiales_3d(rol_usuario: str) -> list:
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(
            """
            SELECT *
            FROM MATERIAL
            WHERE 
                (%s = 'ADM') OR (%s = 'USR' AND MAT_DISP = 1)
            """,
            (rol_usuario, rol_usuario)
        )
        materiales = cursor.fetchall()
        
        return materiales

    except Exception as e:
        print(f"Error al listar materiales 3D: {e}")
        return []
    finally:
        cursor.close()