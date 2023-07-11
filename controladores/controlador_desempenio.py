from bd import obtener_conexion

def listar_desempenio(id):
    conexion = obtener_conexion()
    informe = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT CONCAT(es.nombres ,' ', es.apellidos), esc.nombre, CONCAT(pr.fechaInicio, ' al ', pr.fechaFin), li.descripcion, em.razonSocial, em.direccion, CONCAT(jef.nombre, ' ', jef.apellidos), jef.correo, pr.idPractica FROM ESTUDIANTE es inner join PRACTICA pr on es.idEstudiante = pr.idEstudiante inner join JEFE_INMEDIATO jef on jef.idJefe = pr.idJefe inner join EMPRESA em on em.idEmpresa = jef.idEmpresa inner join PLAN_ESTUDIO pl on pl.idPlanEs = es.idPlanEs inner join ESCUELA esc on esc.idEscuela = pl.idEscuela inner join LINEA_DESARROLLO li on li.idLinea = pr.idLinea WHERE pr.idPractica = %s", (id,))
        informe = cursor.fetchone()
    conexion.close()
    return informe

def listar_todo_desempenio(id):
    conexion = obtener_conexion()
    informe = []
    with conexion.cursor() as cursor:
        cursor.execute("select * from INFORME_DESEMPEÑO where idPractica = %s",(id,))
        informe = cursor.fetchone()
    conexion.close()
    return informe

def insertar_desempenio(est, re, pro, com, tra, comp, org, pun, con, url, idp):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO `informe_desempeño`(`estado`, `fechaEntrega`, `responsabilidad`, `proactividad`, `comunicacionAsertiva`, `trabajoEquipo`, `compromisoCalidad`, `organizacionTrabajo`, `puntualidadAsistencia`, `conclusiones`, `urlFirmaResponsable`, `idPractica`) VALUES ( %s, now(), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                        (est, re, pro, com, tra, comp, org, pun, con, url,  idp))
    conexion.commit()
    conexion.close()
def modificar_desempenio(est, re, pro, com, tra, comp, org, pun, con, url, idp):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE informe_desempeño set estado=%s, responsabilidad=%s, proactividad=%s, comunicacionAsertiva=%s, trabajoEquipo=%s, compromisoCalidad=%s, organizacionTrabajo=%s, puntualidadAsistencia=%s, conclusiones=%s, urlFirmaResponsable=%s where idPractica=%s",
                        (est, re, pro, com, tra, comp, org, pun, con, url,  idp))
    conexion.commit()
    conexion.close()
def obtener_ultimo_desempenio():
    conexion = obtener_conexion()
    idInformeDesempeño = None
    with conexion.cursor() as cursor:
        cursor.execute("SELECT MAX(idInformeDesempeño) as idInformeDesempeño from INFORME_DESEMPEÑO")
        idInformeDesempeño = cursor.fetchone()
    conexion.close()
    return idInformeDesempeño


def insertar_resultado(nom, esc, idi):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO `RESULTADOS`(`nombreResultado`, `escala`, `idInformeDesempeño`) VALUES (%s, %s, %s)",
                        (nom, esc, idi))
    conexion.commit()
    conexion.close()
def eliminar_resultados(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM resultados WHERE idInformeDesempeño=%s",(id))
    conexion.commit()
    conexion.close()
def obtener_resultado(id):
    conexion = obtener_conexion()
    resultado = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT nombreResultado, escala FROM RESULTADOS where idInformeDesempeño = %s",(id,))
        resultado = cursor.fetchall()

    conexion.close()
    return resultado

def observar_informe(observacion, idPractica, idInformeDesempeño):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE INFORME_DESEMPEÑO SET estado='O', observacion = %s WHERE idPractica = %s and idInformeDesempeño = %s",
                       (observacion, idPractica, idInformeDesempeño))
    conexion.commit()
    conexion.close()

def aceptar_informe(idPractica, idInformeDesempeño):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE INFORME_DESEMPEÑO SET estado='A', observacion = '' WHERE idPractica = %s and idInformeDesempeño = %s",
                       (idPractica, idInformeDesempeño))
    conexion.commit()
    conexion.close()