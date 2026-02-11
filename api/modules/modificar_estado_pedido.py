from sessions.database import get_db_connection
from datetime import datetime

def modificar_estado_pedido(pedido_id: int, estado: str) -> bool:
    """
    Modifica el estado de un pedido y actualiza la fecha de última modificación.
    """
    conn = None
    cursor = None
    
    try:
        # 1. Conexión fresca
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 2. Actualizamos estado y fecha
        cursor.execute(
            """
            UPDATE PEDIDO
            SET PED_ESTADO = %s, PED_FACTUAL = %s
            WHERE PED_ID = %s
            """,
            (estado, datetime.now(), pedido_id)
        )
        
        # 3. Confirmamos el cambio
        conn.commit()
        return True

    except Exception as e:
        print(f"Error modificando estado pedido: {e}")
        # 4. Rollback por si las moscas
        if conn:
            conn.rollback()
        return False
        
    finally:
        # 5. Cerramos todo
        if cursor:
            cursor.close()
        if conn:
            conn.close()