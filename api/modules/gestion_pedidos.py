from sessions.database import get_db_connection

def obtener_productos_pedido(pedido_id: int) -> list:
    """
    Recupera los IDs de los productos asociados a un pedido.
    Equivalent to: SELECT PEPR_PRODID INTO productos_comprados
    """
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT PEPR_PRODID FROM PEDIDO_PRODUCTO WHERE PEPR_PEDID = %s",
            (pedido_id,)
        )
        
        # Guardamos el resultado en una variable antes de cerrar
        # Retorna una lista de IDs: [1, 5, 8...]
        lista_ids = [fila['PEPR_PRODID'] for fila in cursor.fetchall()]
        return lista_ids

    except Exception as e:
        print(f"Error obteniendo productos: {e}")
        return []

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def reducir_stock(lista_productos_ids: list):
    """
    Resta stock a los productos comprados.
    Equivalent to: Pro_ReducirStock(productos_comprados)
    """
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Restamos 1 al stock por cada producto en la lista
        # Ojo: Si el mismo ID viene 2 veces en la lista, se resta 2 veces.
        query_update = "UPDATE PRODUCTO SET PROD_STOCK = PROD_STOCK - 1 WHERE PROD_ID = %s AND PROD_STOCK > 0"
        
        for prod_id in lista_productos_ids:
            cursor.execute(query_update, (prod_id,))
            
            # Validación extra (opcional pero recomendada):
            # Si rowcount es 0, significa que no había stock o el producto no existe.
            # Podrías lanzar un error aquí para cancelar toda la venta si falta un producto.
        
        conn.commit()
        return True

    except Exception as e:
        # Si falla la resta de CUALQUIER producto, deshacemos TODO.
        # No queremos que se descuente el producto A si falló el descuento del producto B.
        if conn:
            conn.rollback()
        print(f"Error reduciendo stock: {e}")
        return False

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def continuar_estado_pedido(pedido_id: int):
    """
    Avanza el estado del pedido (ej: pago confirmado).
    Equivalent to: Pro_ContinuarEstadoPedido(id_pedido)
    """
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Asumimos que "Continuar" significa marcar como PAGADO/EN PREPARACIÓN
        cursor.execute(
            "UPDATE PEDIDO SET PED_ESTADO = 'En preparación' WHERE PED_ID = %s",
            (pedido_id,)
        )
        conn.commit()
        return True

    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Error actualizando estado: {e}")
        return False

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def eliminar_pedido(pedido_id: int):
    """
    Anula un pedido (Soft Delete).
    Equivalent to: Pro_EliminarPedido(id_pedido)
    """
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Mantenemos la OPCIÓN A (Soft Delete)
        # Es mucho mejor dejar el registro como 'Anulado' para que quede historial
        # de que hubo una intención de compra o un fallo en Flow.
        cursor.execute(
            "UPDATE PEDIDO SET PED_ESTADO = 'Anulado' WHERE PED_ID = %s",
            (pedido_id,)
        )
        
        conn.commit()
        return True

    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Error anulando pedido: {e}")
        return False

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()