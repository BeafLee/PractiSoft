from bd import obtener_conexion

def obtener_cliente():
    conexion = obtener_conexion()
    cliente = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id, dni, nombre, apellido, telefono,direccion FROM cliente")
        cliente = cursor.fetchall()
    conexion.close()
    return cliente

def obtener_tipousuario_por_usuario(usu):
    conexion = obtener_conexion()
    juego = None
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT idTipoU FROM usuario WHERE idUsuario = %s", (usu,))
        juego = cursor.fetchone()
    conexion.close()
    return juego

def obtener_idUsuario_por_usuario(usu):
    conexion = obtener_conexion()
    juego = None
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT idUsuario FROM usuario WHERE idUsuario = %s", (usu,))
        juego = cursor.fetchone()
    conexion.close()
    return juego

def actualizar_usuario(nomUsuario, contraseña, idTipoU, idUsuario):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE usuario SET nomUsuario = %s, contraseña = %s, idTipoU = %s WHERE idUsuario = %s",
                       (nomUsuario, contraseña, idTipoU, idUsuario))
    conexion.commit()
    conexion.close()