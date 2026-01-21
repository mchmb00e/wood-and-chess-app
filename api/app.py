from flask import Flask
from routes.usuario import usuario_bp
from routes.producto import producto_bp

app = Flask(__name__)

app.register_blueprint(usuario_bp)
app.register_blueprint(producto_bp)

@app.route('/', methods=['GET'])
def home():
    return "¡La API está funcionando!"