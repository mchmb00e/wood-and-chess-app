from flask import Blueprint, jsonify, request
from sessions.database import connection
from modules.crear_material import crear_material
from modules.listar_material import listar_material
from modules.modificar_material import modificar_material
from modules.eliminar_material import eliminar_material
from modules.consultar_material import consultar_material

materiales_bp = Blueprint('materiales_bp', __name__, url_prefix='/api/material')

@materiales_bp.route('/listar_material', methods=['GET'])
def api_listar_materiales():
    try:
        rol = request.args.get('rol', 'USR')
        
        lista = listar_material(rol)
        return jsonify(lista), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@materiales_bp.route('/consultar_material', methods=['GET'])
def api_consultar_material(id_material):
    try:
        material = consultar_material(id_material)
        if material:
            return jsonify(material), 200
        else:
            return jsonify({'mensaje': 'Material no encontrado'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@materiales_bp.route('/crear_material', methods=['POST'])
def api_crear_material():
    try:
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')

        previsualizacion = request.files.get('previsualizacion')
        diffuse = request.files.get('diffuse')
        normal = request.files.get('normal')
        rough = request.files.get('rough')

        if not all([nombre, previsualizacion, diffuse, normal, rough]):
            return jsonify({'error': 'Faltan datos o archivos obligatorios'}), 400

        exito = crear_material(
            nombre, 
            descripcion, 
            previsualizacion, 
            diffuse, 
            normal, 
            rough
        )

        if exito:
            return jsonify({'mensaje': 'Material creado exitosamente'}), 200
        else:
            return jsonify({'error': 'Error al crear el material'}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 400


@materiales_bp.route('/modificar_material', methods=['POST'])
def api_modificar_material(id_material):
    try:
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        
        prev = request.files.get('previsualizacion')
        diff = request.files.get('diffuse')
        norm = request.files.get('normal')
        rough = request.files.get('rough')

        if not all([nombre, prev, diff, norm, rough]):
             return jsonify({'error': 'Faltan archivos o datos para la modificación'}), 400

        exito = modificar_material(
            id_material, 
            nombre, 
            descripcion, 
            prev, 
            diff, 
            norm, 
            rough
        )

        if exito:
            return jsonify({'mensaje': 'Material modificado exitosamente'}), 200
        else:
            return jsonify({'error': 'Error al modificar o ID no encontrado'}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 400


@materiales_bp.route('/eliminar_material', methods=['POST', 'DELETE'])
def api_eliminar_material(id_material):
    try:
        exito = eliminar_material(id_material)
        
        if exito:
            return jsonify({'mensaje': 'Material eliminado correctamente'}), 200
        else:
            return jsonify({'error': 'No se pudo eliminar el material'}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 400