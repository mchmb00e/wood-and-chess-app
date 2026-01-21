from flask import Blueprint, jsonify
from sessions.database import connection

usuario_bp = Blueprint('usuario_bp', __name__, url_prefix='/api/usuario')

@usuario_bp.route('/listar_usuarios', methods=['GET'])
def listar_usuarios():
    query = """
    SELECT USU_RUT, USU_NOMBRE, USU_APELLIDO, USU_EMAIL, USU_ROL, USU_TELEF
    FROM USUARIO
    """
    
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            res = cursor.fetchall()
            
        return jsonify(res), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    