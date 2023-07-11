from bd import obtener_conexion


def obtener_estudiante(id):
    conexion = obtener_conexion()
    estudiante = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT es.idEstudiante, es.codigo, es.dni, CONCAT(es.apellidos, ' ', es.nombres) as nombre,pl.nombre from USUARIO usu inner join ESTUDIANTE es on es.idUsuario=usu.idUsuario inner join PLAN_ESTUDIO pl on pl.idPlanEs=es.idPlanEs where es.idUsuario=%s",(id))
        estudiante = cursor.fetchone()
    conexion.close()
    return estudiante

def obtener_empresa():
    conexion = obtener_conexion()
    empresa = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT em.razonSocial,em.idEmpresa,em.ruc, CONCAT(ji.apellidos, ' ', ji.nombre) as nombre  from EMPRESA em inner join JEFE_INMEDIATO ji on ji.idEmpresa=em.idEmpresa")
        empresa = cursor.fetchall()
        print(empresa)
    conexion.close()
    return empresa

def buscar_empresa_datos(nombre):
    conexion = obtener_conexion()
    empresa = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT em.ruc, CONCAT(ji.apellidos, ' ', ji.nombre) as nombre  from EMPRESA em inner join JEFE_INMEDIATO ji on ji.idEmpresa=em.idEmpresa where em.razonSocial= %s", (nombre))
        empresa = cursor.fetchone()
    conexion.close()
    return empresa

def semestre_actual():
    conexion = obtener_conexion()
    semestreA = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT nombreSe,idsemestre  from SEMESTRE where estado= 'V'")
        semestreA = cursor.fetchone()
    conexion.close()
    return semestreA

def obtenerSemestres():
    conexion = obtener_conexion()
    semestreF = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT nombreSe,idsemestre  from SEMESTRE")
        semestreF = cursor.fetchall()

    conexion.close()
    return semestreF

def obtener_linea_desarrollo():
    conexion = obtener_conexion()
    linea = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT *  from LINEA_DESARROLLO")
        linea = cursor.fetchall()

    conexion.close()
    return linea

def buscar_id_jefe(nombre,ruc):
    conexion = obtener_conexion()
    jefe = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT ji.idJefe from  JEFE_INMEDIATO ji inner join EMPRESA em on em.idEmpresa=ji.idEmpresa where CONCAT(ji.apellidos, ' ', ji.nombre)= %s AND em.ruc= %s" , (nombre,ruc))
        jefe = cursor.fetchone()
    conexion.close()
    return jefe

def obtener_id_personal():
    conexion = obtener_conexion()
    personal = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT idPersonal from  PERSONAL")
        personal = cursor.fetchone()
    conexion.close()
    return personal

def obtener_id_linea(nombre):
    conexion = obtener_conexion()
    linea = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT idLinea from  LINEA_DESARROLLO where descripcion=%s ",(nombre))
        linea = cursor.fetchone()
    conexion.close()
    return linea
def obtener_id_semestre(nombre):
    conexion = obtener_conexion()
    semestre = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT idSemestre from  SEMESTRE where nombreSe=%s ",(nombre))
        semestre = cursor.fetchone()
    conexion.close()
    return semestre

def obtener_ultimoidPractica():
    conexion = obtener_conexion()
    idEmpresa=None
    with conexion.cursor() as cursor:
        cursor.execute("SELECT COALESCE((MAX(idPractica)),0)+1 as idPractica from PRACTICA")
        idEmpresa = cursor.fetchone()
    conexion.close()
    return idEmpresa

def insertar_practica(fechaInicio ,fechaFin,horasPractica,fechaLimite,modalidad ,idEstudiante ,idJefe ,idPersonal ,idLinea ,idSemestreIn,idSemestreFi):
    conexion = obtener_conexion()

    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO PRACTICA(idPractica ,fechaInicio ,fechaFin,horasPractica,fechaLimite,modalidad ,idEstudiante ,idJefe ,idPersonal ,idLinea ,idSemestreIn,idSemestreFi,estado,esConvalidado,estadoPractica,estadoEnvio ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'P','N','I','G')",
                       (obtener_ultimoidPractica(),fechaInicio ,fechaFin,horasPractica,fechaLimite,modalidad ,idEstudiante ,idJefe ,idPersonal ,idLinea ,idSemestreIn,idSemestreFi))
    conexion.commit()
    conexion.close()

def enviar_practica(fechaInicio ,fechaFin,horasPractica,fechaLimite,modalidad ,idEstudiante ,idJefe ,idPersonal ,idLinea ,idSemestreIn,idSemestreFi):
    conexion = obtener_conexion()

    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO PRACTICA(idPractica ,fechaInicio ,fechaFin,horasPractica,fechaLimite,modalidad ,idEstudiante ,idJefe ,idPersonal ,idLinea ,idSemestreIn,idSemestreFi,estado,esConvalidado,estadoPractica,estadoEnvio ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'P','N','I','E')",
                       (obtener_ultimoidPractica(),fechaInicio ,fechaFin,horasPractica,fechaLimite,modalidad ,idEstudiante ,idJefe ,idPersonal ,idLinea ,idSemestreIn,idSemestreFi))
    conexion.commit()
    conexion.close()










def actualizar_facultad(nombre,descripcion, estado, id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE facultad SET nombre= %s, descripcion = %s, estado=%s WHERE id = %s",
                       (nombre, descripcion, estado, id))
    conexion.commit()
    conexion.close()


def dar_baja(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE facultad SET estado=0 WHERE id = %s",
                       (id))
    conexion.commit()
    conexion.close()
def dar_alta(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE facultad SET estado=1 WHERE id = %s",
                       (id))
    conexion.commit()
    conexion.close()
def buscar_facultad(nombre):
    conexion = obtener_conexion()
    facultad = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id,nombre, descripcion, estado FROM facultad WHERE nombre LIKE ('%'||%s||'%')", (nombre,))
        facultad = cursor.fetchall()
    conexion.close()
    return facultad

def buscar_facultad_id(id):
    conexion = obtener_conexion()
    facultad = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id,nombre, descripcion, estado FROM facultad WHERE id = %s", (id,))
        facultad = cursor.fetchone()
    conexion.close()
    return facultad

def eliminar_facultad(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM facultad WHERE id = %s", (id))
    conexion.commit()
    conexion.close()

def actualizar_practica(fechaI,fechaF,horas,fechaL,id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE PRACTICA SET fechaInicio=%s ,fechaFin=%s ,horasPractica=%s, fechaLimite=%s WHERE idPractica = %s",
                       (fechaI,fechaF,horas,fechaL,id))
    conexion.commit()
    conexion.close()