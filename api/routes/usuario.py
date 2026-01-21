from flask import Blueprint, jsonify, request
from sessions.database import connection
from modules.registrar_cliente import registrar_cliente
from scripts.utils import check_password_hash
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

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
    

@usuario_bp.route('/registrar_cliente', methods=['POST'])
def api_registrar_cliente():
    rut = request.form.get('rut')
    rut = int(rut)

    nombre = request.form.get('nombre')
    apellido = request.form.get('apellido')
    email = request.form.get('email')
    contrasena = request.form.get('contrasena')
    telefono = request.form.get('telefono')

    token = registrar_cliente(
        rut = rut,
        nombre = nombre,
        apellido = apellido,
        email = email,
        password = contrasena,
        telefono = telefono
    )

    if token is None:
        token = ""

    return jsonify({
        'token': token
    })

@usuario_bp.route('/autenticar_usuario', methods=['POST'])
def api_autenticar_usuario():
    email = request.form.get('email')
    contrasena = request.form.get('contrasena')

    cursor = connection.cursor()
    try:
        cursor.execute(
            "SELECT USU_RUT, USU_CONTRA FROM USUARIO WHERE USU_EMAIL = %s",
            (email,)
        )
        usuario = cursor.fetchone()

        if not usuario:
            return jsonify({'token': ""}), 401

        rut_usuario = str(usuario["USU_RUT"])
        hash_db = usuario["USU_CONTRA"]

        es_valida = check_password_hash(pwd_plana = contrasena, pwd_hash = hash_db)

        if es_valida:
            token = create_access_token(identity=rut_usuario)
            return jsonify({'token': token}), 200
        else:
            return jsonify({'token': ""}), 401

    except Exception as e:
        return jsonify({'error': 'Error interno servidor', 'detalles': f"{e}"}), 500
    finally:
        cursor.close() # Siempre cerrar el cursor

@usuario_bp.route("/mis_datos", methods=['GET'])
@jwt_required()
def perfil():
    rut = get_jwt_identity()
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT USU_RUT, USU_NOMBRE, USU_APELLIDO, USU_EMAIL, USU_TELEF
        FROM USUARIO
        WHERE USU_RUT = %s
        """,
        (int(rut),)
    )

    usuario = cursor.fetchone()

    return jsonify(usuario)