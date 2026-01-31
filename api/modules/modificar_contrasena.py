from sessions.database import connection
from scripts.utils import check_password_hash, generate_password_hash

def modificar_contrasena(usuario_rut: int, contrasena_actual: str, contrasena_nueva: str) -> bool:
    """
    Modifica la contraseña de un usuario.
    Retorna True si es exitoso, False si falla.
    """
    cursor = connection.cursor()
    try:
        cursor.execute(
            "SELECT USU_CONTRA FROM USUARIO WHERE USU_RUT = %s",
            (usuario_rut,)
        )
        usuario = cursor.fetchone()
        
        if not usuario:
            return False
        
        hash_db = usuario["USU_CONTRA"]
        
        if not check_password_hash(pwd_plana=contrasena_actual, pwd_hash=hash_db):
            return False
        
        nuevo_hash = generate_password_hash(contrasena_nueva)
        
        cursor.execute(
            "UPDATE USUARIO SET USU_CONTRA = %s WHERE USU_RUT = %s",
            (nuevo_hash, usuario_rut)
        )
        connection.commit()
        return True
        
    except Exception as e:
        return False
    finally:
        cursor.close()