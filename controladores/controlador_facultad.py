from bd import obtener_conexion

def insertar_facultad(nombre, descripcion, estado):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO FACULTAD(idFacultad,nombre, descripcion, estado) VALUES (%s, %s,%s, %s)",
                       (obtener_ultimoid(),nombre, descripcion, estado))
    conexion.commit()
    conexion.close()

def obtener_ultimoid():
    conexion = obtener_conexion()
    id=None
    with conexion.cursor() as cursor:
        cursor.execute("SELECT COALESCE((MAX(idFacultad)),0)+1 as idFacultad from FACULTAD")
        id = cursor.fetchone()
    conexion.close()
    return id

def obtener_facultad():
    conexion = obtener_conexion()
    facultad = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT idFacultad,nombre,descripcion ,CASE estado WHEN 'V' THEN 'Vigente' ELSE 'No vigente' END AS estado FROM FACULTAD")
        facultad = cursor.fetchall()
        print(facultad)
    conexion.close()
    return facultad

def obtener_facultad_index(limit,offset):
    conexion=obtener_conexion()
    facultad=[]
    with conexion.cursor() as cursor:
        cursor.execute("SELECT idFacultad,nombre, descripcion ,CASE estado WHEN 'V' THEN 'Vigente' ELSE 'No vigente' END AS estado FROM FACULTAD limit {} offset {}".format(limit, offset))
        facultad = cursor.fetchall()
        print(facultad)
    conexion.close()
    return facultad

def actualizar_facultad(nombre,descripcion, estado, id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE FACULTAD SET nombre= %s, descripcion = %s, estado=%s WHERE idFacultad = %s",
                       (nombre, descripcion, estado, id))
    conexion.commit()
    conexion.close()


def dar_baja(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE FACULTAD SET estado='N' WHERE idFacultad = %s",
                       (id))
    conexion.commit()
    conexion.close()
def dar_alta(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE FACULTAD SET estado='V' WHERE idFacultad = %s",
                       (id))
    conexion.commit()
    conexion.close()



def buscar_facultad(nombre):
    conexion = obtener_conexion()
    facultad = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT idFacultad,nombre, descripcion, estado FROM FACULTAD WHERE nombre LIKE ('%'||%s||'%')", (nombre,))
        facultad = cursor.fetchall()
    conexion.close()
    return facultad

def buscar_facultad_id(id):
    conexion = obtener_conexion()
    facultad = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT idFacultad,nombre, descripcion, estado FROM FACULTAD WHERE idFacultad = %s", (id,))
        facultad = cursor.fetchone()
    conexion.close()
    return facultad

def eliminar_facultad(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM FACULTAD WHERE idFacultad = %s", (id))
    conexion.commit()
    conexion.close()
    