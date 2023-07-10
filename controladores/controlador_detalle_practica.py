from bd import obtener_conexion

def listar_detalle_practica(id):
    conexion = obtener_conexion()
    facultad = []
    with conexion.cursor() as cursor:
        cursor.execute(" SELECT P.fechaInicio,P.fechaFin,P.horasPractica,P.estado,P.modalidad,SE.nombreSe,SE.nombreSe,E.codigo,E.apellidos,E.nombres,E.dni,PE.nombre,EM.razonSocial,EM.ruc,CONCAT(JI.nombre,' ',JI.apellidos) as jefe, P.idPractica FROM PRACTICA P INNER JOIN ESTUDIANTE E ON P.idEstudiante=E.idEstudiante INNER JOIN JEFE_INMEDIATO JI ON JI.idJefe=P.idJefe INNER JOIN EMPRESA EM ON EM.idEmpresa=JI.idEmpresa INNER JOIN SEMESTRE SE on SE.idSemestre=P.idSemestreIn INNER JOIN PLAN_ESTUDIO PE ON PE.idPlanes=E.idPlanes WHERE P.idPractica = %s", (id,))
        facultad = cursor.fetchone()
    conexion.close()
    return facultad

def obtener_tipoUsuario(id):
    conexion = obtener_conexion()
    tipoUsuario=None
    with conexion.cursor() as cursor:
        cursor.execute("SELECT nombPerfil from TIPO_USUARIO where idTipoU=%s", (id,))
        tipoUsuario = cursor.fetchone()
    conexion.close()
    return tipoUsuario