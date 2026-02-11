from sessions.database import get_db_connection
from scripts.utils import check_password_hash
from flask_jwt_extended import create_access_token

def autenticar_usuario(email: str, contrasena: str) -> str:
    """
    Autentica un usuario en el sistema.
    Retorna el token JWT si es exitoso, None si falla.
    """
    conn = None
    cursor = None
    
    try:
        # 1. Abrimos conexión nueva
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT USU_RUT, USU_CONTRA FROM USUARIO WHERE USU_EMAIL = %s",
            (email,)
        )
        usuario = cursor.fetchone()
        
        # Si no existe el usuario, cerramos por fuera
        if not usuario:
            return None
        
        rut_usuario = str(usuario["USU_RUT"])
        hash_db = usuario["USU_CONTRA"]
        
        # 2. Verificamos la pass
        if check_password_hash(pwd_plana=contrasena, pwd_hash=hash_db):
            # Si es el Easykid entrando a su cuenta, le damos el token
            token = create_access_token(identity=rut_usuario)
            return token
            
        return None

    except Exception as e:
        print(f"Error en auth: {e}")
        return None
        
    finally:
        # 3. Limpieza sagrada: cerrar cursor y conexión
        if cursor:
            cursor.close()
        if conn:
            conn.close()