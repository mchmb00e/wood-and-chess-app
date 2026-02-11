import requests
from sessions.env import getenv
from scripts.utils import generate_signature_payment

# Endpoint para consultar estado en Sandbox
FLOW_STATUS_URL = "https://sandbox.flow.cl/api/payment/getStatus"

def consultar_estado_flow(token: str) -> dict:
    """
    Consulta a Flow el estado real de un pago usando su token.
    Retorna un diccionario con la info del pago (status, commerceOrder, etc.)
    o None si falla la conexión.
    """
    try:
        # 1. Preparar parámetros básicos
        params = {
            "apiKey": getenv('FLOW_API_KEY'),
            "token": token
        }

        # 2. Generar la firma usando tu utilidad existente
        # Flow exige que la petición de estado también vaya firmada
        params["s"] = generate_signature_payment(params, getenv('FLOW_SECRET_KEY'))

        # 3. Hacer la consulta GET a Flow
        # GET https://sandbox.flow.cl/api/payment/getStatus?apiKey=...&token=...&s=...
        response = requests.get(FLOW_STATUS_URL, params=params)
        
        # 4. Procesar respuesta
        if response.status_code != 200:
            print(f"Error Flow API ({response.status_code}): {response.text}")
            return None
            
        data = response.json()
        
        return data

    except Exception as e:
        print(f"Excepción conectando con Flow: {e}")
        return None