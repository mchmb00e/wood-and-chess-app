import bcrypt
import pymysql

def crear_super_admin():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='chess_store'
    )
    
    rut = 11111111
    email = "admin@woodchess.cl"
    password_plana = "admin123"
    
    # Encriptar con BCRYPT
    salt = bcrypt.gensalt()
    hash_bytes = bcrypt.hashpw(password_plana.encode('utf-8'), salt)
    password_hash = hash_bytes.decode('utf-8')
    
    cursor = conn.cursor()
    try:
        # Borramos al admin anterior si existe
        cursor.execute("DELETE FROM USUARIO WHERE USU_RUT = %s", (rut,))
        
        query = """
            INSERT INTO USUARIO (USU_RUT, USU_NOMBRE, USU_APELLIDO, USU_EMAIL, USU_CONTRA, USU_ROL, USU_TELEF)
            VALUES (%s, 'Admin', 'Supremo', %s, %s, 'ADM', '999999999')
        """
        cursor.execute(query, (rut, email, password_hash))
        conn.commit()
        print("✅ Admin creado con BCRYPT.")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    crear_super_admin()
