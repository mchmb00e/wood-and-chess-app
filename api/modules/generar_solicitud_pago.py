import requests
from sessions.database import get_db_connection # Importamos la nueva función
from sessions.env import getenv
from scripts.utils import generate_signature_payment

FLOW_URL = "https://sandbox.flow.cl/api/payment/create"

def generar_solicitud_pago(pedido_id: int):
    """
    Genera una solicitud en Flow y actualiza el pedido.
    Retorna: (url_pago, token) o (None, None)
    """
    conn = None
    cursor = None

    try:
        # 1. Abrimos conexión fresca para leer los datos
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT P.PED_PTOTAL, U.USU_EMAIL
            FROM PEDIDO P
            INNER JOIN USUARIO U ON P.PED_USURUT = U.USU_RUT
            WHERE P.PED_ID = %s
            """,
            (pedido_id,)
        )
        data_pedido = cursor.fetchone()

        if not data_pedido:
            print("Pedido no encontrado (o quizás no existe para ese RUT)")
            return None, None

        monto = int(data_pedido['PED_PTOTAL'])
        email = data_pedido['USU_EMAIL']

        # 2. Preparar parámetros para el "Flow Violento" 🎵
        params = {
            "apiKey": getenv('FLOW_API_KEY'),
            "commerceOrder": str(pedido_id),
            "subject": f"Wood&Chess Orden N° {pedido_id}",
            "currency": "CLP",
            "amount": monto,
            "email": email,
            "paymentMethod": 9,
            "urlConfirmation": f"{getenv('BACK_URL')}/api/pedido/confirmar",
            "urlReturn": f"{getenv('FRONT_URL')}/confirmacion?i={pedido_id}"
        }

        # 3. Firmar la petición
        params["s"] = generate_signature_payment(params, getenv('FLOW_SECRET_KEY'))

        # 4. Enviar a Flow (OJO: Agregué timeout=20s para que no se pegue)
        try:
            response = requests.post(FLOW_URL, data=params, timeout=20)
            resultado_flow = response.json()
        except requests.exceptions.Timeout:
            print("Error: Flow se demoró mucho en responder.")
            return None, None

        if "token" not in resultado_flow:
            print(f"Error Flow: {resultado_flow}")
            return None, None

        token = resultado_flow["token"]
        url_base = resultado_flow["url"]
        
        # Construimos la URL final donde mandamos al usuario
        url_pago = f"{url_base}?token={token}"

        # 5. Actualizar BD con el token recibido
        # Esto es clave para luego validar el pago cuando el usuario vuelva
        cursor.execute(
            "UPDATE PEDIDO SET PED_TOKEN = %s WHERE PED_ID = %s",
            (token, pedido_id)
        )
        conn.commit()

        # 6. Retornar el par solicitado, todo listo pa' la venta
        return url_pago, token

    except Exception as e:
        # Si falla algo (base de datos o lógica), hacemos rollback
        if conn:
            conn.rollback()
        print(f"Error generando solicitud pago: {e}")
        return None, None
        
    finally:
        # 7. Cerramos el boliche
        if cursor:
            cursor.close()
        if conn:
            conn.close()