from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

# Importamos desde 'datos'
from app.datos.dao_admin import Pro_CrearProducto, Pro_CrearMaterial

bp_admin = Blueprint('admin', __name__)

@bp_admin.route('/material/crear', methods=['POST'])
@jwt_required()
def crear_material():
    # Datos de texto
    nombre = request.form.get('nombre')
    descripcion = request.form.get('descripcion')
    
    # Archivos
    previsualizacion = request.files.get('previsualizacion')
    diffuse = request.files.get('diffuse')
    rough = request.files.get('rough')
    normal = request.files.get('normal')

    if not all([nombre, previsualizacion, diffuse, rough, normal]):
        return jsonify({"mensaje": "Faltan datos o texturas"}), 400

    exito = Pro_CrearMaterial(nombre, descripcion, previsualizacion, diffuse, rough, normal)

    if exito:
        return jsonify({"mensaje": "Material creado correctamente"}), 201
    else:
        return jsonify({"mensaje": "Error al procesar el material"}), 500

@bp_admin.route('/producto/crear', methods=['POST'])
@jwt_required()
def crear_producto():
    nombre = request.form.get('nombre')
    descripcion = request.form.get('descripcion')
    stock = request.form.get('stock')
    precio = request.form.get('precio')
    
    # Lista de imágenes
    lista_imagenes = request.files.getlist('imagenes')

    if not all([nombre, stock, precio]) or not lista_imagenes:
        return jsonify({"mensaje": "Faltan datos o imágenes del producto"}), 400

    exito = Pro_CrearProducto(nombre, descripcion, stock, precio, lista_imagenes)

    if exito:
        return jsonify({"mensaje": "Producto creado correctamente"}), 201
    else:
        return jsonify({"mensaje": "Error al procesar el producto"}), 500
