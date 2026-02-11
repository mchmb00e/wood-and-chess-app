from sessions.database import get_db_connection
from sessions.env import getenv
import os

def eliminar_producto(id_producto):
    conn = None
    cursor = None
    base = getenv("BASE_ARCHIVO")

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # --- 1. PREPARAR RUTAS DE ARCHIVOS (Antes de borrar de la DB) ---
        
        # Fotos de los comentarios
        cursor.execute("""
            SELECT F.FOTO_RUTA FROM FOTOGRAFIA F
            INNER JOIN COMENTARIO C ON F.FOTO_COMID = C.COM_ID
            WHERE C.COM_PRODID = %s
        """, (id_producto,))
        fotos_comentarios = cursor.fetchall()

        # Imágenes del producto
        cursor.execute("SELECT IMA_RUTA FROM IMAGEN WHERE IMA_PRODID = %s", (id_producto,))
        imagenes_producto = cursor.fetchall()

        # --- 2. BORRAR REGISTROS DE TABLAS "HIJAS" (Evita FK Error) ---

        # A. Borrar de CARRO (donde te tiró el error antes)
        cursor.execute("DELETE FROM CARRO WHERE CAR_PRODID = %s", (id_producto,))

        # B. Borrar de PEDIDO_PRODUCTO (Historial de ventas)
        cursor.execute("DELETE FROM PEDIDO_PRODUCTO WHERE PEPR_PRODID = %s", (id_producto,))

        # C. Borrar FOTOGRAFIA (fotos de comentarios) y luego COMENTARIO
        # Primero las fotos por la FK en COMENTARIO
        cursor.execute("""
            DELETE F FROM FOTOGRAFIA F
            INNER JOIN COMENTARIO C ON F.FOTO_COMID = C.COM_ID
            WHERE C.COM_PRODID = %s
        """, (id_producto,))
        cursor.execute("DELETE FROM COMENTARIO WHERE COM_PRODID = %s", (id_producto,))

        # D. Borrar de IMAGEN
        cursor.execute("DELETE FROM IMAGEN WHERE IMA_PRODID = %s", (id_producto,))

        # --- 3. BORRAR EL PRODUCTO (El "Padre") ---
        cursor.execute("DELETE FROM PRODUCTO WHERE PROD_ID = %s", (id_producto,))

        # --- 4. BORRAR ARCHIVOS FÍSICOS ---
        # Si llegamos aquí sin errores, procedemos a borrar los archivos
        for fila in fotos_comentarios:
            ruta = os.path.join(base, fila["FOTO_RUTA"])
            if os.path.exists(ruta): os.remove(ruta)

        for fila in imagenes_producto:
            ruta = os.path.join(base, fila["IMA_RUTA"])
            if os.path.exists(ruta): os.remove(ruta)

        # 5. COMMIT: Si algo falló arriba, nada de esto se ejecuta
        conn.commit()
        return True

    except Exception as e:
        print(f"Error crítico eliminando producto {id_producto}: {e}")
        if conn:
            conn.rollback()
        return False

    finally:
        if cursor: cursor.close()
        if conn: conn.close()