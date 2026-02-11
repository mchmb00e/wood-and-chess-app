from sessions.database import get_db_connection

def calcular_total_pedido(productos: list) -> int:
    """
    Calcula el total monetario de una lista de productos basándose en sus IDs.
    Recibe una lista de diccionarios: [{'id': 1, 'cantidad': 2}, ...]
    """
    # Si la lista está vacía, cortamos por lo sano al tiro
    if not productos:
        return 0

    conn = None
    cursor = None
    total = 0

    try:
        # 1. Abrimos la conexión fresca
        conn = get_db_connection()
        cursor = conn.cursor()

        # 2. Extraemos solo los IDs para hacer la consulta
        ids_productos = [p['id'] for p in productos]

        # 3. Generamos placeholders dinámicos
        # Tu lógica aquí estaba joya, la mantenemos tal cual
        placeholders = ', '.join(['%s'] * len(ids_productos))
        
        query = f"""
            SELECT PROD_ID, PROD_PRECIO 
            FROM PRODUCTO 
            WHERE PROD_ID IN ({placeholders})
        """

        # Ejecutamos pasando la lista de IDs como tupla
        cursor.execute(query, tuple(ids_productos))
        resultados = cursor.fetchall()

        # 4. Convertimos los resultados a diccionario para búsqueda rápida O(1)
        # Ojo: Asumimos que el cursor devuelve dicts (DictCursor) por tu config
        mapa_precios = {row['PROD_ID']: row['PROD_PRECIO'] for row in resultados}

        # 5. Calculamos el total
        for prod in productos:
            prod_id = prod['id']
            
            # Obtenemos precio (si no está, 0)
            precio_unitario = mapa_precios.get(prod_id, 0)
            
            # Cantidad por defecto 1 si no viene
            cantidad = prod.get('cantidad', 1)
            
            total += precio_unitario * cantidad

        return total

    except Exception as e:
        print(f"Error calculando total del pedido: {e}")
        return 0
        
    finally:
        # 6. Cerramos todo para no dejar conexiones colgadas
        if cursor:
            cursor.close()
        if conn:
            conn.close()