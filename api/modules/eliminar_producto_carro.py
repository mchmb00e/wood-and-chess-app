from sessions.database import connection

def eliminar_producto_carro(car_id: int, usuario_rut: int) -> int:
    """
    Elimina un producto del carro.
    Retorna la cantidad de registros restantes del mismo producto, o -1 si falla.
    """
    cursor = connection.cursor()
    try:
        cursor.execute(
            """
            SELECT CAR_PRODID
            FROM CARRO
            WHERE CAR_ID = %s AND CAR_USURUT = %s
            """,
            (car_id, usuario_rut)
        )
        registro = cursor.fetchone()
        
        if not registro:
            return -1
        
        prod_id = registro["CAR_PRODID"]
        
        cursor.execute(
            """
            DELETE FROM CARRO
            WHERE CAR_ID = %s AND CAR_USURUT = %s
            """,
            (car_id, usuario_rut)
        )
        connection.commit()
        
        cursor.execute(
            """
            SELECT COUNT(*) as cantidad
            FROM CARRO
            WHERE CAR_USURUT = %s AND CAR_PRODID = %s
            """,
            (usuario_rut, prod_id)
        )
        resultado = cursor.fetchone()
        return resultado["cantidad"]
    except Exception as e:
        return -1
    finally:
        cursor.close()