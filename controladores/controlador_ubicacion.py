from bd import obtener_conexion

def listar_distritos():
    conexion=obtener_conexion()
    usuario = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT di.idDistrito, p.nombre as pais, d.nombre as departamento, pr.nombre as provincia, di.nombre as distrito FROM pais p inner join departamento d on p.idPais = d.idPais inner join provincia pr on d.idDepartamento = pr.idDepartamento inner join distrito di on pr.idProvincia = di.idProvincia;")
        usuario = cursor.fetchall()
    conexion.close()
    return usuario

def obtener_datos_combos():
    conexion=obtener_conexion()
    usuario = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT idPais, nombre FROM pais")
        usuario.append(cursor.fetchall())

        cursor.execute("SELECT d.idDepartamento, d.nombre, p.idPais FROM pais p inner join departamento d on p.idPais = d.idPais")
        usuario.append(cursor.fetchall())

        cursor.execute("SELECT pr.idProvincia, pr.nombre, d.idDepartamento FROM pais p inner join departamento d on p.idPais = d.idPais inner join provincia pr on d.idDepartamento = pr.idDepartamento")
        usuario.append(cursor.fetchall())

    conexion.close()
    return usuario


# def registrar_jefe():
#     conexion=obtener_conexion()
    
#     with conexion.cursor() as cursor:
#         cursor.execute("insert into usuario values (usu, pass, v)")
        

#         cursor.execute("SELECT id from usuario where nomUsuario = usu and contraseña = pass")
#         id = cursor.fetchone()[0]

#         cursor.execute("insert into jefe values (..........., %s)", id)

#     conexion.commit()
#     conexion.close()