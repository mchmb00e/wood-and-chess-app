from sessions.database import get_db_connection

def consultar_pedido(pedido_id: int, usuario_rut: int, rol: str) -> dict:
    """
    Consulta los detalles de un pedido.
    """
    conn = None
    cursor = None
    try:
        # 1. Iniciamos la conexión fresca
        conn = get_db_connection()
        cursor = conn.cursor()

        # 2. Verificar acceso: el Admin es el "Easykid" del sistema y ve todo, 
        # el usuario solo lo suyo por seguridad.
        if rol == "ADM":
            cursor.execute(
                """
                SELECT P.*, U.USU_NOMBRE, U.USU_RUT, U.USU_EMAIL, U.USU_TELEF
                FROM PEDIDO P
                INNER JOIN USUARIO U ON P.PED_USURUT = U.USU_RUT
                WHERE P.PED_ID = %s
                """,
                (pedido_id,)
            )
        else:
            cursor.execute(
                """
                SELECT P.*, U.USU_NOMBRE, U.USU_RUT, U.USU_EMAIL, U.USU_TELEF
                FROM PEDIDO P
                INNER JOIN USUARIO U ON P.PED_USURUT = U.USU_RUT
                WHERE P.PED_ID = %s AND P.PED_USURUT = %s
                """,
                (pedido_id, usuario_rut)
            )
        
        pedido = cursor.fetchone()
        
        if not pedido:
            return None
        
        # 3. Consultamos los productos asociados a ese pedido
        cursor.execute(
            """
            SELECT PP.*, PR.PROD_NOMBRE
            FROM PEDIDO_PRODUCTO PP
            INNER JOIN PRODUCTO PR ON PP.PEPR_PRODID = PR.PROD_ID
            WHERE PP.PEPR_PEDID = %s
            """,
            (pedido_id,)
        )
        productos_db = cursor.fetchall()
        
        productos = []
        for prod in productos_db:
            personalizado = prod["PEPR_MATPRI"] is not None
            productos.append({
                "id": prod["PEPR_PRODID"],
                "nombre": prod["PROD_NOMBRE"],
                "cantidad": 1, # Asumido 1 según la estructura actual de tu tabla intermedia
                "personalizado": personalizado,
                "materiales": [
                    prod["PEPR_MATPRI"],
                    prod["PEPR_MATSEC"],
                    prod["PEPR_MATTER"],
                    prod["PEPR_MATCUAT"]
                ]
            })
        
        retiro_en_tienda = pedido["PED_CALLE"] is None
        
        # 4. Armamos el objeto de respuesta final
        resultado = {
            "id": pedido["PED_ID"],
            "cliente": {
                "nombre": pedido["USU_NOMBRE"],
                "rut": str(pedido["USU_RUT"]),
                "email": pedido["USU_EMAIL"],
                "telefono": pedido["USU_TELEF"]
            },
            "estado": pedido["PED_ESTADO"],
            "retiro_en_tienda": retiro_en_tienda,
            "productos": productos
        }
        
        if not retiro_en_tienda:
            resultado["envio"] = {
                "calle": pedido["PED_CALLE"],
                "numero": pedido["PED_NUMERO"],
                "comuna": pedido["PED_COMUNA"],
                "region": pedido["PED_REGION"],
                "indicaciones": pedido["PED_INDEXTRA"]
            }
        
        return resultado

    except Exception as e:
        print(f"Error consultando pedido: {e}")
        return None
        
    finally:
        # 5. Cerramos cursor y conexión para que el server no transpire de más
        if cursor:
            cursor.close()
        if conn:
            conn.close()