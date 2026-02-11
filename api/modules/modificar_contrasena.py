from sessions.database import get_db_connection
from scripts.utils import check_password_hash, generate_password_hash

def modificar_contrasena(usuario_rut: int, contrasena_actual: str, contrasena_nueva: str) -> bool:
    """
    Modifica la contraseña de un usuario.
    Retorna True si es exitoso, False si falla.
    """
    conn = None
    cursor = None
    
    try:
        # 1. Abrimos conexión segura y dedicada
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 2. Verificamos la contraseña actual
        cursor.execute(
            "SELECT USU_CONTRA FROM USUARIO WHERE USU_RUT = %s",
            (usuario_rut,)
        )
        usuario = cursor.fetchone()
        
        if not usuario:
            return False
        
        hash_db = usuario["USU_CONTRA"]
        
        # Si la contraseña actual no coincide, cortamos al toque
        if not check_password_hash(pwd_plana=contrasena_actual, pwd_hash=hash_db):
            return False
        
        # 3. Generamos el hash nuevo y actualizamos
        nuevo_hash = generate_password_hash(contrasena_nueva)
        
        cursor.execute(
            "UPDATE USUARIO SET USU_CONTRA = %s WHERE USU_RUT = %s",
            (nuevo_hash, usuario_rut)
        )
        
        # 4. Confirmamos el cambio
        conn.commit()
        return True
        
    except Exception as e:
        print(f"Error cambiando contraseña: {e}")
        # Si falla el update, hacemos rollback por seguridad
        if conn:
            conn.rollback()
        return False
        
    finally:
        # 5. Cerramos todo
        if cursor:
            cursor.close()
        if conn:
            conn.close()