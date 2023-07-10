from bd import obtener_conexion

def obtener_Jefe():
    conexion = obtener_conexion()
    jefe = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT  CONCAT(jf.apellidos, ', ', jf.nombre) AS jefe,jf.telefono,jf.correo,jf.cargo,em.razonSocial,jf.idJefe FROM JEFE_INMEDIATO jf INNER JOIN EMPRESA em ON jf.idEmpresa=em.idEmpresa")
        jefe = cursor.fetchall()
    conexion.close()
    return jefe

def insertar_JEFE(nombre ,apellidos,telefono,telefono2,correo ,correo2 ,cargo ,turno ,empresa ,usuario,contraseña,distrito):
    conexion = obtener_conexion()

    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO USUARIO(nomUsuario,contraseña,idTipoU) values(%s,%s,4)",
                       (usuario,contraseña))
        idUsuario = cursor.lastrowid
        cursor.execute("INSERT INTO JEFE_INMEDIATO(nombre ,apellidos,telefono,telefono2,correo ,correo2 ,cargo ,turnoHorario ,idEmpresa ,idUsuario,idDistrito)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                       (nombre ,apellidos,telefono,telefono2,correo ,correo2 ,cargo ,turno ,empresa ,idUsuario,distrito))
    conexion.commit()
    conexion.close()

def obtener_DetalleJefe(id):
    conexion = obtener_conexion()
    jefe = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT  CONCAT(jf.apellidos, ', ', jf.nombre) AS jefe,jf.telefono,jf.correo,jf.cargo,em.razonSocial,jf.idJefe,jf.telefono2,jf.correo2,ds.nombre FROM JEFE_INMEDIATO jf INNER JOIN EMPRESA em ON jf.idEmpresa=em.idEmpresa left JOIN distrito ds on ds.idDistrito=jf.idDistrito WHERE jf.idJefe=%s",(id))
        jefe = cursor.fetchall()
    conexion.close()
    return jefe

def actualizar_JEFE(nombre ,apellidos,telefono,telefono2,correo ,correo2 ,cargo ,turno ,empresa ,distrito,ID):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE JEFE_INMEDIATO SET nombre=%s ,apellidos=%s,telefono=%s,telefono2=%s,correo=%s ,correo2=%s ,cargo=%s ,turnoHorario=%s ,idEmpresa=%s ,idDistrito=%s WHERE JEFE_INMEDIATO.idJefe=%s",
                       (nombre ,apellidos,telefono,telefono2,correo ,correo2 ,cargo ,turno ,empresa ,distrito,ID))
    conexion.commit()
    conexion.close()

def obtener_DetalleJefeID(id):
    conexion = obtener_conexion()
    jefe = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT  jf.apellidos, jf.nombre,jf.telefono,jf.correo,jf.cargo,em.razonSocial,jf.idJefe,jf.telefono2,jf.correo2,ds.nombre,jf.idUsuario FROM JEFE_INMEDIATO jf INNER JOIN EMPRESA em ON jf.idEmpresa=em.idEmpresa left JOIN distrito ds on ds.idDistrito=jf.idDistrito WHERE jf.idJefe=%s",(id))
        jefe = cursor.fetchall()
    conexion.close()
    return jefe

def obtener_UsuarioJefe(id):
    conexion = obtener_conexion()
    jefe = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT nomUsuario,contraseña FROM USUARIO WHERE idUsuario=%s",(id))
        jefe = cursor.fetchall()
    conexion.close()
    return jefe


