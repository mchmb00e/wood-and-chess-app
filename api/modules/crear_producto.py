from sessions.database import get_db_connection # Importamos la función nueva
from sessions.env import getenv
from scripts.utils import getextension, save_file
import os

def crear_producto(nombre, descripcion, stock, precio, lista_imagenes):
    conn = None
    cursor = None
    base = getenv("BASE_ARCHIVO")

    if not descripcion:
        descripcion = None

    try:
        # 1. Iniciamos la conexión y transacción
        conn = get_db_connection()
        cursor = conn.cursor()

        # 2. Insertamos el producto
        query_prod = """
            INSERT INTO PRODUCTO (PROD_NOMBRE, PROD_DESC, PROD_STOCK, PROD_PRECIO)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query_prod, (nombre, descripcion, stock, precio))
        
        # Obtenemos el ID del producto recién creado
        last_id = str(cursor.lastrowid)

        # 3. Procesamos las imágenes
        for i, imagen in enumerate(lista_imagenes):
            principal = 1 if i == 0 else 0
            extension = getextension(imagen.filename)
            ruta_imagen = f"producto/{last_id}_{i+1}.{extension}"

            query_img = """
                INSERT INTO IMAGEN (IMA_PRODID, IMA_RUTA, IMA_PRINCIPAL)
                VALUES (%s, %s, %s)
            """
            cursor.execute(query_img, (last_id, ruta_imagen, principal))
            
            # Guardamos el archivo físico
            # Ojo: Si esto falla, saltará al except y hará rollback de la DB
            save_file(imagen, os.path.join(base, ruta_imagen))

        # 4. Si todo salió bien hasta aquí, confirmamos los cambios en la DB
        conn.commit()
        return True

    except Exception as e:
        print(f"Error creando producto: {e}")
        # 5. ¡Salvavidas! Si algo falla, deshacemos los cambios en la DB
        if conn:
            conn.rollback()
        return False

    finally:
        # 6. Cerramos el kiosco
        if cursor:
            cursor.close()
        if conn:
            conn.close()