from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config

jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    jwt.init_app(app)
    CORS(app)

    # 1. Rutas de Acceso (Login y Registro)
    from app.controladores.controlador_acceso import bp_acceso
    app.register_blueprint(bp_acceso, url_prefix='/api/acceso')

    # 2. Rutas de Administración (Productos y Materiales)
    from app.controladores.controlador_admin import bp_admin
    app.register_blueprint(bp_admin, url_prefix='/api/admin')

    # 3. Rutas de Carro
    from app.controladores.controlador_carro import bp_carro
    app.register_blueprint(bp_carro, url_prefix='/api/carro')

    return app