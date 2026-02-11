from sessions.database import get_db_connection

def puede_comentar(usuario_rut: int, producto_id: int) -> bool:
    """
    Verifica si el usuario puede comentar un producto.
    Retorna True si el usuario compró el producto.
    """
    conn = None
    cursor = None
    try:
        # 1. Obtenemos una conexión fresca para esta consulta
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 2. Ejecutamos la validación de compra
        cursor.execute(
            """
            SELECT COUNT(*) as cantidad
            FROM PEDIDO P
            INNER JOIN PEDIDO_PRODUCTO PP ON P.PED_ID = PP.PEPR_PEDID
            WHERE P.PED_USURUT = %s AND PP.PEPR_PRODID = %s
            """,
            (usuario_rut, producto_id)
        )
        
        # Obtenemos el resultado (asumiendo DictCursor por la configuración previa)
        resultado = cursor.fetchone()
        
        # 3. Retornamos True si existe al menos un registro de compra
        return resultado["cantidad"] > 0
        
    except Exception as e:
        # Es recomendable registrar el error para facilitar el debugging
        print(f"Error al verificar permisos de comentario: {e}")
        return False
        
    finally:
        # 4. Cerramos recursos de forma segura
        if cursor:
            cursor.close()
        if conn:
            conn.close()