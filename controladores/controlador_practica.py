from bd import obtener_conexion

def obtener_practica():
    conexion = obtener_conexion()
    practica = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT PRACTICA.idPractica, CONCAT(ESTUDIANTE.apellidos, ', ', ESTUDIANTE.nombres) AS estudiante, EMPRESA.razonSocial, LINEA_DESARROLLO.descripcion,PRACTICA.fechaInicio, PRACTICA.fechaFin, PRACTICA.horasPractica, CASE PRACTICA.estado WHEN 1 THEN 'Vigente' ELSE 'No vigente' END AS estado, PRACTICA.fechaLimite,case PRACTICA.modalidad when'P' then 'Presencial' else 'Virtual' end as modalidad, CONCAT(JEFE_INMEDIATO.apellidos, ', ', JEFE_INMEDIATO.nombre) AS jefe,ESTUDIANTE.codigo FROM PRACTICA INNER JOIN ESTUDIANTE ON PRACTICA.idEstudiante = ESTUDIANTE.idEstudiante INNER JOIN JEFE_INMEDIATO ON JEFE_INMEDIATO.idJefe = PRACTICA.idJefe INNER JOIN EMPRESA ON EMPRESA.idEmpresa = JEFE_INMEDIATO.idEmpresa INNER JOIN LINEA_DESARROLLO ON LINEA_DESARROLLO.idLinea = PRACTICA.idLinea WHERE PRACTICA.estadoEnvio='E' or PRACTICA.estadoEnvio='O' or PRACTICA.estadoEnvio='A';")
        practica = cursor.fetchall()
        print(practica)
    conexion.close()
    return practica

def obtener_practicaE(idE):
    conexion = obtener_conexion()
    practica = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT PRACTICA.idPractica, CONCAT(ESTUDIANTE.apellidos, ', ', ESTUDIANTE.nombres) AS estudiante, EMPRESA.razonSocial, LINEA_DESARROLLO.descripcion,PRACTICA.fechaInicio, PRACTICA.fechaFin, PRACTICA.horasPractica, CASE PRACTICA.estado WHEN 1 THEN 'Vigente' ELSE 'No vigente' END AS estado, PRACTICA.fechaLimite,case PRACTICA.modalidad when'P' then 'Presencial' else 'Virtual' end as modalidad, CONCAT(JEFE_INMEDIATO.apellidos, ', ', JEFE_INMEDIATO.nombre) AS jefe,ESTUDIANTE.codigo FROM PRACTICA INNER JOIN ESTUDIANTE ON PRACTICA.idEstudiante = ESTUDIANTE.idEstudiante INNER JOIN JEFE_INMEDIATO ON JEFE_INMEDIATO.idJefe = PRACTICA.idJefe INNER JOIN EMPRESA ON EMPRESA.idEmpresa = JEFE_INMEDIATO.idEmpresa INNER JOIN LINEA_DESARROLLO ON LINEA_DESARROLLO.idLinea = PRACTICA.idLinea WHERE ESTUDIANTE.idEstudiante=%s and (PRACTICA.estadoEnvio='G' or PRACTICA.estadoEnvio='E' or PRACTICA.estadoEnvio='A' or PRACTICA.estadoEnvio='O')",(idE))
        practica = cursor.fetchall()
        print(practica)
    conexion.close()
    return practica

def obtener_practicaID(id):
    conexion = obtener_conexion()
    practica = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT PRACTICA.idPractica,ESTUDIANTE.codigo,ESTUDIANTE.dni, CONCAT(ESTUDIANTE.apellidos, ', ', ESTUDIANTE.nombres) AS estudiante,plan_estudio.nombre, EMPRESA.razonSocial, LINEA_DESARROLLO.descripcion,PRACTICA.fechaInicio, PRACTICA.fechaFin, PRACTICA.horasPractica, CASE PRACTICA.estado WHEN 1 THEN 'Vigente' ELSE 'No vigente' END AS estado, PRACTICA.fechaLimite,case PRACTICA.modalidad when'P' then 'Presencial' else 'Virtual' end as modalidad, CONCAT(JEFE_INMEDIATO.apellidos, ', ', JEFE_INMEDIATO.nombre) AS jefe FROM PRACTICA INNER JOIN ESTUDIANTE ON PRACTICA.idEstudiante = ESTUDIANTE.idEstudiante INNER JOIN JEFE_INMEDIATO ON JEFE_INMEDIATO.idJefe = PRACTICA.idJefe INNER JOIN EMPRESA ON EMPRESA.idEmpresa = JEFE_INMEDIATO.idEmpresa INNER JOIN LINEA_DESARROLLO ON LINEA_DESARROLLO.idLinea = PRACTICA.idLinea INNER JOIN plan_estudio on estudiante.idPlanEs=plan_estudio.idPlanEs WHERE PRACTICA.idPractica=%s",(id))
        practica = cursor.fetchall()
        print(practica)
    conexion.close()
    return practica