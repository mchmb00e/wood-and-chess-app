from scripts.utils import generate_password_hash
from sessions.database import get_db_connection  # Importamos la función creadora
from flask_jwt_extended import create_access_token

def registrar_cliente(rut: int, nombre: str, apellido: str, email: str, password: str, telefono: str) -> str:
    """
    Registra un cliente en el sistema.
    Retorna el token JWT si es exitoso, None si el RUT/Email ya existen o si hay error.
    """
    conn = None
    cursor = None
    
    # 1. Preparar datos iniciales
    pwd_hash = generate_password_hash(password)
    identity = str(rut)

    try:
        # 2. Abrimos conexión fresca
        conn = get_db_connection()
        cursor = conn.cursor()

        # 3. Verificamos si el usuario ya existe (RUT o Email)
        query_condition = """
            SELECT USU_RUT
            FROM USUARIO
            WHERE USU_RUT = %s
            OR USU_EMAIL = %s
        """
        cursor.execute(query_condition, (rut, email))

        if cursor.fetchone():
            # Si ya existe, no registramos nada
            return None

        # 4. Insertamos el nuevo cliente
        query_insert = """
            INSERT INTO USUARIO (USU_RUT, USU_NOMBRE, USU_APELLIDO, USU_EMAIL, USU_CONTRA, USU_ROL, USU_TELEF)
            VALUES (%s, %s, %s, %s, %s, 'USR', %s)
        """
        cursor.execute(query_insert, (rut, nombre, apellido, email, pwd_hash, telefono))
        
        # 5. Confirmamos la transacción
        conn.commit()

        # 6. Generamos el token de acceso para que entre logueado de una
        token = create_access_token(identity=identity)
        return token

    except Exception as e:
        print(f"Error en registro de cliente: {e}")
        # Si algo falla (ej: error de red), deshacemos cualquier cambio pendiente
        if conn:
            conn.rollback()
        return None
        
    finally:
        # 7. Cerramos recursos sagradamente
        if cursor:
            cursor.close()
        if conn:
            conn.close()