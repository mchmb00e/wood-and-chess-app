from sessions.database import get_db_connection
# Asumo que listar_productos está en el mismo archivo o lo importas
# from modules.productos import listar_productos 

def buscar_producto(busqueda: str, rol_usuario: str) -> list:
    """
    Busca productos por nombre.
    Si no hay búsqueda, lista todos según el rol.
    """
    if not busqueda:
        # Asegúrate que tu listar_productos ya use get_db_connection también
        from modules.listar_productos import listar_productos # Import local para evitar circular imports si aplica
        return listar_productos(rol_usuario)

    conn = None
    cursor = None
    try:
        # 1. Conexión fresca
        conn = get_db_connection()
        cursor = conn.cursor()

        # 2. Construcción de la query
        query = """
            SELECT 
                P.PROD_ID, 
                P.PROD_NOMBRE, 
                P.PROD_DESC, 
                P.PROD_PRECIO, 
                P.PROD_STOCK,
                I.IMA_RUTA
            FROM PRODUCTO P
            LEFT JOIN IMAGEN I ON P.PROD_ID = I.IMA_PRODID AND I.IMA_PRINCIPAL = 1
            WHERE P.PROD_NOMBRE LIKE %s
        """
        params = [f"%{busqueda}%"]

        # Filtro de seguridad para usuarios normales
        if rol_usuario != "ADM":
            query += " AND P.PROD_STOCK > 0"

        cursor.execute(query, tuple(params))
        filas = cursor.fetchall()
        
        # 3. Mapeo de resultados
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
        print(f"Error al buscar productos: {e}")
        return []
    finally:
        # 4. Cerramos el boliche
        if cursor:
            cursor.close()
        if conn:
            conn.close()