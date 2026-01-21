import bcrypt
import pymysql
from flask_jwt_extended import create_access_token

def get_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='chess_store'
    )

def Pro_RegistrarCliente(rut, nombre, apellido, email, password, telefono):
    salt = bcrypt.gensalt()
    hash_bytes = bcrypt.hashpw(password.encode('utf-8'), salt)
    password_hash_str = hash_bytes.decode('utf-8')
    
    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = """
            INSERT INTO USUARIO (USU_RUT, USU_NOMBRE, USU_APELLIDO, USU_EMAIL, USU_CONTRA, USU_ROL, USU_TELEF)
            VALUES (%s, %s, %s, %s, %s, 'USR', %s)
        """
        cursor.execute(query, (rut, nombre, apellido, email, password_hash_str, telefono))
        conn.commit()
        cursor.close()
        conn.close()

        token = create_access_token(identity=str(rut), additional_claims={"rol": "USR"})
        return token

    except Exception as e:
        print(f"Error en Pro_RegistrarCliente: {e}")
        cursor.close()
        conn.close()
        return None

def Pro_AutenticarUsuario(email, password_plana):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = "SELECT USU_RUT, USU_CONTRA, USU_ROL FROM USUARIO WHERE USU_EMAIL = %s"
        cursor.execute(query, (email,))
        usuario = cursor.fetchone()
        cursor.close()
        conn.close()

        if usuario:
            rut_db = str(usuario[0])
            password_hash_db = usuario[1]
            rol_db = usuario[2]

            if bcrypt.checkpw(password_plana.encode('utf-8'), password_hash_db.encode('utf-8')):
                token = create_access_token(identity=rut_db, additional_claims={"rol": rol_db})
                return token
        
        return None

    except Exception as e:
        print(f"Error en Pro_AutenticarUsuario: {e}")
        return None