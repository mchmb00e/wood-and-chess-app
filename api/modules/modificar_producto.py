from sessions.database import get_db_connection # Importamos la nueva función
from sessions.env import getenv
from scripts.utils import getextension, save_file
import os

def modificar_producto(id_producto, nombre, descripcion, stock, precio, lista_imagenes):
    """
    Actualiza la información de un producto y reemplaza sus imágenes.
    """
    conn = None
    cursor = None
    base = getenv("BASE_ARCHIVO")

    if not descripcion:
        descripcion = None

    try:
        # 1. Iniciamos conexión y transacción
        conn = get_db_connection()
        cursor = conn.cursor()

        # 2. Actualizamos los datos básicos del producto
        query_update = """
            UPDATE PRODUCTO
            SET PROD_NOMBRE = %s,
                PROD_DESC = %s,
                PROD_STOCK = %s,
                PROD_PRECIO = %s
            WHERE PROD_ID = %s
        """
        cursor.execute(query_update, (nombre, descripcion, stock, precio, id_producto))

        # 3. Gestionamos las imágenes antiguas
        # Primero buscamos las rutas para borrarlas físicamente
        cursor.execute(
            "SELECT IMA_RUTA FROM IMAGEN WHERE IMA_PRODID = %s",
            (id_producto,)
        )
        # CORRECCIÓN: fetchall() devuelve una lista de diccionarios
        eliminar_imagenes = cursor.fetchall()

        for fila in eliminar_imagenes:
            ruta_antigua = fila["IMA_RUTA"]
            ruta_completa = os.path.join(base, ruta_antigua)
            if os.path.exists(ruta_completa):
                os.remove(ruta_completa)

        # Borramos los registros antiguos de la tabla IMAGEN
        cursor.execute(
            "DELETE FROM IMAGEN WHERE IMA_PRODID = %s",
            (id_producto,)
        )

        # 4. Insertamos las nuevas imágenes
        for i, imagen in enumerate(lista_imagenes):
            principal = 1 if i == 0 else 0
            extension = getextension(imagen.filename)
            
            # Generamos un nombre de archivo único basado en el ID y el índice
            ruta_imagen = f"producto/{id_producto}_{i+1}.{extension}"

            query_insert = """
                INSERT INTO IMAGEN (IMA_PRODID, IMA_RUTA, IMA_PRINCIPAL)
                VALUES (%s, %s, %s)
            """
            cursor.execute(query_insert, (id_producto, ruta_imagen, principal))
            
            # Guardamos el archivo físico
            save_file(imagen, os.path.join(base, ruta_imagen))

        # 5. El momento de la verdad: Si todo salió bien, hacemos el commit
        conn.commit()
        return True

    except Exception as e:
        print(f"Error modificando producto {id_producto}: {e}")
        # Si algo falló, deshacemos cualquier cambio en la base de datos
        if conn:
            conn.rollback()
        return False

    finally:
        # 6. Cerramos los recursos para no dejar "fugas"
        if cursor:
            cursor.close()
        if conn:
            conn.close()