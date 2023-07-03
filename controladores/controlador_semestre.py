from bd import obtener_conexion

def insertar_semestre(nombreSe,fechaI, fechaF, estado):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO SEMESTRE(nombreSe,fechaI, fechaF, estado) VALUES (%s,%s, %s, %s)",
                       (nombreSe,fechaI, fechaF, estado))
    conexion.commit()
    conexion.close()

# def obtener_ultimoidSemestre():
#     conexion = obtener_conexion()
#     idSemestre=None
#     with conexion.cursor() as cursor:
#         cursor.execute("SELECT COALESCE((MAX(idSemestre)),0)+1 as idSemestre from semestre")
#         idSemestre = cursor.fetchone()
#     conexion.close()
#     return idSemestre

def obtener_semestre():
    conexion = obtener_conexion()
    semestre = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT idSemestre,nombreSe,DATE_FORMAT(fechaI, '%d-%m-%Y')as fechaI,DATE_FORMAT(fechaF, '%d-%m-%Y')as fechaF ,CASE estado WHEN 'V' THEN 'Vigente' ELSE 'No vigente' END AS estado FROM SEMESTRE")
        semestre = cursor.fetchall()

    conexion.close()
    return semestre
def obtener_semestre_index(limit,offset):
    conexion=obtener_conexion()
    semestre=[]
    with conexion.cursor() as cursor:
        cursor.execute("SELECT idSemestre,nombreSe,DATE_FORMAT(fechaI, '%d-%m-%Y')as fechaI,DATE_FORMAT(fechaF, '%d-%m-%Y')as fechaF ,CASE estado WHEN 'V' THEN 'Vigente' ELSE 'No vigente' END AS estado FROM SEMESTRE limit {} offset {}".format(limit, offset))
        semestre = cursor.fetchall()

    conexion.close()
    return semestre
def actualizar_semestre(nombreSe,fechaI, fechaF, estado, idSemestre):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE SEMESTRE SET nombreSe= %s, fechaI= %s, fechaF= %s, estado=%s WHERE idSemestre = %s",
                       (nombreSe,fechaI, fechaF, estado, idSemestre))
    conexion.commit()
    conexion.close()


def dar_baja(idSemestre):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE SEMESTRE SET estado='N' WHERE idSemestre = %s",
                       (idSemestre))
    conexion.commit()
    conexion.close()
def dar_alta(idSemestre):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE SEMESTRE SET estado='V' WHERE idSemestre = %s",
                       (idSemestre))
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

def buscar_semestre_id(idSemestre):
    conexion = obtener_conexion()
    semestre = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT idSemestre, nombreSe, fechaI, fechaF, estado FROM SEMESTRE WHERE idSemestre = %s", (idSemestre,))
        semestre = cursor.fetchone()
    conexion.close()
    return semestre

def eliminar_semestre(idSemestre):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM SEMESTRE WHERE idSemestre = %s", (idSemestre))
    conexion.commit()
    conexion.close()