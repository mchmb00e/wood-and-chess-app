from sessions.database import connection
from sessions.env import getenv
from scripts.utils import getextension, save_file
import os

def crear_producto(nombre, descripcion, stock, precio, lista_imagenes):
    cursor = connection.cursor()
    base = getenv("BASE_ARCHIVO")

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

        connection.commit()
        return True
    except Exception as e:
        return False