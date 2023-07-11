from bd import obtener_conexion

def buscar_id(idInformeFinalEmp):
    conexion = obtener_conexion()
    informe = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT EM.razonSocial,CONCAT(j.nombre,' ',j.apellidos) AS responsable,j.cargo,CONCAT(ES.nombres,' ',ES.apellidos)AS estudiante,PR.fechaInicio,PR.fechaFin,ife.urlFirmaResponsable,IFE.urlSelloEmpresa,IFE.* from informe_final_empresa IFE INNER JOIN practica PR ON PR.idPractica=IFE.idPractica inner join jefe_inmediato j ON J.idJefe=PR.idJefe INNER JOIN empresa EM ON EM.idEmpresa=j.idEmpresa INNER JOIN estudiante ES ON ES.idEstudiante=PR.idEstudiante WHERE IFE.idInformeFinalEmpresa=%s", (idInformeFinalEmp,))
        informe = cursor.fetchone()
    conexion.close()
    return informe

def buscar_valoracion(idInformeFinalEmp):
    conexion = obtener_conexion()
    informe = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT aspectoValoracion FROM valoracion where idInformeFinalEmpresa=%s", (idInformeFinalEmp,))
        informe = cursor.fetchall()
    conexion.close()
    return informe

############################################################################################

def infoPlantilla(idPractica):
    conexion = obtener_conexion()
    info = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT E.razonSocial, CONCAT(J.nombre,' ',J.apellidos), J.cargo, CONCAT(ES.nombres,' ',ES.apellidos), P.fechaInicio, P.fechaFIN,p.idPractica FROM practica P INNER JOIN jefe_inmediato J ON J.idJefe=P.idJefe INNER JOIN empresa E ON E.idEmpresa=J.idEmpresa INNER JOIN estudiante ES ON ES.idEstudiante=P.idEstudiante WHERE p.idPractica=%s",(idPractica))
        info = cursor.fetchone()
    conexion.close()
    return info

def insertar_informe_final_empresa(idInformeFinalEmpresa,estado,fechaEntrega,urlFirmaResponsable,urlSelloEmpresa, observacion,idPractica):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO informe_final_empresa (idInformeFinalEmpresa,estado, fechaEntrega, urlFirmaResponsable, urlSelloEmpresa, observacion, idPractica) VALUES (%s,%s,%s,%s,%s,%s,%s)",(idInformeFinalEmpresa,estado,fechaEntrega,urlFirmaResponsable,urlSelloEmpresa, observacion,idPractica))
    conexion.commit()
    conexion.close()

def insertar_valoracion(valoracion,id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO valoracion (aspectoValoracion, idInformeFinalEmpresa) VALUES (%s,%s)",(valoracion,id))
    conexion.commit()
    conexion.close()

def obtener_ultimo_ifem():
    conexion = obtener_conexion()
    idIFEM = None
    with conexion.cursor() as cursor:
        cursor.execute("SELECT MAX(idInformeFinalEmpresa) as idInformeFinalEmpresa from informe_final_empresa;")
        idIFEM = cursor.fetchone()
    conexion.close()
    return idIFEM


def actualizar_informe_final_empresa(estado,urlFirmaResponsable,urlSelloEmpresa,idInformeFinalEmpresa):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE informe_final_empresa SET estado=%s,urlFirmaResponsable = %s,urlSelloEmpresa = %s WHERE idInformeFinalEmpresa = %s",
                       (estado,urlFirmaResponsable,urlSelloEmpresa,idInformeFinalEmpresa))
    conexion.commit()
    conexion.close()

def actualizar_valoracion(aspectoValoracion,idInformeFinalEmpresa):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE valoracion SET aspectoValoracion = %s WHERE idInformeFinalEmpresa = %s",
                       (aspectoValoracion,idInformeFinalEmpresa))
    conexion.commit()
    conexion.close()  

def eliminar_valoracion(idInformeFinalEmpresa):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM valoracion WHERE idInformeFinalEmpresa = %s",
                       (idInformeFinalEmpresa))
    conexion.commit()
    conexion.close()  

def buscar_sello(idInformeFinalEmp):
    conexion = obtener_conexion()
    informe = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT urlSelloEmpresa FROM informe_final_empresa where idInformeFinalEmpresa=%s", (idInformeFinalEmp,))
        informe = cursor.fetchall()
    conexion.close()
    return informe

def buscar_firma(idInformeFinalEmp):
    conexion = obtener_conexion()
    informe = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT urlFirmaResponsable FROM informe_final_empresa where idInformeFinalEmpresa=%s", (idInformeFinalEmp,))
        informe = cursor.fetchall()
    conexion.close()
    return informe  

def actualizar_obs_informe_final_empresa(estado,obs,idInformeFinalEmp):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE informe_final_empresa SET estado=%s,observacion = %s WHERE idInformeFinalEmpresa = %s",
                       (estado,obs,idInformeFinalEmp))
    conexion.commit()
    conexion.close()