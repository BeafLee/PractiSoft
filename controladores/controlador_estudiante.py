from bd import obtener_conexion



def obtener_estudiante():
    conexion = obtener_conexion()
    estudiante = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT idEstudiante,codigo,nombres,apellidos,cicloActual,semestreInicio,dni,correo1,correo2,telefono1,telefono2,direccion, CASE estado WHEN 'A' THEN 'Apto' ELSE 'No apto' END AS estado, idPlanEs,idCiudad,idUsuario FROM ESTUDIANTE")
        estudiante = cursor.fetchall()

    conexion.close()
    return estudiante


def obtener_estudiante_index(limit,offset):
    conexion=obtener_conexion()
    estudiante=[]
    with conexion.cursor() as cursor:
        cursor.execute("SELECT idEstudiante,codigo,nombres,apellidos,cicloActual,semestreInicio,dni,correo1,correo2,telefono1,telefono2,direccion, CASE estado WHEN 'A' THEN 'Apto' ELSE 'No apto' END AS estado, idPlanEs,idCiudad,idUsuario FROM ESTUDIANTE limit {} offset {}".format(limit, offset))
        estudiante = cursor.fetchall()

    conexion.close()
    return estudiante



def dar_baja(idEstudiante):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE ESTUDIANTE SET estado='N' WHERE idEstudiante = %s",
                       (idEstudiante))
    conexion.commit()
    conexion.close()
def dar_alta(idEstudiante):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE ESTUDIANTE SET estado='A' WHERE idEstudiante = %s",
                       (idEstudiante))
    conexion.commit()
    conexion.close()

def buscar_semestre(nombreSe):
    conexion = obtener_conexion()
    semestres = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT idSemestre,nombreSe,DATE_FORMAT(fechaI, '%%d-%%m-%%Y')as fechaI,DATE_FORMAT(fechaF, '%%d-%%m-%%Y')as fechaF ,CASE estado WHEN 1 THEN 'Vigente' ELSE 'No vigente' END AS estado FROM SEMESTRE WHERE nombreSe LIKE concat('%%', %s, '%%')", (nombreSe))
        semestres = cursor.fetchall()
    conexion.close()
    return semestres

def buscar_estudiante_id(idEstudiante):
    conexion = obtener_conexion()
    estudiante = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT idEstudiante,codigo,nombres,apellidos,cicloActual,semestreInicio,dni,correo1,correo2,telefono1,telefono2,direccion, CASE estado WHEN 'A' THEN 'Apto' ELSE 'NO APTO' END AS estado, idPlanEs,idCiudad,idUsuario FROM ESTUDIANTE WHERE idEstudiante = %s", (idEstudiante,))
        estudiante = cursor.fetchone()
    conexion.close()
    return estudiante
