from sessions.database import connection
from datetime import datetime

def modificar_estado_pedido(pedido_id: int, estado: str) -> bool:
    """
    Modifica el estado de un pedido.
    """
    cursor = connection.cursor()
    try:
        cursor.execute(
            """
            UPDATE PEDIDO
            SET PED_ESTADO = %s, PED_FACTUAL = %s
            WHERE PED_ID = %s
            """,
            (estado, datetime.now(), pedido_id)
        )
        connection.commit()
        return True
    except Exception as e:
        return False
    finally:
        cursor.close()