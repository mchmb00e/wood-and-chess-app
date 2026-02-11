from sessions.database import get_db_connection

def consultar_stock(producto_id: int) -> int:
    """
    Consulta el stock disponible de un producto específico.
    """
    conn = None
    cursor = None
    try:
        # 1. Abrimos conexión nueva
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = "SELECT PROD_STOCK FROM PRODUCTO WHERE PROD_ID = %s"
        cursor.execute(query, (producto_id,))
        
        # Como usamos DictCursor, el resultado es un diccionario
        resultado = cursor.fetchone()
        
        # Si existe el producto, devolvemos el stock; si no, 0
        return resultado["PROD_STOCK"] if resultado else 0

    except Exception as e:
        print(f"Error consultando stock del producto {producto_id}: {e}")
        return 0
        
    finally:
        # 2. Cerramos todo para no dejar la puerta abierta
        if cursor:
            cursor.close()
        if conn:
            conn.close()