from flask import send_file, jsonify
import os
from werkzeug.utils import secure_filename
from sessions.env import getenv  # Usamos tu wrapper para asegurar que lea el .env

def obtener_archivo(ruta_relativa):
    """
    Obtiene un archivo del sistema dada su ruta relativa
    """
    try:
        if not ruta_relativa:
            return jsonify({
                'error': 'El parámetro "ruta" es requerido'
            }), 400
        
        # Usamos tu función getenv para mantener consistencia
        base_archivo = getenv('BASE_ARCHIVO')
        
        # Fallback por si no está en el .env (opcional, pero buena práctica)
        if not base_archivo:
            base_archivo = 'static/files/'

        base_absoluta = os.path.abspath(base_archivo)
        
        # Construir ruta completa
        ruta_completa = os.path.abspath(os.path.join(base_absoluta, ruta_relativa))
        
        # SECURITY CHECK: Previene Path Traversal (evita que pidan ../../../etc/passwd)
        if not ruta_completa.startswith(base_absoluta):
            return jsonify({
                'error': 'Ruta inválida (Intento de Path Traversal)'
            }), 400
        
        # Verificar que el archivo existe
        if not os.path.exists(ruta_completa):
            return jsonify({
                'error': f'El archivo no existe'
            }), 404 # 404 es más semántico para "No encontrado"
        
        # Verificar que es un archivo y no una carpeta
        if not os.path.isfile(ruta_completa):
            return jsonify({
                'error': 'La ruta especificada no es un archivo válido'
            }), 400
        
        # Enviar el archivo
        return send_file(ruta_completa), 200
        
    except Exception as e:
        print(f"Error sirviendo archivo: {e}")
        return jsonify({
            'error': 'Error interno del servidor al obtener el archivo'
        }), 500