from sessions.database import connection

def agregar_producto_carro(usuario_rut: int, prod_id: int, mat1: int, mat2: int, mat3: int, mat4: int) -> int:
    """
    Agrega un producto al carro del usuario.
    Retorna la cantidad de registros del producto en el carro, o -1 si falla.
    """
    cursor = connection.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO CARRO (CAR_USURUT, CAR_PRODID, CAR_MAT1, CAR_MAT2, CAR_MAT3, CAR_MAT4)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (usuario_rut, prod_id, mat1, mat2, mat3, mat4)
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