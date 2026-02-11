from modules.listar_carro import listar_carro
# from modules.vaciar_carro import vaciar_carro  <-- OJO: Ya no la importamos, la haremos "in-house"
from modules.calcular_total_pedido import calcular_total_pedido
from scripts.utils import parse_cart
from sessions.database import get_db_connection  # Importamos la nueva función

datos_envio_none = {
    'calle': None,
    'numero': None,
    'comuna': None,
    'region': None,
    'indicaciones': None
}

def generar_pedido(rut: int, datos_envio: dict = datos_envio_none):
    # 1. Preparación de datos (Lecturas)
    # Esto puede ir fuera de la transacción de escritura
    items_carro = listar_carro(rut)
    productos = parse_cart(items_carro)
    
    # Validación simple
    if not productos:
        return None

    total = calcular_total_pedido(productos)

    conn = None
    cursor = None

    try:
        # 2. Iniciamos la transacción de escritura
        conn = get_db_connection()
        cursor = conn.cursor()

        # A. Insertar Cabecera del Pedido
        sql_pedido = """
            INSERT INTO PEDIDO (
                PED_USURUT, PED_ESTADO, PED_CALLE, PED_NUMERO, 
                PED_COMUNA, PED_REGION, PED_INDEXTRA, PED_PTOTAL, 
                PED_TOKEN, PED_FCREADO, PED_FACTUAL
            ) VALUES (
                %s, %s, %s, %s, 
                %s, %s, %s, %s, 
                %s, CURDATE(), CURDATE() 
            )
        """
        # Nota: Asumo que en tu tabla el estado 'Pendiente de pago' entra como string
        cursor.execute(sql_pedido, (
            rut,
            'Pendiente de pago',
            datos_envio.get('calle'),
            datos_envio.get('numero'),
            datos_envio.get('comuna'),
            datos_envio.get('region'),
            datos_envio.get('indicaciones'),
            total,
            None 
        ))
        
        # Recuperamos el ID generado
        id_pedido = cursor.lastrowid

        # B. Insertar Detalles (Productos)
        sql_detalle = """
            INSERT INTO PEDIDO_PRODUCTO (
                PEPR_PEDID, PEPR_PRODID, 
                PEPR_MATPRI, PEPR_MATSEC, PEPR_MATTER, PEPR_MATCUAT
            ) VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        for p in productos:
            cursor.execute(sql_detalle, (
                id_pedido,
                p["id"],
                p.get("mat1"), 
                p.get("mat2"),
                p.get("mat3"),
                p.get("mat4")
            ))
        
        # C. Vaciar el Carro (CRÍTICO: Hacerlo aquí mismo)
        # Al hacerlo con el mismo cursor, si falla el commit final, 
        # el carro NO se vacía. ¡Seguridad total!
        sql_vaciar = "DELETE FROM CARRO WHERE CAR_USURUT = %s"
        cursor.execute(sql_vaciar, (rut,))

        # D. El momento de la verdad: Commit
        conn.commit()
        
        return id_pedido

    except Exception as e:
        print(f"Error grave generando pedido: {e}")
        # Si algo falló (en el pedido, en los productos o al vaciar carro),
        # volvemos todo atrás como si nada hubiera pasado.
        if conn:
            conn.rollback()
        return None
        
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()