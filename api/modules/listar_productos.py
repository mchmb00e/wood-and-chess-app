from sessions.database import get_db_connection

def listar_productos(rol_usuario: str) -> list:
    conn = None
    cursor = None
    try:
        # 1. Abrimos conexión fresca "al tiro"
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT 
                P.PROD_ID, 
                P.PROD_NOMBRE, 
                P.PROD_DESC, 
                P.PROD_PRECIO, 
                P.PROD_STOCK,
                I.IMA_RUTA
            FROM PRODUCTO P
            LEFT JOIN IMAGEN I ON P.PROD_ID = I.IMA_PRODID AND I.IMA_PRINCIPAL = 1
            WHERE 
                (%s = 'ADM') OR (%s = 'USR' AND P.PROD_STOCK > 0)
            """,
            (rol_usuario, rol_usuario)
        )
        filas = cursor.fetchall()
        
        resultado = []
        for fila in filas:
            resultado.append({
                "id": fila["PROD_ID"],
                "nombre": fila["PROD_NOMBRE"],
                "descripcion": fila["PROD_DESC"],
                "precio": fila["PROD_PRECIO"],
                "stock": fila["PROD_STOCK"],
                "ruta": fila["IMA_RUTA"]
            })
        return resultado

    except Exception as e:
        print(f"Error listando productos: {e}")
        return []
        
    finally:
        # 2. Cerramos el kiosco para liberar recursos
        if cursor:
            cursor.close()
        if conn:
            conn.close()