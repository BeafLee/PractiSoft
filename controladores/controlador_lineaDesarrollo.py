from bd import obtener_conexion


def obtener_Lineas():
    conexion = obtener_conexion()
    lineas = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT idLinea,descripcion,case estado when'V' then'VIGENTE'  else 'NO VIGENTE' END AS ESTADO FROM LINEA_DESARROLLO ")
        lineas = cursor.fetchall()
    conexion.close()
    return lineas

def obtener_LineaID(id):
    conexion = obtener_conexion()
    lineas = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT idLinea,descripcion,case estado when'V' then'VIGENTE'  else 'NO VIGENTE' END AS ESTADO FROM LINEA_DESARROLLO WHERE idLinea=%s",(id))
        lineas = cursor.fetchall()
    conexion.close()
    return lineas

def obtener_ultimoid():
    conexion = obtener_conexion()
    id=None
    with conexion.cursor() as cursor:
        cursor.execute("SELECT COALESCE((MAX(idLinea)),0)+1 as id from LINEA_DESARROLLO")
        id = cursor.fetchone()
    conexion.close()
    return id

def insertar_linea(descripcion):
    conexion = obtener_conexion()

    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO LINEA_DESARROLLO(idLinea,descripcion,estado) VALUES (%s,%s,'V')",
                       (obtener_ultimoid(),descripcion))
    conexion.commit()
    conexion.close()

def eliminar_Linea(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM LINEA_DESARROLLO WHERE idLinea = %s ", (id))
    conexion.commit()
    conexion.close()

def actualizar_Linea(descripcion,id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE LINEA_DESARROLLO SET descripcion = %s WHERE idLinea=%s",
                       (descripcion,id))
    conexion.commit()
    conexion.close()

def DarBaja(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE LINEA_DESARROLLO SET estado = 'N' WHERE idLinea=%s",
                       (id))
    conexion.commit()
    conexion.close()

def DesacerDarBaja(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE LINEA_DESARROLLO SET estado = 'V' WHERE idLinea=%s",
                       (id))
    conexion.commit()
    conexion.close()

