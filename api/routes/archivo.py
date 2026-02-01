from flask import Blueprint, request
from modules.obtener_archivo import obtener_archivo

archivo_bp = Blueprint('archivo', __name__)

@archivo_bp.route('/api/obtener_archivo', methods=['GET'])
def ruta_obtener_archivo():
    """
    GET /api/obtener_archivo?ruta=producto/3_1.jpg
    
    Retorna el archivo solicitado
    """
    ruta_relativa = request.args.get('ruta')
    return obtener_archivo(ruta_relativa)