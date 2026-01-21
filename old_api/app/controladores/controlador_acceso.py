from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity
# Importamos desde la carpeta 'datos'
from app.datos.dao_usuario import Pro_RegistrarCliente, Pro_AutenticarUsuario

bp_acceso = Blueprint('acceso', __name__)

@bp_acceso.route('/login', methods=['POST'])
def iniciar_sesion():
    data = request.get_json()
    
    email = data.get('email')
    password = data.get('contrasena') 

    if not email or not password:
        return jsonify({"mensaje": "Faltan credenciales"}), 400

    token = Pro_AutenticarUsuario(email, password)

    if token:
        return jsonify({"mensaje": "Autenticación exitosa", "token": token}), 200
    else:
        return jsonify({"mensaje": "Credenciales inválidas"}), 401

@bp_acceso.route('/registro', methods=['POST'])
def registrarse():
    data = request.get_json()
    
    if not all([data.get('rut'), data.get('email'), data.get('contrasena')]):
        return jsonify({"mensaje": "Faltan datos para el registro"}), 400

    token = Pro_RegistrarCliente(
        rut=data.get('rut'),
        nombre=data.get('nombre'),
        apellido=data.get('apellido'),
        email=data.get('email'),
        password=data.get('contrasena'),
        telefono=data.get('telefono')
    )

    if token:
        return jsonify({"mensaje": "Usuario registrado exitosamente", "token": token}), 201
    else:
        return jsonify({"mensaje": "Error al registrar"}), 500
