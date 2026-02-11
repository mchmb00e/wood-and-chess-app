from sessions.database import connection
from sessions.env import getenv
from scripts.utils import getextension, save_file
import os

def crear_material(nombre, descripcion, previsualizacion, diffuse, normal, rough):
    cursor = connection.cursor()
    base = getenv("BASE_ARCHIVO")

    if not descripcion:
        descripcion = None

    try:
        query_insert = """
            INSERT INTO MATERIAL (MAT_NOMBRE, MAT_DESC, MAT_IMAGEN, MAT_DISP, MAT_RDIFFUSE, MAT_RNORMAL, MAT_RROUGH)
            VALUES (%s, %s, '', 1, '', '', '')
        """
        cursor.execute(query_insert, (nombre, descripcion))

        last_id = str(cursor.lastrowid)

        ext_prev = getextension(previsualizacion.filename)
        ext_diff = getextension(diffuse.filename)
        ext_norm = getextension(normal.filename)
        ext_roug = getextension(rough.filename)

        ruta_prev = f"matimg/{last_id}.{ext_prev}"
        ruta_diff = f"tex/diffuse/{last_id}_d.{ext_diff}"
        ruta_norm = f"tex/normal/{last_id}_n.{ext_norm}"
        ruta_roug = f"tex/rough/{last_id}_r.{ext_roug}"

        save_file(previsualizacion, os.path.join(base, ruta_prev))
        save_file(diffuse, os.path.join(base, ruta_diff))
        save_file(normal, os.path.join(base, ruta_norm))
        save_file(rough, os.path.join(base, ruta_roug))

        query_update = """
            UPDATE MATERIAL
            SET MAT_IMAGEN = %s,
                MAT_RDIFFUSE = %s,
                MAT_RNORMAL = %s,
                MAT_RROUGH = %s
            WHERE MAT_ID = %s
        """
        cursor.execute(query_update, (ruta_prev, ruta_diff, ruta_norm, ruta_roug, last_id))

        connection.commit()
        return True

    except Exception as e:
        print(f"Error al crear material: {e}")
        return False
    finally:
        cursor.close()