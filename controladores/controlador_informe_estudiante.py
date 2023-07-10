from bd import obtener_conexion


def listarInforme(id):
    conexion = obtener_conexion()
    informe = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT CONCAT(es.nombres ,' ', es.apellidos),es.codigo,es.semestreInicio, em.razonSocial, CONCAT(jef.nombre, ' ', jef.apellidos), jef.cargo,pr.fechaInicio,pr.fechaFin,pr.idPractica FROM ESTUDIANTE es inner join PRACTICA pr on es.idEstudiante = pr.idEstudiante inner join JEFE_INMEDIATO jef on jef.idJefe = pr.idJefe inner join EMPRESA em on em.idEmpresa = jef.idEmpresa inner join PLAN_ESTUDIO pl on pl.idPlanEs = es.idPlanEs inner join ESCUELA esc on esc.idEscuela = pl.idEscuela inner join LINEA_DESARROLLO li on li.idLinea = pr.idLinea where idPractica=%s",(id))
        informe = cursor.fetchone()
    conexion.close()
    return informe
def obtener_firmas(id):
    conexion = obtener_conexion()
    informe = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT urlFirmaEstudiante,urlFirmaResponsable from informe_inicial_estudiante where idInformeInicialEst=%s",(id))
        informe = cursor.fetchone()
    conexion.close()
    return informe
def obtener_ultimo_ie():
    conexion = obtener_conexion()
    idInformeDesempeño = None
    with conexion.cursor() as cursor:
        cursor.execute("SELECT COALESCE(MAX(idInformeInicialEst),0) as id from informe_inicial_estudiante")
        idInformeDesempeño = cursor.fetchone()
    conexion.close()
    return idInformeDesempeño
def obtener_idInformeInicial(id):
    conexion = obtener_conexion()
    idInformeDesempeño = None
    with conexion.cursor() as cursor:
        cursor.execute("SELECT idInformeInicialEst as id from objetivos_practica where idObjetivo=%s",(id))
        idInformeDesempeño = cursor.fetchone()
    conexion.close()
    return idInformeDesempeño
def obtener_informe_iniciales(id):
    conexion = obtener_conexion()
    informe = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT fechaEntrega,estado,idInformeInicialEst from INFORME_INICIAL_ESTUDIANTE where idPractica=%s",(id))
        informe = cursor.fetchone()
    conexion.close()
    return informe
def obtener_totalh(id):
    conexion = obtener_conexion()
    informe = []
    with conexion.cursor() as cursor:
        cursor.execute("select sum(NHoras) from plan_trabajo where idInformeInicialEst=%s",(id))
        informe = cursor.fetchone()
    conexion.close()
    return informe
def insertar_objetivos(objetivo,idi):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO objetivos_practica(objetivo, idInformeInicialEst) VALUES (%s,%s)",
                       (objetivo, idi))
    conexion.commit()
    conexion.close()
def modificar_objetivos(objetivo,idi):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE objetivos_practica set objetivo=%s where idObjetivo=%s) VALUES (%s,%s)",
                       (objetivo, idi))
    conexion.commit()
    conexion.close()    
def insertar_plan(nsem,fechai,fechaf,act,horas,id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO plan_trabajo(NSemana, fechaI,fechaF,actividad,NHoras,idInformeInicialEst) VALUES (%s,%s,%s,%s,%s,%s)",
                       (nsem,fechai,fechaf,act,horas,id))
    conexion.commit()
    conexion.close()
        
def obtener_objetivos(id):
    conexion = obtener_conexion()
    informe = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT objetivo,idInformeInicialEst from objetivos_practica where idInformeInicialEst=%s",(id))
        informe = cursor.fetchall()
    conexion.close()
    return informe
def eliminar_objetivos(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM objetivos_practica WHERE idInformeInicialEst=%s",(id))
        informe = cursor.fetchall()
    conexion.commit()
    conexion.close()

def obtener_plan(id):
    conexion = obtener_conexion()
    informe = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT nsemana, CONCAT(fechaI ,' al ', fechaF),actividad, NHoras from plan_trabajo where idInformeInicialEst=%s",(id))
        informe = cursor.fetchall()
    conexion.close()
    return informe
def obtener_plane(id):
    conexion = obtener_conexion()
    informe = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT nsemana, fechaI , fechaF,actividad, NHoras from plan_trabajo where idInformeInicialEst=%s",(id))
        informe = cursor.fetchall()
    conexion.close()
    return informe
def eliminar_plan(id):
    conexion = obtener_conexion()
    informe = []
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM plan_trabajo WHERE idInformeInicialEst=%s",(id))
        informe = cursor.fetchall()
    conexion.commit()
    conexion.close()
def obtener_informe_finales(id):
    conexion = obtener_conexion()
    informe = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT fechaEntrega,estado from INFORME_FINAL_ESTUDIANTE where idPractica=%s",(id))
        informe = cursor.fetchone()
    conexion.close()
    return informe
def obtener_informe_final_em(id):
    conexion = obtener_conexion()
    informe = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT fechaEntrega,estado from INFORME_FINAL_EMPRESA where idPractica=%s",(id))
        informe = cursor.fetchone()
    conexion.close()
    return informe
def obtener_informe_desemp(id):
    conexion = obtener_conexion()
    informe = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT fechaEntrega,estado from INFORME_DESEMPEÑO where idPractica=%s",(id))
        informe = cursor.fetchone()
    conexion.close()
    return informe
def obtener_informe_inicial_em(id):
    conexion = obtener_conexion()
    informe = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT fechaEntrega,estado from INFORME_INICIAL_EMPRESA where idPractica=%s",(id))
        informe = cursor.fetchone()
    conexion.close()
    return informe
def insertar_informe_inicial_estudiante(estado,urlFirmaE, urlFirmaJ, idPractica):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO INFORME_INICIAL_ESTUDIANTE(estado, fechaEntrega, urlFirmaEstudiante, urlFirmaResponsable, idPractica) VALUES (%s,now(),%s,%s,%s)",
                       (estado, urlFirmaE,urlFirmaJ, idPractica))
    conexion.commit()
    conexion.close()
def modificar_informe_inicial_estudiante(estado,urlFirmaE, urlFirmaJ, idPractica):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE INFORME_INICIAL_ESTUDIANTE set estado=%s, urlFirmaEstudiante=%s, urlFirmaResponsable=%s, where idPractica=%s",
                       (estado, urlFirmaE,urlFirmaJ, idPractica))
    conexion.commit()
    conexion.close()