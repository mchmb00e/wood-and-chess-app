from datetime import timedelta
from flask import Flask
from routes.usuario import usuario_bp
from routes.producto import producto_bp
from routes.carro import carro_bp
from sessions.env import getenv
from flask_jwt_extended import JWTManager
from routes.pedido import pedido_bp
from routes.archivo import archivo_bp

app = Flask(__name__)

app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours = int(getenv('TOKEN_EXPIRES_IN')))
app.config["JWT_SECRET_KEY"] = "CONTRASENA_MUY_PERO_MUYMUY_SEGURA"

app.register_blueprint(usuario_bp)
app.register_blueprint(producto_bp)
app.register_blueprint(carro_bp)
app.register_blueprint(pedido_bp)
app.register_blueprint(archivo_bp)

jwt = JWTManager(app)

@app.route('/', methods=['GET'])
def home():
    return "¡La API está funcionando!"

@app.route('/vixo', methods=['GET'])
def vixo():
    return "Hola vixo"