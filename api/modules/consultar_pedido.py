from sessions.database import connection

def consultar_pedido(pedido_id: int, usuario_rut: int, rol: str) -> dict:
    """
    Consulta los detalles de un pedido.
    """
    cursor = connection.cursor()
    try:
        # Verificar acceso: admin ve todo, usuario solo los suyos
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
                "cantidad": 1,
                "personalizado": personalizado,
                "materiales": [
                    prod["PEPR_MATPRI"],
                    prod["PEPR_MATSEC"],
                    prod["PEPR_MATTER"],
                    prod["PEPR_MATCUAT"]
                ]
            })
        
        retiro_en_tienda = pedido["PED_CALLE"] is None
        
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
                "indicaciones": pedido["PED_INDEXTRA"]
            }
        
        return resultado
    except Exception as e:
        return None
    finally:
        cursor.close()