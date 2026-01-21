def create_admin(
        rut: int,
        nombre: str,
        apellido: str,
        email: str,
        contrasena: str,
        telefono: str) -> bool:
    """
    Create a administrator user for Wood&Chess System
    """
    from sessions.database import connection
    from scripts.utils import generate_password_hash
    
    contrasena_hash = generate_password_hash(contrasena)

    with connection.cursor() as cursor:
        sql_check = "SELECT * FROM USUARIO WHERE USU_RUT = %s OR USU_EMAIL = %s"
        cursor.execute(sql_check, (rut, email))
        
        res = cursor.fetchone()

        if res:
            print(f"Usuario duplicado")
            return False

        sql_insert = """
        INSERT INTO USUARIO 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(
        sql_insert,
        (rut, nombre, apellido, email, contrasena_hash, 'ADM', telefono)
        )
        
        connection.commit()
        return True