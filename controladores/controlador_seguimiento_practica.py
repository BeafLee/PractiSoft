from bd import obtener_conexion

def insertar_seguimiento_practica(fechaCreacion, horaCreacion, tipo, observacion, idPractica):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO SEGUIMIENTO_PRACTICA(fechaCreacion, horaCreacion, tipo, observacion, idPractica) VALUES (%s, %s, %s, %s, %s)",
                       (fechaCreacion, horaCreacion, tipo, observacion, idPractica))
    conexion.commit()
    conexion.close()

def obtener_idpractica(id):
    conexion = obtener_conexion()
    juego = None
    with conexion.cursor() as cursor:
        cursor.execute("SELECT idPractica FROM PRACTICA where idPractica = %s",(id,))
        juego = cursor.fetchone()
    conexion.close()
    return juego

def obtener_datos(idPractica):
    conexion = obtener_conexion()
    juego = None
    with conexion.cursor() as cursor:
        cursor.execute("select e.codigo, CONCAT(e.nombres, ' ' , e.apellidos) as nombre_completo, em.ruc, em.razonSocial, p.idPractica from PRACTICA p inner join ESTUDIANTE e on p.idEstudiante = e.idEstudiante inner join JEFE_INMEDIATO j on p.idJefe = j.idJefe inner join EMPRESA em on em.idEmpresa = j.idEmpresa where p.idPractica = %s",(idPractica,))
        juego = cursor.fetchone()
    conexion.close()
    return juego

def obtener_ultimoid():
    conexion = obtener_conexion()
    idSeguimiento=None
    with conexion.cursor() as cursor:
        cursor.execute("SELECT COALESCE((MAX(idSeguimiento)),0)+1 as idSeguimiento from SEGUIMIENTO_PRACTICA")
        idSeguimiento = cursor.fetchone()
    conexion.close()
    return idSeguimiento

def obtener_seguimiento_practica(id):
    conexion = obtener_conexion()
    seguimiento_practica = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT se.idSeguimiento, CONCAT(e.nombres, ' ' , e.apellidos) as nombre_completo, em.razonSocial, CASE se.tipo WHEN 'P' THEN 'Presencial' WHEN 'V' THEN 'Virtual' ELSE 'Otro valor' END AS tipo, se.fechaCreacion, se.horaCreacion FROM SEGUIMIENTO_PRACTICA se INNER JOIN PRACTICA p ON p.idPractica = se.idPractica INNER JOIN JEFE_INMEDIATO j ON j.idJefe = p.idJefe INNER JOIN ESTUDIANTE e ON e.idEstudiante = p.idEstudiante INNER JOIN EMPRESA em ON em.idEmpresa = j.idEmpresa where p.idPractica = %s",(id,))
        seguimiento_practica = cursor.fetchall()
    conexion.close()
    return seguimiento_practica

def obtener_seguimiento_practica_total(idSeguimiento):
    conexion = obtener_conexion()
    seguimiento_practica = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT CONCAT(e.nombres, ' ' , e.apellidos) as nombre_completo, em.razonSocial, CASE se.tipo WHEN 'P' THEN 'Presencial' WHEN 'V' THEN 'Virtual' ELSE 'Otro valor' END AS tipo , se.fechaCreacion, se.horaCreacion, se.observacion, p.idPractica FROM SEGUIMIENTO_PRACTICA se INNER JOIN PRACTICA p ON p.idPractica = se.idPractica INNER JOIN JEFE_INMEDIATO j ON j.idJefe = p.idJefe INNER JOIN ESTUDIANTE e ON e.idEstudiante = p.idEstudiante INNER JOIN EMPRESA em ON em.idEmpresa = j.idEmpresa where se.idSeguimiento = %s", (idSeguimiento,))
        seguimiento_practica = cursor.fetchone()
    conexion.close()
    return seguimiento_practica


