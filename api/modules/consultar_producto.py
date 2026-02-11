from sessions.database import get_db_connection

def consultar_producto(p_id_producto: int) -> dict:
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # 1. Datos básicos
        cursor.execute(
            "SELECT PROD_ID, PROD_NOMBRE, PROD_DESC, PROD_STOCK, PROD_PRECIO FROM PRODUCTO WHERE PROD_ID = %s",
            (p_id_producto,)
        )
        reg_producto = cursor.fetchone()
        if not reg_producto: return None

        # 2. Imágenes principales del producto
        cursor.execute("SELECT IMA_RUTA FROM IMAGEN WHERE IMA_PRODID = %s", (p_id_producto,))
        lista_imagenes = [fila["IMA_RUTA"] for fila in cursor.fetchall()]

        # 3. Comentarios del producto
        cursor.execute(
            "SELECT COM_ID, COM_CALIF, COM_TITULO, COM_DESC, COM_FECHA FROM COMENTARIO WHERE COM_PRODID = %s ORDER BY COM_FECHA DESC",
            (p_id_producto,)
        )
        filas_comentarios = cursor.fetchall()

        lista_comentarios = []
        for fila in filas_comentarios:
            com_id = fila["COM_ID"]
            
            # Buscamos las fotos de cada comentario
            cursor.execute("SELECT FOTO_RUTA FROM FOTOGRAFIA WHERE FOTO_COMID = %s", (com_id,))
            fotos_comentario = [f["FOTO_RUTA"] for f in cursor.fetchall()]

            # Mapeo según tu esquema exacto
            lista_comentarios.append({
                "id": com_id,
                "calificacion": fila["COM_CALIF"],
                "titulo": fila["COM_TITULO"],
                "descripcion": fila["COM_DESC"],
                "fecha": str(fila["COM_FECHA"]),
                "imagenes": fotos_comentario # Cambiado de 'fotografias' a 'imagenes'
            })

        # 4. Resultado final (JSON Match)
        return {
            "id": reg_producto["PROD_ID"],
            "nombre": reg_producto["PROD_NOMBRE"],
            "descripcion": reg_producto["PROD_DESC"], # Opcional en el esquema
            "precio": reg_producto["PROD_PRECIO"],
            "stock": reg_producto["PROD_STOCK"],
            "imagenes": lista_imagenes,
            "comentarios": lista_comentarios # Cambiado de 'resenas' a 'comentarios'
        }

    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        if cursor: cursor.close()
        if conn: conn.close()