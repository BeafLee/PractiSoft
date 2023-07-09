from bd import obtener_conexion

def listar_distritos():
    conexion=obtener_conexion()
    ubicaciones = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT di.idDistrito, p.nombre as pais, d.nombre as departamento, pr.nombre as provincia, di.nombre as distrito FROM pais p inner join departamento d on p.idPais = d.idPais inner join provincia pr on d.idDepartamento = pr.idDepartamento inner join distrito di on pr.idProvincia = di.idProvincia;")
        ubicaciones = cursor.fetchall()
    conexion.close()
    return ubicaciones

def insertar_distrito(nombre, idProvincia):
    conexion=obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("insert into DISTRITO(nombre, idProvincia) values (%s, %s)", (nombre, idProvincia))
    conexion.commit()
    conexion.close()

def buscar_distrito(idDistrito):
    conexion = obtener_conexion()
    ubicacion = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT di.idDistrito, di.nombre as distrito, p.idpais, d.IDDEPARTAMENTO, pr.IDPROVINCIA FROM pais p inner join departamento d on p.idPais = d.idPais inner join provincia pr on d.idDepartamento = pr.idDepartamento inner join distrito di on pr.idProvincia = di.idProvincia WHERE idDistrito = %s", (idDistrito,))
        ubicacion = cursor.fetchone()
    conexion.close()
    return ubicacion

def eliminar_distrito(idDistrito):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM DISTRITO WHERE idDistrito = %s", (idDistrito))
    conexion.commit()
    conexion.close()

def actualizar_distrito(nombre, idProvincia, idDistrito):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE DISTRITO SET nombre= %s, idProvincia= %s WHERE idDistrito = %s",
                       (nombre, idProvincia, idDistrito))
    conexion.commit()
    conexion.close()



def datos_paises():
    conexion=obtener_conexion()
    ubicacion = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT idPais, nombre FROM pais")
        ubicacion = cursor.fetchall()

    conexion.close()
    return ubicacion

def datos_departamentos(idPais):
    conexion=obtener_conexion()
    ubicacion = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT idDepartamento, nombre FROM departamento where idPais = %s", idPais)
        ubicacion = cursor.fetchall()
    conexion.close()
    return ubicacion

def datos_provincias(idDepartamento):
    conexion=obtener_conexion()
    ubicacion = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT idProvincia, nombre FROM PROVINCIA where idDepartamento = %s", idDepartamento)
        ubicacion = cursor.fetchall()
    conexion.close()
    return ubicacion




# def registrar_jefe():
#     conexion=obtener_conexion()
    
#     with conexion.cursor() as cursor:
#         cursor.execute("insert into usuario values (usu, pass, v)")
        

#         cursor.execute("SELECT id from usuario where nomUsuario = usu and contraseña = pass")
#         id = cursor.fetchone()[0]

#         cursor.execute("insert into jefe values (..........., %s)", id)

#     conexion.commit()
#     conexion.close()