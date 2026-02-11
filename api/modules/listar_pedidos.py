from sessions.database import get_db_connection

def listar_pedidos(usuario_rut: int, rol: str, buscar_id: int = None) -> list:
    """
    Lista los pedidos.
    Si es admin: todos los pedidos.
    Si es usuario: solo los suyos.
    """
    conn = None
    cursor = None
    
    try:
        # 1. Abrimos conexión nueva
        conn = get_db_connection()
        cursor = conn.cursor()

        if rol == "ADM":
            if buscar_id:
                cursor.execute(
                    """
                    SELECT PED_ID, PED_USURUT, PED_ESTADO, PED_PTOTAL, PED_FCREADO
                    FROM PEDIDO
                    WHERE PED_ID = %s
                    """,
                    (buscar_id,)
                )
            else:
                cursor.execute(
                    """
                    SELECT PED_ID, PED_USURUT, PED_ESTADO, PED_PTOTAL, PED_FCREADO
                    FROM PEDIDO
                    """
                )
        else:
            # Si es usuario normal, blindamos la consulta con su RUT
            if buscar_id:
                cursor.execute(
                    """
                    SELECT PED_ID, PED_USURUT, PED_ESTADO, PED_PTOTAL, PED_FCREADO
                    FROM PEDIDO
                    WHERE PED_USURUT = %s AND PED_ID = %s
                    """,
                    (usuario_rut, buscar_id)
                )
            else:
                cursor.execute(
                    """
                    SELECT PED_ID, PED_USURUT, PED_ESTADO, PED_PTOTAL, PED_FCREADO
                    FROM PEDIDO
                    WHERE PED_USURUT = %s
                    """,
                    (usuario_rut,)
                )
        
        filas = cursor.fetchall()
        
        resultado = []
        for fila in filas:
            resultado.append({
                "id": fila["PED_ID"],
                "usuario_rut": fila["PED_USURUT"],
                "estado": fila["PED_ESTADO"],
                "total": fila["PED_PTOTAL"],
                "fecha_creado": str(fila["PED_FCREADO"])
            })
        return resultado

    except Exception as e:
        print(f"Error al listar pedidos: {e}")
        return []
        
    finally:
        # 2. Cerramos el boliche
        if cursor:
            cursor.close()
        if conn:
            conn.close()