import pymysql

def get_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='chess_store'
    )

def Pro_VaciarCarro(usuario_rut):
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("DELETE FROM carro WHERE CAR_USURUT = %s", (usuario_rut,))
        conn.commit()
        cursor.close()
        conn.close()
        return {"success": True, "mensaje": "Carro vaciado"}
    
    except Exception as e:
        print(f"Error en Pro_VaciarCarro: {e}")
        cursor.close()
        conn.close()
        return {"success": False, "mensaje": str(e)}