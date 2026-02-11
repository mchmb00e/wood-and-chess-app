from sessions.database import connection
from sessions.env import getenv
import os

def eliminar_material(id_material):
    cursor = connection.cursor()
    base = getenv("BASE_ARCHIVO")

    try:
        query_select = """
            SELECT MAT_IMAGEN, MAT_RDIFFUSE, MAT_RNORMAL, MAT_RROUGH
            FROM MATERIAL
            WHERE MAT_ID = %s
        """
        cursor.execute(query_select, (id_material,))
        archivos = cursor.fetchone()

        if archivos:
            for ruta_relativa in archivos:
                if ruta_relativa:
                    ruta_completa = os.path.join(base, ruta_relativa)
                    if os.path.exists(ruta_completa):
                        os.remove(ruta_completa)

        cursor.execute(
            "DELETE FROM MATERIAL WHERE MAT_ID = %s",
            (id_material,)
        )

        connection.commit()
        return True

    except Exception as e:
        print(f"Error al eliminar material: {e}")
        return False
    finally:
        cursor.close()