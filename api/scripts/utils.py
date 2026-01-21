import os

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
