from bd import obtener_conexion

def obtener_Distrito():
    conexion = obtener_conexion()
    distrito = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT*FROM DISTRITO")
        distrito = cursor.fetchall()
    conexion.close()
    return distrito

def obtener_Provincia():
    conexion = obtener_conexion()
    provincia = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT*FROM PROVINCIA")
        provincia = cursor.fetchall()
    conexion.close()
    return provincia

def obtener_Departamento():
    conexion = obtener_conexion()
    departamento = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT*FROM DEPARTAMENTO")
        departamento = cursor.fetchall()
    conexion.close()
    return departamento

