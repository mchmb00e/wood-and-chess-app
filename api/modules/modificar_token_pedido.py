from sessions.database import get_db_connection

def modificar_token_pedido(id_pedido: int, token: str) -> bool:
    """
    Actualiza el token de un pedido existente.
    Retorna True si la operación fue exitosa, False si hubo error.
    """
    conn = None
    cursor = None
    
    try:
        # 1. Obtenemos conexión fresca
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 2. Ejecutamos el update
        sql = "UPDATE PEDIDO SET PED_TOKEN = %s WHERE PED_ID = %s"
        cursor.execute(sql, (token, id_pedido))
        
        # 3. Confirmamos cambios
        conn.commit()
        
        # Opcional: Verificar si realmente se actualizó alguna fila
        # if cursor.rowcount == 0:
        #     print(f"Advertencia: No se encontró el pedido {id_pedido}")
        
        return True
        
    except Exception as e:
        # 4. Si falla, rollback para no dejar basura
        if conn:
            conn.rollback()
        print(f"Error al modificar token del pedido: {e}")
        return False
        
    finally:
        # 5. Cerramos cursor y conexión
        if cursor:
            cursor.close()
        if conn:
            conn.close()