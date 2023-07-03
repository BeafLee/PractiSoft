from bd import obtener_conexion

def verificarUsuario(usu, contra):
    conexion=obtener_conexion()
    usuario = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM USUARIO WHERE nomUsuario = %s and contraseña = %s", (usu, contra))
        usuario = cursor.fetchone()
        print(usuario)
    conexion.close()
    return usuario

def obtenerIdUsuario(usu):
    conexion=obtener_conexion()
    usuario = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT usuario.idUsuario FROM USUARIO WHERE nomUsuario = %s", (usu))
        usuario = cursor.fetchone()
        print(usuario)
    conexion.close()
    return usuario