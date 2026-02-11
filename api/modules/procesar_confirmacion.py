from modules.consultar_estado_flow import consultar_estado_flow
from modules.gestion_pedidos import (
    obtener_productos_pedido, 
    reducir_stock, 
    continuar_estado_pedido, 
    eliminar_pedido
)

def procesar_confirmacion_pago(token: str) -> bool:
    """
    Orquestador que consulta a Flow y actualiza el stock/estado del pedido.
    Implementación de Pro_ActualizarEstadoPago(p_token).
    """
    
    # 1. Consultamos el estado real en Flow
    # Esto es vital para evitar fraudes (que no nos pasen un token falso)
    consulta_estado = consultar_estado_flow(token)
    
    if not consulta_estado:
        print("Error: No se pudo verificar el estado con Flow.")
        return False

    # 2. Extraemos variables con seguridad
    id_pedido = consulta_estado.get('commerceOrder')
    estado_pago = consulta_estado.get('status') # 1: Pendiente, 2: Pagado, 3: Rechazado, 4: Anulado
    
    # Validamos que el ID sea un número
    try:
        id_pedido = int(id_pedido)
    except (ValueError, TypeError):
        print(f"Error: ID de pedido inválido recibido de Flow: {id_pedido}")
        return False

    print(f"Procesando Pedido {id_pedido} con Estado Flow {estado_pago}")

    # --- LÓGICA DE NEGOCIO ---

    # CASO 1: PENDIENTE
    if estado_pago == 1:
        # El pago aún no se completa. No hacemos cambios en DB.
        # Retornamos True porque la comunicación fue exitosa.
        return True

    # CASO 2: PAGADO (ÉXITO)
    elif estado_pago == 2:
        print(f"¡Pago confirmado para pedido {id_pedido}! Iniciando despacho digital...")
        
        # A. Recuperamos los productos para saber qué descontar
        productos_comprados = obtener_productos_pedido(id_pedido)
        
        if not productos_comprados:
            print(f"Advertencia: El pedido {id_pedido} figura pagado pero no tiene productos.")
            # Igual marcamos el pedido como 'pagado' para revisión manual
            continuar_estado_pedido(id_pedido)
            return True

        # B. Reducimos el stock (Crítico)
        exito_stock = reducir_stock(productos_comprados)
        
        if not exito_stock:
            print(f"Alerta Crítica: Falló la reducción de stock para pedido {id_pedido}")
            # Aquí podrías decidir si anular el pedido o marcarlo con un estado de "Error Stock"
            # Por ahora, seguimos para asegurar que el cliente vea su pedido confirmado.
        
        # C. Avanzamos el estado del pedido a 'En preparación'
        continuar_estado_pedido(id_pedido)
        return True

    # CASO 3: RECHAZADO O ANULADO
    elif estado_pago == 3 or estado_pago == 4:
        print(f"Pago rechazado/anulado para pedido {id_pedido}. Cancelando orden.")
        
        # Liberamos el pedido (Soft Delete)
        eliminar_pedido(id_pedido)
        return True

    # CASO: ESTADO DESCONOCIDO
    print(f"Estado desconocido recibido de Flow: {estado_pago}")
    return False