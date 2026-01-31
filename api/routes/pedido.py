from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from modules.listar_pedidos import listar_pedidos
from modules.obtener_rol import obtener_rol
from modules.consultar_pedido import consultar_pedido
from modules.modificar_estado_pedido import modificar_estado_pedido

pedido_bp = Blueprint('pedido_bp', __name__, url_prefix='/api/pedido')
@pedido_bp.route('/listar', methods=['GET'])
@jwt_required()
def api_listar_pedidos():
    usuario_rut = get_jwt_identity()
    buscar_id = request.args.get('id')
    
    rol = obtener_rol(int(usuario_rut))
    
    resultado = listar_pedidos(
        usuario_rut=int(usuario_rut),
        rol=rol,
        buscar_id=int(buscar_id) if buscar_id else None
    )
    
    return jsonify(resultado), 200
@pedido_bp.route('/consultar/<id>', methods=['GET'])
@jwt_required()
def api_consultar_pedido(id):
    usuario_rut = get_jwt_identity()
    
    rol = obtener_rol(int(usuario_rut))
    
    resultado = consultar_pedido(
        pedido_id=int(id),
        usuario_rut=int(usuario_rut),
        rol=rol
    )
    
    if resultado:
        return jsonify(resultado), 200
    else:
        return jsonify({'mensaje': 'Pedido no encontrado'}), 400
    
@pedido_bp.route('/actualizar', methods=['PUT'])
@jwt_required()
def api_modificar_estado_pedido():
    pedido_id = request.form.get('id')
    estado = request.form.get('estado')
    
    exito = modificar_estado_pedido(
        pedido_id=int(pedido_id),
        estado=estado
    )
    
    if exito:
        return jsonify({'mensaje': 'Estado actualizado correctamente'}), 200
    else:
        return jsonify({'mensaje': 'Error al actualizar estado'}), 400