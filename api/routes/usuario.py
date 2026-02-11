from flask import Blueprint, jsonify, request
from modules.registrar_cliente import registrar_cliente
from flask_jwt_extended import get_jwt_identity, jwt_required
from modules.autenticar_usuario import autenticar_usuario
from modules.modificar_contrasena import modificar_contrasena
from modules.obtener_sesion import obtener_sesion

usuario_bp = Blueprint('usuario_bp', __name__, url_prefix='/api/usuario')

@usuario_bp.route('/registrar', methods=['POST'])
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

@usuario_bp.route('/autenticar', methods=['POST'])
def api_autenticar_usuario():
    email = request.form.get('email')
    contrasena = request.form.get('contrasena')
    
    token = autenticar_usuario(email, contrasena)
    
    if token:
        return jsonify({'token': token}), 200
    else:
        return jsonify({'token': ""}), 400

@usuario_bp.route('/obtener_sesion', methods=['GET'])
@jwt_required()
def api_obtener_sesion():
    usuario_rut = get_jwt_identity()
    
    datos = obtener_sesion(usuario_rut)
    
    if datos:
        return jsonify(datos), 200
    else:
        return jsonify({'error': 'Usuario no encontrado'}), 400

@usuario_bp.route('/modificar_contrasena', methods=['PUT'])
@jwt_required()
def api_modificar_contrasena():
    usuario_rut = get_jwt_identity()
    contrasena_actual = request.form.get('contrasena_actual')
    contrasena_nueva = request.form.get('contrasena_nueva')
    
    exito = modificar_contrasena(usuario_rut, contrasena_actual, contrasena_nueva)
    
    if exito:
        return jsonify({'mensaje': 'Contraseña modificada correctamente'}), 200
    else:
        return jsonify({'mensaje': 'Error al modificar contraseña'}), 400