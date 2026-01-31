from sessions.database import connection

def listar_carro(usuario_rut: int) -> list:
    """
    Lista los productos en el carro del usuario.
    """
    cursor = connection.cursor()
    try:
        cursor.execute(
            """
            SELECT C.CAR_ID, P.PROD_NOMBRE, P.PROD_DESC, P.PROD_PRECIO,
                   I.IMA_RUTA, C.CAR_MAT1, C.CAR_MAT2, C.CAR_MAT3, C.CAR_MAT4
            FROM CARRO C
            INNER JOIN PRODUCTO P ON C.CAR_PRODID = P.PROD_ID
            LEFT JOIN IMAGEN I ON P.PROD_ID = I.IMA_PRODID AND I.IMA_PRINCIPAL = 1
            WHERE C.CAR_USURUT = %s
            """,
            (usuario_rut,)
        )
        filas = cursor.fetchall()
        
        resultado = []
        for fila in filas:
            personalizado = fila["CAR_MAT1"] is not None
            resultado.append({
                "id": fila["CAR_ID"],
                "nombre": fila["PROD_NOMBRE"],
                "descripcion": fila["PROD_DESC"],
                "precio": fila["PROD_PRECIO"],
                "ruta": fila["IMA_RUTA"],
                "personalizado": personalizado,
                "materiales": [
                    fila["CAR_MAT1"],
                    fila["CAR_MAT2"],
                    fila["CAR_MAT3"],
                    fila["CAR_MAT4"]
                ]
            })
        return resultado
    except Exception as e:
        return []
    finally:
        cursor.close()