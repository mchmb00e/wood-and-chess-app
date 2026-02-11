from sessions.database import get_db_connection

def listar_carro(usuario_rut: int) -> list:
    """
    Lista los productos en el carro del usuario.
    """
    conn = None
    cursor = None
    
    try:
        # 1. Conexión fresca para lectura rápida
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT 
                C.CAR_ID, 
                C.CAR_PRODID, 
                P.PROD_NOMBRE, 
                P.PROD_DESC, 
                P.PROD_PRECIO,
                I.IMA_RUTA, 
                C.CAR_MAT1, 
                C.CAR_MAT2, 
                C.CAR_MAT3, 
                C.CAR_MAT4
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
            
            # Construimos el objeto tal cual lo necesita el frontend
            resultado.append({
                "id": fila["CAR_PRODID"], 
                "cart_id": fila["CAR_ID"], 
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
        print(f"Error al listar carro: {e}")
        return []
        
    finally:
        # 2. Cerramos todo
        if cursor:
            cursor.close()
        if conn:
            conn.close()