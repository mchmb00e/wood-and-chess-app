import os
import hmac
import hashlib

def generate_password_hash(password: str) -> str:
    """
    Generate a hashed password using bcrypt algorithm.\n
    bcrypt module is necessary (pip bcrypt).
    """
    from bcrypt import hashpw, gensalt
    pwd_byte = password.encode('utf-8')
    hashed = hashpw(pwd_byte, gensalt()).decode('utf-8')

    return hashed

def getextension(filename: str) -> str:
    """
    Obtiene la extensión de un archivo.
    """
    if '.' in filename:
        return filename.rsplit('.', 1)[1].lower()
    return ''

def save_file(file_obj, full_path: str) -> bool:
    """
    Guarda el archivo en la ruta física.
    """
    try:
        # Asegurar que el directorio existe
        directory = os.path.dirname(full_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
            
        file_obj.save(full_path)
        return True
    except Exception as e:
        print(f"Error guardando archivo en {full_path}: {e}")
        return False

def check_password_hash(pwd_plana: str, pwd_hash: str) -> bool:
    """
    Valida si dos contraseñas con válidas.
    """
    from bcrypt import checkpw

    pwd1_bytes = pwd_plana.encode('utf-8')
    pwd2_bytes = pwd_hash.encode('utf-8')

    validate = checkpw(pwd1_bytes, pwd2_bytes)

    return validate

def parse_cart(cart: list):
    products = []
    for product in cart:
        products.append({
            'id': product["id"],
            'mat1': product["materiales"][0],
            'mat2': product["materiales"][1],
            'mat3': product["materiales"][2],
            'mat4': product["materiales"][3]
        })

    return products

def generate_signature_payment(params: dict, secret_key: str) -> str:
    """
    Genera la firma HMAC-SHA256 requerida por Flow.
    Concatena clave+valor de los parámetros ordenados alfabéticamente.
    """
    # 1. Ordenar las llaves alfabéticamente
    keys_ordenadas = sorted(params.keys())
    
    # 2. Concatenar clave+valor
    mensaje_a_firmar = "".join([f"{key}{params[key]}" for key in keys_ordenadas])
    
    # 3. Generar HMAC-SHA256
    signature = hmac.new(
        key=secret_key.encode('utf-8'),
        msg=mensaje_a_firmar.encode('utf-8'),
        digestmod=hashlib.sha256
    ).hexdigest()
    
    return signature