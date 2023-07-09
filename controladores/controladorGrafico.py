from bd import obtener_conexion

def obtener_cantidadPracticasLineaD():
    conexion = obtener_conexion()
    nombreCantidad = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT LD.descripcion, COUNT(P.idPractica) AS cantidad FROM LINEA_DESARROLLO LD LEFT JOIN PRACTICA P ON LD.idLinea = P.idLinea GROUP BY LD.descripcion;")
        nombreCantidad = cursor.fetchall()
    conexion.close()
    return nombreCantidad


