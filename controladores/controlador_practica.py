from bd import obtener_conexion

def obtener_practica():
    conexion = obtener_conexion()
    practica = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT PRACTICA.idPractica, CONCAT(ESTUDIANTE.apellidos, ', ', ESTUDIANTE.nombres) AS estudiante, EMPRESA.razonSocial, LINEA_DESARROLLO.descripcion,PRACTICA.fechaInicio, PRACTICA.fechaFin, PRACTICA.horasPractica, CASE PRACTICA.estado WHEN 1 THEN 'Vigente' ELSE 'No vigente' END AS estado, PRACTICA.fechaLimite,case PRACTICA.modalidad when'P' then 'Presencial' else 'Virtual' end as modalidad, CONCAT(JEFE_INMEDIATO.apellidos, ', ', JEFE_INMEDIATO.nombre) AS jefe FROM PRACTICA INNER JOIN ESTUDIANTE ON PRACTICA.idEstudiante = ESTUDIANTE.idEstudiante INNER JOIN JEFE_INMEDIATO ON JEFE_INMEDIATO.idJefe = PRACTICA.idJefe INNER JOIN EMPRESA ON EMPRESA.idEmpresa = JEFE_INMEDIATO.idEmpresa INNER JOIN LINEA_DESARROLLO ON LINEA_DESARROLLO.idLinea = PRACTICA.idLinea;")
        practica = cursor.fetchall()
        print(practica)
    conexion.close()
    return practica