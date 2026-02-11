from sessions.database import connection
from sessions.env import getenv
from scripts.utils import getextension, save_file
import os

def modificar_material(id_material, nombre, descripcion, previsualizacion, diffuse, normal, rough):
    cursor = connection.cursor()
    base = getenv("BASE_ARCHIVO")

    if not descripcion:
        descripcion = None

    try:
        query_update_info = """
            UPDATE MATERIAL
            SET MAT_NOMBRE = %s,
                MAT_DESC = %s
            WHERE MAT_ID = %s
        """
        cursor.execute(query_update_info, (nombre, descripcion, id_material))

        query_select_old = """
            SELECT MAT_IMAGEN, MAT_RDIFFUSE, MAT_RNORMAL, MAT_RROUGH
            FROM MATERIAL
            WHERE MAT_ID = %s
        """
        cursor.execute(query_select_old, (id_material,))
        old_files = cursor.fetchone()

        if old_files:
            for ruta_antigua in old_files:
                if ruta_antigua:
                    ruta_completa = os.path.join(base, ruta_antigua)
                    if os.path.exists(ruta_completa):
                        os.remove(ruta_completa)

        ext_prev = getextension(previsualizacion.filename)
        ext_diff = getextension(diffuse.filename)
        ext_norm = getextension(normal.filename)
        ext_roug = getextension(rough.filename)

        ruta_new_prev = f"matimg/{id_material}.{ext_prev}"
        ruta_new_diff = f"tex/diffuse/{id_material}_d.{ext_diff}"
        ruta_new_norm = f"tex/normal/{id_material}_n.{ext_norm}"
        ruta_new_rough = f"tex/rough/{id_material}_r.{ext_roug}"

        query_update_paths = """
            UPDATE MATERIAL
            SET MAT_IMAGEN = %s,
                MAT_RDIFFUSE = %s,
                MAT_RNORMAL = %s,
                MAT_RROUGH = %s
            WHERE MAT_ID = %s
        """
        cursor.execute(query_update_paths, (ruta_new_prev, ruta_new_diff, ruta_new_norm, ruta_new_rough, id_material))

        save_file(previsualizacion, os.path.join(base, ruta_new_prev))
        save_file(diffuse, os.path.join(base, ruta_new_diff))
        save_file(normal, os.path.join(base, ruta_new_norm))
        save_file(rough, os.path.join(base, ruta_new_rough))

        connection.commit()
        return True

    except Exception as e:
        print(f"Error al modificar material: {e}")
        return False
    finally:
        cursor.close()