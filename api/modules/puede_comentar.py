from sessions.database import connection

def puede_comentar(usuario_rut: int, producto_id: int) -> bool:
    """
    Verifica si el usuario puede comentar un producto.
    Retorna True si el usuario compró el producto.
    """
    cursor = connection.cursor()
    try:
        cursor.execute(
            """
            SELECT COUNT(*) as cantidad
            FROM PEDIDO P
            INNER JOIN PEDIDO_PRODUCTO PP ON P.PED_ID = PP.PEPR_PEDID
            WHERE P.PED_USURUT = %s AND PP.PEPR_PRODID = %s
            """,
            (usuario_rut, producto_id)
        )
        resultado = cursor.fetchone()
        return resultado["cantidad"] > 0
    except Exception as e:
        return False
    finally:
        cursor.close()