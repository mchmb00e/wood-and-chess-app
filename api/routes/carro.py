from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from modules.listar_carro import listar_carro
from modules.agregar_producto_carro import agregar_producto_carro
from modules.eliminar_producto_carro import eliminar_producto_carro
from modules.vaciar_carro import vaciar_carro
from modules.puede_comentar import puede_comentar

carro_bp = Blueprint('carro_bp', __name__, url_prefix='/api/carro')

@carro_bp.route('/listar', methods=['GET'])
@jwt_required()
def api_listar_carro():
    usuario_rut = get_jwt_identity()
    
    resultado = listar_carro(usuario_rut)
    
    return jsonify(resultado), 200

@carro_bp.route('/agregar', methods=['POST'])
@jwt_required()
def api_agregar_producto_carro():
    usuario_rut = get_jwt_identity()
    prod_id = request.form.get('id')
    mat1 = request.form.get('id_material1')
    mat2 = request.form.get('id_material2')
    mat3 = request.form.get('id_material3')
    mat4 = request.form.get('id_material4')
    
    cantidad = agregar_producto_carro(
        usuario_rut=int(usuario_rut),
        prod_id=int(prod_id),
        mat1=int(mat1) if mat1 else None,
        mat2=int(mat2) if mat2 else None,
        mat3=int(mat3) if mat3 else None,
        mat4=int(mat4) if mat4 else None
    )
    
    if cantidad >= 0:
        return jsonify({'cantidad': cantidad}), 200
    else:
        return jsonify({'mensaje': 'Error al agregar producto'}), 400

@carro_bp.route('/eliminar/<id>', methods=['DELETE'])
@jwt_required()
def api_eliminar_producto_carro(id):
    usuario_rut = get_jwt_identity()
    
    cantidad = eliminar_producto_carro(
        car_id=int(id),
        usuario_rut=int(usuario_rut)
    )
    
    if cantidad >= 0:
        return jsonify({'cantidad': cantidad}), 200
    else:
        return jsonify({'mensaje': 'Error al eliminar producto'}), 400
    
@carro_bp.route('/vaciar', methods=['DELETE'])
@jwt_required()
def api_vaciar_carro():
    usuario_rut = get_jwt_identity()
    
    exito = vaciar_carro(int(usuario_rut))
    
    if exito:
        return jsonify({'mensaje': 'Carro vaciado correctamente'}), 200
    else:
        return jsonify({'mensaje': 'Error al vaciar carro'}), 400
    
@carro_bp.route('/puede_comentar/<id_producto>', methods=['GET'])
@jwt_required()
def api_puede_comentar(id_producto):
    usuario_rut = get_jwt_identity()
    
    habilitado = puede_comentar(
        usuario_rut=int(usuario_rut),
        producto_id=int(id_producto)
    )
    
    return jsonify({'habilitado': habilitado}), 200