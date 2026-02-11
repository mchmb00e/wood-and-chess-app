from flask import Blueprint, jsonify, request
from modules.crear_producto import crear_producto
from modules.puede_comentar import puede_comentar
from modules.listar_productos import listar_productos
from modules.obtener_rol import obtener_rol
from modules.buscar_producto import buscar_producto
from modules.eliminar_producto import eliminar_producto
from modules.consultar_stock import consultar_stock
from modules.consultar_producto import consultar_producto
from modules.modificar_producto import modificar_producto
from flask_jwt_extended import jwt_required, get_jwt_identity

producto_bp = Blueprint('producto_bp', __name__, url_prefix='/api/producto')

@producto_bp.route('/crear', methods=['POST'])
def api_crear_producto():
    try:
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        stock = request.form.get('stock')
        precio = request.form.get('precio')

        lista_imagenes = request.files.getlist('imagenes')

        val_stock = int(stock) if stock else 0
        val_precio = int(precio)

        exito = crear_producto(
            nombre=nombre,
            descripcion=descripcion,
            stock=val_stock,
            precio=val_precio,
            lista_imagenes=lista_imagenes
        )

        if exito:
            return jsonify({
                "mensaje": "Producto creado correctamente"
            }), 200
        else:
            return jsonify({
                "mensaje": "Hubo un error interno al guardar el producto"
            }), 400

    except Exception as e:
        return jsonify({"mensaje": str(e)}), 400
    
@producto_bp.route('/puede_comentar/<id_producto>', methods=['GET'])
@jwt_required()
def api_puede_comentar(id_producto):
    usuario_rut = get_jwt_identity()
    
    habilitado = puede_comentar(
        usuario_rut=int(usuario_rut),
        producto_id=int(id_producto)
    )
    
    return jsonify({'habilitado': habilitado}), 200

@producto_bp.route('/listar', methods=['GET'])
@jwt_required(optional = True)
def api_listar_productos():
    usuario_rut = get_jwt_identity()
    usuario_rol = 'USR' if usuario_rut is None else obtener_rol(usuario_rut)
    q = request.args.get('q')
    try:
        if q:
            productos = buscar_producto(busqueda = q, rol_usuario = usuario_rol)
        else:
            productos = listar_productos(usuario_rol)
    except Exception as e:
        return jsonify({'mensaje': e}), 400

    return jsonify(productos), 200

@producto_bp.route('/eliminar/<id>', methods=['DELETE'])
@jwt_required()
def api_eliminar_producto(id):
    usuario_rut = get_jwt_identity()
    usuario_rol = obtener_rol(int(usuario_rut))
    print(usuario_rut, usuario_rol)
    if usuario_rol == 'ADM':
        exito = eliminar_producto(id)
    else:
        exito = False

    if exito:
        return jsonify({'mensaje': 'Producto eliminado con exito.'})
    else:
        return jsonify({'mensaje': 'Hubo un error con el procedimiento.'})
    
@producto_bp.route('consultar_stock/<id>', methods=['GET'])
@jwt_required()
def api_consultar_stock(id):
    return jsonify({'cantidad': consultar_stock(id)})

@producto_bp.route('/consultar/<id>', methods=['GET'])
def api_consultar(id):
    return jsonify(consultar_producto(id))

@producto_bp.route('/modificar', methods=['PUT'])
@jwt_required()
def api_modificar_producto():
    try:
        # 1. Verificación de Seguridad (Solo ADM puede modificar)
        usuario_rut = get_jwt_identity()
        usuario_rol = obtener_rol(int(usuario_rut))
        
        if usuario_rol != 'ADM':
            return jsonify({"mensaje": "No tienes permisos para realizar esta acción"}), 403

        # 2. Captura de datos desde el form-data
        id_prod = request.form.get('id')
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        stock = request.form.get('stock')
        precio = request.form.get('precio')
        
        # Captura de la lista de archivos
        lista_imagenes = request.files.getlist('imagenes')

        # Validaciones básicas de tipos
        if not id_prod:
            return jsonify({"mensaje": "El ID del producto es requerido"}), 400
            
        val_stock = int(stock) if stock else 0
        val_precio = int(precio) if precio else 0

        # 3. Llamada al módulo lógico
        exito = modificar_producto(
            id_producto=int(id_prod),
            nombre=nombre,
            descripcion=descripcion,
            stock=val_stock,
            precio=val_precio,
            lista_imagenes=lista_imagenes
        )

        # 4. Retorno de respuestas según el resultado
        if exito:
            return jsonify({
                "mensaje": "Producto modificado correctamente"
            }), 200
        else:
            return jsonify({
                "mensaje": "Hubo un error interno al modificar el producto"
            }), 400

    except Exception as e:
        # En caso de errores inesperados (ej. error de conversión de int)
        return jsonify({"mensaje": f"Error en la solicitud: {str(e)}"}), 400