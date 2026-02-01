from flask import send_file, jsonify
import os
from werkzeug.utils import secure_filename

def obtener_archivo(ruta_relativa):
    """
    Obtiene un archivo del sistema dada su ruta relativa
    """
    try:
        if not ruta_relativa:
            return jsonify({
                'error': 'El parámetro "ruta" es requerido'
            }), 400
        
        # Obtener la ruta base y convertir a absoluta
        base_archivo = os.getenv('BASE_ARCHIVO', 'static/files/')
        base_absoluta = os.path.abspath(base_archivo)
        
        # Construir ruta completa
        ruta_completa = os.path.abspath(os.path.join(base_absoluta, ruta_relativa))
        
        # Verificar que la ruta está dentro de la carpeta base (previene path traversal)
        if not ruta_completa.startswith(base_absoluta):
            return jsonify({
                'error': 'Ruta inválida'
            }), 400
        
        # Verificar que el archivo existe
        if not os.path.exists(ruta_completa):
            return jsonify({
                'error': f'El archivo no existe: {ruta_relativa}'
            }), 400
        
        # Verificar que es un archivo
        if not os.path.isfile(ruta_completa):
            return jsonify({
                'error': 'La ruta especificada no es un archivo válido'
            }), 400
        
        # Enviar el archivo
        return send_file(ruta_completa), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Error al obtener el archivo: {str(e)}'
        }), 400