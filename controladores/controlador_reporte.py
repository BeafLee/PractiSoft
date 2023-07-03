from bd import obtener_conexion

def obtener_reporte_1():
    conexion = obtener_conexion()
    reporte1 = []
    with conexion.cursor() as cursor:
        cursor.execute("select se.nombreSe,ld.descripcion, count(pr.idlinea) from PRACTICA pr inner join SEMESTRE as se on pr.idSemestreIn = se.idSemestre inner join LINEA_DESARROLLO as ld on ld.idLinea=pr.idLinea GROUP by ld.descripcion;")
        reporte1 = cursor.fetchall()
        print(reporte1)
    conexion.close()
    return reporte1

def obtener_reporte_2():
    conexion = obtener_conexion()
    reporte2 = []
    with conexion.cursor() as cursor:
        cursor.execute("select CONCAT(seI.nombreSe, ' - ' , seF.nombreSe) ,pr.estado,COUNT(pr.idPractica) from PRACTICA pr inner join SEMESTRE seI ON seI.idSemestre=pr.idSemestreIn inner join SEMESTRE seF ON seF.idSemestre=pr.idSemestreFi GROUP BY seI.nombreSe,seF.nombreSe,pr.estado;")
        reporte2 = cursor.fetchall()
        print(reporte2)
    conexion.close()
    return reporte2



