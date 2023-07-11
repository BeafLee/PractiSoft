from bd import obtener_conexion

def obtener_practica():
    conexion = obtener_conexion()
    practica = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT PRACTICA.idPractica, CONCAT(ESTUDIANTE.apellidos, ', ', ESTUDIANTE.nombres) AS estudiante, EMPRESA.razonSocial, LINEA_DESARROLLO.descripcion,PRACTICA.fechaInicio, PRACTICA.fechaFin, PRACTICA.horasPractica, CASE PRACTICA.estadoPractica WHEN 'I' THEN 'Inicializado' WHEN 'P' THEN 'En proceso' WHEN 'E'THEN 'En espera' ELSE 'Finalizado' END AS estadoPractica, PRACTICA.fechaLimite,case PRACTICA.modalidad when'P' then 'Presencial' else 'Virtual' end as modalidad, CONCAT(JEFE_INMEDIATO.apellidos, ', ', JEFE_INMEDIATO.nombre) AS jefe,ESTUDIANTE.codigo,PRACTICA.estadoEnvio FROM PRACTICA INNER JOIN ESTUDIANTE ON PRACTICA.idEstudiante = ESTUDIANTE.idEstudiante INNER JOIN JEFE_INMEDIATO ON JEFE_INMEDIATO.idJefe = PRACTICA.idJefe INNER JOIN EMPRESA ON EMPRESA.idEmpresa = JEFE_INMEDIATO.idEmpresa INNER JOIN LINEA_DESARROLLO ON LINEA_DESARROLLO.idLinea = PRACTICA.idLinea WHERE PRACTICA.estadoEnvio='E' or PRACTICA.estadoEnvio='O' or PRACTICA.estadoEnvio='A';")
        practica = cursor.fetchall()
        print(practica)
    conexion.close()
    return practica

def obtener_practicaE(idE):
    conexion = obtener_conexion()
    practica = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT PRACTICA.idPractica, CONCAT(ESTUDIANTE.apellidos, ', ', ESTUDIANTE.nombres) AS estudiante, EMPRESA.razonSocial, LINEA_DESARROLLO.descripcion,PRACTICA.fechaInicio, PRACTICA.fechaFin, PRACTICA.horasPractica, CASE PRACTICA.estadoPractica WHEN 'I' THEN 'Inicializado' WHEN 'P' THEN 'En proceso' WHEN 'E'THEN 'En espera' ELSE 'Finalizado' END AS estadoPractica, PRACTICA.fechaLimite,case PRACTICA.modalidad when'P' then 'Presencial' else 'Virtual' end as modalidad, CONCAT(JEFE_INMEDIATO.apellidos, ', ', JEFE_INMEDIATO.nombre) AS jefe,ESTUDIANTE.codigo,CASE PRACTICA.estadoEnvio WHEN 'G' THEN 'GUARDADO' WHEN 'E' THEN 'ENVIADO' WHEN 'A' THEN 'APROBADO' WHEN 'O' THEN 'OBSERVADO' ELSE'N' END AS ESTADO_ENVIO FROM PRACTICA INNER JOIN ESTUDIANTE ON PRACTICA.idEstudiante = ESTUDIANTE.idEstudiante INNER JOIN JEFE_INMEDIATO ON JEFE_INMEDIATO.idJefe = PRACTICA.idJefe INNER JOIN EMPRESA ON EMPRESA.idEmpresa = JEFE_INMEDIATO.idEmpresa INNER JOIN LINEA_DESARROLLO ON LINEA_DESARROLLO.idLinea = PRACTICA.idLinea WHERE ESTUDIANTE.idEstudiante=%s",(idE))
        practica = cursor.fetchall()
        print(practica)
    conexion.close()
    return practica

def obtener_practicaID(id):
    conexion = obtener_conexion()
    practica = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT PRACTICA.idPractica,ESTUDIANTE.codigo,ESTUDIANTE.dni, CONCAT(ESTUDIANTE.apellidos, ', ', ESTUDIANTE.nombres) AS estudiante,plan_estudio.nombre, EMPRESA.razonSocial, LINEA_DESARROLLO.descripcion,PRACTICA.fechaInicio, PRACTICA.fechaFin, PRACTICA.horasPractica, CASE PRACTICA.estadoPractica WHEN 'I' THEN 'Inicializado' WHEN 'P' THEN 'En proceso' WHEN 'E'THEN 'En espera' ELSE 'Finalizado' END AS estadoPractica, PRACTICA.fechaLimite,case PRACTICA.modalidad when'P' then 'Presencial' else 'Virtual' end as modalidad, CONCAT(JEFE_INMEDIATO.apellidos, ', ', JEFE_INMEDIATO.nombre) AS jefe FROM PRACTICA INNER JOIN ESTUDIANTE ON PRACTICA.idEstudiante = ESTUDIANTE.idEstudiante INNER JOIN JEFE_INMEDIATO ON JEFE_INMEDIATO.idJefe = PRACTICA.idJefe INNER JOIN EMPRESA ON EMPRESA.idEmpresa = JEFE_INMEDIATO.idEmpresa INNER JOIN LINEA_DESARROLLO ON LINEA_DESARROLLO.idLinea = PRACTICA.idLinea INNER JOIN plan_estudio on estudiante.idPlanEs=plan_estudio.idPlanEs WHERE PRACTICA.idPractica=%s",(id))
        practica = cursor.fetchall()
        print(practica)
    conexion.close()
    return practica

def obtener_EstudianteUs(id):
    conexion = obtener_conexion()
    practica = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT idEstudiante FROM USUARIO us INNER JOIN ESTUDIANTE es ON us.idUsuario=es.idUsuario  WHERE us.idUsuario=%s",(id))
        practica = cursor.fetchall()
        print(practica)
    conexion.close()
    return practica

def EnviarPractica(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE PRACTICA SET estadoEnvio='E' WHERE idPractica = %s",
                       (id))
    conexion.commit()
    conexion.close()

def obtener_estado(id):
    conexion = obtener_conexion()
    estado = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT CASE PRACTICA.estadoPractica WHEN 'I' THEN 'Inicializado' WHEN 'P' THEN 'En proceso' WHEN 'E'THEN 'En espera' ELSE 'Finalizado' END AS estadoPractica FROM PRACTICA PRACTICA WHERE PRACTICA.idPractica = %s", (id,))
        estado = cursor.fetchone()
    conexion.close()
    return estado