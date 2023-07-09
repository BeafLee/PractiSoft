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


#Provincias
def listar_provincias():
    conexion=obtener_conexion()
    ubicaciones = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT pr.idProvincia, p.nombre as pais, d.nombre as departamento, pr.nombre as provincia FROM pais p inner join departamento d on p.idPais = d.idPais inner join provincia pr on d.idDepartamento = pr.idDepartamento;")
        ubicaciones = cursor.fetchall()
    conexion.close()
    return ubicaciones

def insertar_provincia(nombre, idDepartamento):
    conexion=obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("insert into PROVINCIA(nombre, idDepartamento) values (%s, %s)", (nombre, idDepartamento))
    conexion.commit()
    conexion.close()

def buscar_provincia(idProvincia):
    conexion = obtener_conexion()
    ubicacion = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT pr.IDPROVINCIA, pr.nombre, p.idpais, d.IDDEPARTAMENTO FROM pais p inner join departamento d on p.idPais = d.idPais inner join provincia pr on d.idDepartamento = pr.idDepartamento WHERE IDPROVINCIA = %s", (idProvincia,))
        ubicacion = cursor.fetchone()
    conexion.close()
    return ubicacion

def eliminar_provincia(idProvincia):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM PROVINCIA WHERE IDPROVINCIA = %s", (idProvincia))
    conexion.commit()
    conexion.close()

def actualizar_provincia(nombre, idDepartamento, idProvincia):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE PROVINCIA SET nombre= %s, idDepartamento= %s WHERE idProvincia = %s",
                       (nombre, idDepartamento, idProvincia))
    conexion.commit()
    conexion.close()



#DEPARTAMENTO
def listar_departamento():
    conexion=obtener_conexion()
    ubicaciones = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT d.idDepartamento, p.nombre as pais, d.nombre as departamento FROM pais p inner join departamento d on p.idPais = d.idPais;")
        ubicaciones = cursor.fetchall()
    conexion.close()
    return ubicaciones

def insertar_departamento(nombre, idPais):
    conexion=obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("insert into DEPARTAMENTO(nombre, idPais) values (%s, %s)", (nombre, idPais))
    conexion.commit()
    conexion.close()

def buscar_departamento(idDepartamento):
    conexion = obtener_conexion()
    ubicacion = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT d.idDepartamento, d.nombre, p.idpais FROM pais p inner join departamento d on p.idPais = d.idPais WHERE idDepartamento = %s", (idDepartamento,))
        ubicacion = cursor.fetchone()
    conexion.close()
    return ubicacion

def eliminar_departamento(idDepartamento):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM DEPARTAMENTO WHERE idDepartamento = %s", (idDepartamento))
    conexion.commit()
    conexion.close()

def actualizar_departamento(nombre, idPais, idDepartamento):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE DEPARTAMENTO SET nombre= %s, idPais= %s WHERE idDepartamento = %s",
                       (nombre, idPais, idDepartamento))
    conexion.commit()
    conexion.close()


#PAIS
def listar_pais():
    conexion=obtener_conexion()
    ubicaciones = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT idPais, nombre FROM pais;")
        ubicaciones = cursor.fetchall()
    conexion.close()
    return ubicaciones

def insertar_pais(nombre):
    conexion=obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("insert into PAIS(nombre) values (%s)", (nombre))
    conexion.commit()
    conexion.close()

def buscar_pais(idPais):
    conexion = obtener_conexion()
    ubicacion = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT idpais, nombre FROM PAIS WHERE idPais = %s", (idPais,))
        ubicacion = cursor.fetchone()
    conexion.close()
    return ubicacion

def eliminar_pais(idPais):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM PAIS WHERE idPais = %s", (idPais))
    conexion.commit()
    conexion.close()

def actualizar_pais(nombre, idPais):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE PAIS SET nombre= %s WHERE idPais = %s",
                       (nombre, idPais))
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