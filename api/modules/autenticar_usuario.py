from sessions.database import connection
from scripts.utils import check_password_hash
from flask_jwt_extended import create_access_token

def autenticar_usuario(email: str, contrasena: str) -> str:
    """
    Autentica un usuario en el sistema.
    Retorna el token JWT si es exitoso, None si falla.
    """
    cursor = connection.cursor()
    try:
        cursor.execute(
            "SELECT USU_RUT, USU_CONTRA FROM USUARIO WHERE USU_EMAIL = %s",
            (email,)
        )
        usuario = cursor.fetchone()
        if not usuario:
            return None
        
        rut_usuario = str(usuario["USU_RUT"])
        hash_db = usuario["USU_CONTRA"]
        
        if check_password_hash(pwd_plana=contrasena, pwd_hash=hash_db):
            token = create_access_token(identity=rut_usuario)
            return token
        return None
    except Exception as e:
        return None
    finally:
        cursor.close()