from sessions.database import connection

def consultar_material(id_material: int) -> dict:
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT * FROM MATERIAL WHERE MAT_ID = %s",
            (id_material,)
        )
        material = cursor.fetchone()
        
        return material

    except Exception as e:
        print(f"Error al consultar material: {e}")
        return None
    finally:
        cursor.close()