import os
from werkzeug.utils import secure_filename

def getextension(filename):
    """
    Obtiene la extensión de un archivo (ej: .jpg).
    """
    if '.' in filename:
        return filename.rsplit('.', 1)[1].lower()
    return ''

def save_file(file_obj, full_path):
    """
    Guarda el archivo en la ruta física, creando carpetas si no existen.
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
