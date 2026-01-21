from flask import Blueprint, jsonify, request
from sessions.database import connection
from modules.crear_producto import crear_producto

producto_bp = Blueprint('producto_bp', __name__, url_prefix='/api/producto')

@producto_bp.route('/crear_producto', methods=['POST'])
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
                "success": True, 
                "mensaje": "Producto creado correctamente"
            }), 200
        else:
            return jsonify({
                "success": False, 
                "mensaje": "Hubo un error interno al guardar el producto"
            }), 500

    except Exception as e:
        return jsonify({"success": False, "mensaje": str(e)}), 500