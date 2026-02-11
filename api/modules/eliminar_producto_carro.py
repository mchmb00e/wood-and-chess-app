from sessions.database import get_db_connection

def eliminar_producto_carro(prod_id: int, usuario_rut: int) -> int:
    """
    Elimina UNA sola instancia de un producto específico para un usuario.
    Retorna la cantidad restante de ese producto o -1 si hay error.
    """
    conn = None
    cursor = None
    
    try:
        # 1. Abrimos conexión nueva
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 2. Eliminamos solo UNA instancia (LIMIT 1)
        query_delete = """
            DELETE FROM CARRO 
            WHERE CAR_PRODID = %s AND CAR_USURUT = %s 
            LIMIT 1
        """
        cursor.execute(query_delete, (prod_id, usuario_rut))
        
        # Si no borró nada (rowcount == 0), es que el producto no estaba
        if cursor.rowcount == 0:
            return -1
            
        # 3. Confirmamos la eliminación (Commit)
        conn.commit()
        
        # 4. Contamos cuántos quedan para actualizar la UI del usuario
        query_count = """
            SELECT COUNT(*) as cantidad 
            FROM CARRO 
            WHERE CAR_PRODID = %s AND CAR_USURUT = %s
        """
        cursor.execute(query_count, (prod_id, usuario_rut))
        resultado = cursor.fetchone()
        
        return resultado["cantidad"]

    except Exception as e:
        print(f"Error al eliminar: {e}")
        # 5. Rollback por si las moscas
        if conn:
            conn.rollback() 
        return -1
        
    finally:
        # 6. Limpieza final
        if cursor:
            cursor.close()
        if conn:
            conn.close()