import os
import pymysql
from app.utilidades.archivos import getextension, save_file

def get_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='chess_store'
    )

def Pro_CrearMaterial(nombre, descripcion, previsualizacion, diffuse, rough, normal):
    conn = get_connection()
    cursor = conn.cursor()
    base = os.getenv("BASE_ARCHIVO", "static/uploads/")

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
        ext_rough = getextension(rough.filename)

        ruta_previsualizacion = f"matimg/{last_id}.{ext_prev}"
        ruta_diffuse = f"tex/diffuse/{last_id}_d.{ext_diff}"
        ruta_normal = f"tex/normal/{last_id}_n.{ext_norm}"
        ruta_rough = f"tex/rough/{last_id}_r.{ext_rough}"

        save_file(previsualizacion, os.path.join(base, ruta_previsualizacion))
        save_file(diffuse, os.path.join(base, ruta_diffuse))
        save_file(normal, os.path.join(base, ruta_normal))
        save_file(rough, os.path.join(base, ruta_rough))

        query_update = """
            UPDATE MATERIAL
            SET MAT_IMAGEN = %s,
                MAT_RDIFFUSE = %s,
                MAT_RNORMAL = %s,
                MAT_RROUGH = %s
            WHERE MAT_ID = %s
        """
        cursor.execute(query_update, (ruta_previsualizacion, ruta_diffuse, ruta_normal, ruta_rough, last_id))

        conn.commit()
        cursor.close()
        conn.close()
        return True

    except Exception as e:
        print(f"Error crítico en Pro_CrearMaterial: {e}")
        conn.rollback()
        cursor.close()
        conn.close()
        return False

def crear_producto(nombre, descripcion, stock, precio, lista_imagenes):
    conn = get_connection()
    cursor = conn.cursor()
    base = os.getenv("BASE_ARCHIVO", "static/uploads/")

    if not descripcion:
        descripcion = None

    try:
        query_prod = """
            INSERT INTO PRODUCTO (PROD_NOMBRE, PROD_DESC, PROD_STOCK, PROD_PRECIO)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query_prod, (nombre, descripcion, stock, precio))
        last_id = str(cursor.lastrowid)

        for i, imagen in enumerate(lista_imagenes):
            principal = 1 if i == 0 else 0
            extension = getextension(imagen.filename)
            ruta_imagen = f"producto/{last_id}_{i+1}.{extension}"

            query_img = """
                INSERT INTO IMAGEN (IMA_PRODID, IMA_RUTA, IMA_PRINCIPAL)
                VALUES (%s, %s, %s)
            """
            cursor.execute(query_img, (last_id, ruta_imagen, principal))
            save_file(imagen, os.path.join(base, ruta_imagen))

        conn.commit()
        cursor.close()
        conn.close()
        return True

    except Exception as e:
        print(f"Error crítico en Pro_CrearProducto: {e}")
        conn.rollback()
        cursor.close()
        conn.close()
        return False