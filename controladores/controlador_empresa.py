from bd import obtener_conexion

def insertar_empresa_nacional(razonSocial,direccion,ruc,telefono,telefono2,correo,idDistrito):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO EMPRESA(idEmpresa,razonSocial,direccion,ruc,telefono,telefono2,correo,idDistrito) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
                       (obtener_ultimoidEmpresa(),razonSocial,direccion,ruc,telefono,telefono2,correo,idDistrito))
    conexion.commit()
    conexion.close()

def insertar_empresa_internacional(razonSocial,direccion,ruc,telefono,telefono2,correo,idPais):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO EMPRESA(idEmpresa,razonSocial,direccion,ruc,telefono,telefono2,correo,idPais) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
                       (obtener_ultimoidEmpresa(),razonSocial,direccion,ruc,telefono,telefono2,correo,idPais))
    conexion.commit()
    conexion.close()

def obtener_ultimoidEmpresa():
    conexion = obtener_conexion()
    idEmpresa=None
    with conexion.cursor() as cursor:
        cursor.execute("SELECT COALESCE((MAX(idEmpresa)),0)+1 as idEmpresa from EMPRESA")
        idEmpresa = cursor.fetchone()
    conexion.close()
    return idEmpresa

def obtener_empresa():
    conexion = obtener_conexion()
    empresa = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT idEmpresa,razonSocial,ruc,telefono,correo FROM EMPRESA")
        empresa = cursor.fetchall()
        print(empresa)
    conexion.close()
    return empresa

def actualizar_empresa_nacional(razonSocial,direccion,ruc,telefono,telefono2,correo,idDistrito,idEmpresa):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE EMPRESA SET razonSocial = %s,direccion = %s,ruc = %s,telefono = %s,telefono2 = %s,correo = %s,idDistrito = %s, idPais = NULL WHERE idEmpresa = %s",
                       (razonSocial,direccion,ruc,telefono,telefono2,correo,idDistrito,idEmpresa))
    conexion.commit()
    conexion.close()

def actualizar_empresa_internacional(razonSocial,direccion,ruc,telefono,telefono2,correo,idPais,idEmpresa):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE EMPRESA SET razonSocial = %s,direccion = %s,ruc = %s,telefono = %s,telefono2 = %s,correo = %s,idPais = %s, idDistrito = NULL WHERE idEmpresa = %s",
                       (razonSocial,direccion,ruc,telefono,telefono2,correo,idPais,idEmpresa))
    conexion.commit()
    conexion.close()

def buscar_empresa(razonSocial):
    conexion = obtener_conexion()
    empresa = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM EMPRESA WHERE razonSocial LIKE ('%'||%s||'%')", (razonSocial,))
        empresa = cursor.fetchall()
    conexion.close()
    return empresa

def buscar_empresa_id(idEmpresa):
    conexion = obtener_conexion()
    empresa = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM EMPRESA WHERE idEmpresa = %s", (idEmpresa))
        empresa = cursor.fetchone()
    conexion.close()
    return empresa

def eliminar_empresa(idEmpresa):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM EMPRESA WHERE idEmpresa = %s", (idEmpresa))
    conexion.commit()
    conexion.close()

def listar_pais():
    conexion = obtener_conexion()
    pais = []
    with conexion.cursor() as cursor:
        cursor.execute("select idPais,nombre from PAIS")
        pais = cursor.fetchall()
    conexion.close()
    return pais

def nombrePais(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("select nombre from PAIS where idPais = %s",(id))
        pais = cursor.fetchone()
    conexion.close()
    return pais

def listar_departamento():
    conexion = obtener_conexion()
    dep = []
    with conexion.cursor() as cursor:
        cursor.execute("select nombre from DEPARTAMENTO")
        dep = cursor.fetchall()
    conexion.close()
    return dep

def listar_provincia(dep):
    conexion = obtener_conexion()
    prov = []
    with conexion.cursor() as cursor:
        cursor.execute("select p.nombre from PROVINCIA p inner join DEPARTAMENTO d  on p.idDepartamento = d.idDepartamento where d.nombre = %s",(dep))
        prov = cursor.fetchall()
    conexion.close()
    return prov

def listar_distrito(prov):
    conexion = obtener_conexion()
    dis = []
    with conexion.cursor() as cursor:
        cursor.execute("select d.idDistrito,d.nombre from DISTRITO d inner join PROVINCIA p on d.idProvincia = p.idProvincia where p.nombre = %s",(prov))
        dis = cursor.fetchall()
    conexion.close()
    return dis

def empresa_nacional(idDistrito):
    conexion = obtener_conexion()
    dis = []
    with conexion.cursor() as cursor:
        cursor.execute("select 'Perú', dep.nombre, p.nombre, dis.nombre, dis.idDistrito FROM DISTRITO dis INNER JOIN PROVINCIA p ON dis.idProvincia = p.idProvincia INNER JOIN DEPARTAMENTO dep ON p.idDepartamento = dep.idDepartamento where dis.idDistrito = %s ",(idDistrito))
        dis = cursor.fetchone()
    conexion.close()
    return dis