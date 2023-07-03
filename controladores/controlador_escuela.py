from bd import obtener_conexion

def insertar_escuela(nombre,descripcion, estado, nombre1):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO ESCUELA(idEscuela,nombre,descripcion, estado, idFacultad) VALUES (%s,%s,%s, %s, %s)",
                       (obtener_ultimoid(),nombre,descripcion, estado, obtener_idfacultad(nombre1)))
    conexion.commit()
    conexion.close()

def obtener_idfacultad(nombre):
    conexion = obtener_conexion()
    id=None
    with conexion.cursor() as cursor:
        cursor.execute("SELECT idFacultad from FACULTAD WHERE nombre = %s",
                       (nombre))
        id = cursor.fetchone()
    conexion.close()
    return id


def obtener_ultimoid():
    conexion = obtener_conexion()
    id=None
    with conexion.cursor() as cursor:
        cursor.execute("SELECT COALESCE((MAX(idEscuela)),0)+1 as idEscuela from ESCUELA")
        id = cursor.fetchone()
    conexion.close()
    return id


def listarFacultades():
    conexion = obtener_conexion()
    facultad=[]
    with conexion.cursor() as cursor:
        cursor.execute("SELECT nombre from FACULTAD")
        facultad = cursor.fetchall()
    conexion.close()
    return facultad


def obtener_escuela():
    conexion = obtener_conexion()
    escuela = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT idEscuela,e.nombre,e.descripcion,CASE e.estado WHEN 'V' THEN 'Vigente' ELSE 'No vigente' END AS estado, f.nombre FROM ESCUELA e INNER JOIN FACULTAD f on e.idFacultad=f.idFacultad")
        escuela = cursor.fetchall()
        print(escuela)
    conexion.close()
    return escuela

def obtener_escuela_index(limit,offset):
    conexion=obtener_conexion()
    escuela=[]
    with conexion.cursor() as cursor:
        cursor.execute("SELECT idEscuela,nombre,descripcion, CASE estado WHEN 'V' THEN 'Vigente' ELSE 'No vigente' END AS estado, idFacultad FROM ESCUELA limit {} offset {}".format(limit, offset))
        escuela = cursor.fetchall()
        print(escuela)
    conexion.close()
    return escuela

def actualizar_escuela(nombre,descripcion, estado, nombre1,id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE ESCUELA SET nombre= %s,descripcion= %s, estado= %s, idFacultad= %s WHERE idEscuela = %s",
                       (nombre,descripcion, estado, obtener_idfacultad(nombre1),id))
    conexion.commit()
    conexion.close()


def dar_baja(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE ESCUELA SET estado='N' WHERE idEscuela = %s",
                       (id))
    conexion.commit()
    conexion.close()
def dar_alta(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE ESCUELA SET estado='V' WHERE idEscuela = %s",
                       (id))
    conexion.commit()
    conexion.close()
def buscar_escuela(nombre):
    conexion = obtener_conexion()
    escuela = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT idEscuela,nombre,descripcion, estado, idFacultad FROM ESCUELA WHERE nombre LIKE ('%'||%s||'%')", (nombre,))
        escuela = cursor.fetchall()
    conexion.close()
    return escuela

def buscar_escuela_id(id):
    conexion = obtener_conexion()
    escuela = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT idEscuela,e.nombre,e.descripcion, e.estado, f.nombre FROM ESCUELA e INNER JOIN FACULTAD f on e.idFacultad=f.idFacultad  WHERE idEscuela = %s", (id,))
        escuela = cursor.fetchone()
    conexion.close()
    return escuela

def eliminar_escuela(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM ESCUELA WHERE idEscuela = %s", (id))
    conexion.commit()
    conexion.close()