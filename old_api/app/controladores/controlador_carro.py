from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.datos.dao_carro import Pro_VaciarCarro

bp_carro = Blueprint('carro', __name__)

@bp_carro.route('/vaciar', methods=['POST'])
@jwt_required()
def vaciar_carro():
    usuario_rut = get_jwt_identity()
    resultado = Pro_VaciarCarro(usuario_rut)
    return jsonify(resultado)