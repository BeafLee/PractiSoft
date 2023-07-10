from bd import obtener_conexion

def obtener_cantidadPracticasLineaD():
    conexion = obtener_conexion()
    nombreCantidad = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT LD.descripcion, COUNT(P.idPractica) AS cantidad FROM LINEA_DESARROLLO LD LEFT JOIN PRACTICA P ON LD.idLinea = P.idLinea GROUP BY LD.descripcion;")
        nombreCantidad = cursor.fetchall()
    conexion.close()
    return nombreCantidad

def obtener_reporte1():
    conexion = obtener_conexion()
    reporte1 = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT estado, COUNT(DISTINCT idEstudiante) AS cantidad_estudiantes FROM PRACTICA GROUP BY estado;")
        reporte1 = cursor.fetchall()
    conexion.close()
    return reporte1

def obtener_reporte2():
    conexion = obtener_conexion()
    reporte2 = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT YEAR(fechaInicio) AS Anio, COUNT(*) AS TotalPracticas FROM PRACTICA GROUP BY YEAR(fechaInicio) ORDER BY Anio;")
        reporte2 = cursor.fetchall()
    conexion.close()
    return reporte2