from scripts.utils import generate_password_hash
from sessions.database import connection
from flask_jwt_extended import create_access_token

def registrar_cliente(rut: int, nombre: str, apellido: str, email: str, password: str, telefono: str) -> str:
    """
    Registra un cliente en el sistema.
    """
    pwd_hash = generate_password_hash(password)
    identity = str(rut)

    cursor = connection.cursor()
    try:

        query_condition = """
            SELECT *
            FROM USUARIO
            WHERE USU_RUT = %s
            OR USU_EMAIL = %s
        """

        cursor.execute(query_condition, (rut, email))

        if cursor.fetchone():
            return None

        query = """
            INSERT INTO USUARIO (USU_RUT, USU_NOMBRE, USU_APELLIDO, USU_EMAIL, USU_CONTRA, USU_ROL, USU_TELEF)
            VALUES (%s, %s, %s, %s, %s, 'USR', %s)
        """
        cursor.execute(query, (rut, nombre, apellido, email, pwd_hash, telefono))
        connection.commit()

        token = create_access_token(identity = identity)
        return token

    except Exception as e:
        return None