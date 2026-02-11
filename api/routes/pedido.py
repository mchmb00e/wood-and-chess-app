from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from modules.listar_pedidos import listar_pedidos
from modules.obtener_rol import obtener_rol
from modules.consultar_pedido import consultar_pedido
from modules.modificar_estado_pedido import modificar_estado_pedido
from modules.generar_pedido import generar_pedido
from modules.generar_solicitud_pago import generar_solicitud_pago
from modules.modificar_token_pedido import modificar_token_pedido
from modules.procesar_confirmacion import procesar_confirmacion_pago

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
    
@pedido_bp.route('/generar', methods=['POST'])
@jwt_required()
def api_generar_pedido():
    rut = get_jwt_identity()
    retiro_en_tienda = True if int(request.args.get('retiro_en_tienda')) == 1 else False
    if retiro_en_tienda:
        datos_envio = {
            'calle': request.form.get('calle'),
            'numero': request.form.get('numero'),
            'comuna': request.form.get('comuna'),
            'region': request.form.get('region'),
            'indicaciones': request.form.get('indicaciones')
        }
        id_pedido = generar_pedido(rut = rut, datos_envio = datos_envio)
    else:
        id_pedido = generar_pedido(rut = rut)
    
    url_pago, token = generar_solicitud_pago(id_pedido)

    modificar_token_pedido(id_pedido, token)

    if id_pedido is not None:
        return jsonify({'url_pago': url_pago})
    else:
        return jsonify({'mensaje': "Hubo un error."})


@pedido_bp.route('/confirmar', methods=['POST'])
def api_confirmar_pedido():
    """
    Endpoint (Webhook) que recibe la confirmación de pago desde Flow.
    Solo delega al módulo de lógica.
    """
    # 1. Obtener el token del formulario (Flow envía x-www-form-urlencoded)
    token = request.form.get('token')
    
    # 2. Validación básica de entrada
    if not token:
        return jsonify({'error': 'Token no proporcionado'}), 400

    # 3. Delegar la lógica al módulo que implementa el pseudocódigo
    resultado = procesar_confirmacion_pago(token)

    # 4. Responder a Flow
    if resultado:
        # Retornar 200 OK le indica a Flow que deje de reintentar
        return "ACEPTADO", 200
    else:
        # Retornar error (500) hace que Flow reintente más tarde
        return jsonify({'error': 'Error al procesar la confirmación'}), 500