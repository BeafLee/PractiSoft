from bd import obtener_conexion

def insertar_informe_inicial_empresa(estado,urlAceptacionCompromiso,fechaEntrega,labores,urlFirmaResponsable,urlSelloEmpresa,idPractica):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO INFORME_INICIAL_EMPRESA (idInformeInicialEmpresa,estado,urlAceptacionCompromiso,fechaEntrega,labores,urlFirmaResponsable,urlSelloEmpresa,idPractica) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
                       (obtener_ultimoidIIE(),estado,urlAceptacionCompromiso,fechaEntrega,labores,urlFirmaResponsable,urlSelloEmpresa,idPractica))
    conexion.commit()
    conexion.close()

def obtener_ultimoidIIE():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT COALESCE((MAX(idInformeInicialEmpresa)),0)+1 as idInformeInicialEmpresa from INFORME_INICIAL_EMPRESA")
        idIIE = cursor.fetchone()
    conexion.close()
    return idIIE

def obtener_informe_inicial_empresa():
    conexion = obtener_conexion()
    informe_inicial_empresa = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT idInformeInicialEmpresa,estado,urlAceptacionCompromiso,fechaEntrega,labores,urlFirmaResponsable,urlSelloEmpresa,idPractica FROM INFORME_INICIAL_EMPRESA")
        informe_inicial_empresa = cursor.fetchall()
    conexion.close()
    return informe_inicial_empresa

def actualizar_informe_inicial_empresa(estado,urlAceptacionCompromiso,fechaEntrega,labores,urlFirmaResponsable,urlSelloEmpresa,idInformeInicialEmpresa):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE INFORME_INICIAL_EMPRESA SET estado = %s,urlAceptacionCompromiso = %s,fechaEntrega = %s,labores = %s,urlFirmaResponsable = %s,urlSelloEmpresa = %s WHERE idInformeInicialEmpresa = %s",
                       (estado,urlAceptacionCompromiso,fechaEntrega,labores,urlFirmaResponsable,urlSelloEmpresa,idInformeInicialEmpresa))
    conexion.commit()
    conexion.close()

def buscar_informe_inicial_empresa_id(idInformeInicialEmpresa):
    conexion = obtener_conexion()
    informe_inicial_empresa = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT idInformeInicialEmpresa,urlAceptacionCompromiso,fechaEntrega,labores,urlFirmaResponsable,urlSelloEmpresa,idPractica,observacion FROM INFORME_INICIAL_EMPRESA WHERE idInformeInicialEmpresa = %s;", (idInformeInicialEmpresa))
        informe_inicial_empresa = cursor.fetchone()
    conexion.close()
    return informe_inicial_empresa

def obtener_informe_iniciales(id):
    conexion = obtener_conexion()
    informe = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT fechaEntrega,estado from INFORME_INICIAL_EMPRESA where idPractica=%s",(id))
        informe = cursor.fetchone()
    conexion.close()
    return informe
def obtener_informe_finales(id):
    conexion = obtener_conexion()
    informe = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT fechaEntrega,estado from INFORME_FINAL_EMPRESA where idPractica=%s",(id))
        informe = cursor.fetchone()
    conexion.close()
    return informe
def eliminar_informe_inicial_empresa(idInformeInicialEmpresa):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM INFORME_INICIAL_EMPRESA WHERE idInformeInicialEmpresa = %s", (idInformeInicialEmpresa))
    conexion.commit()
    conexion.close()
def infoPlantilla(idPractica):
    conexion = obtener_conexion()
    info = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT EM.razonSocial, CONCAT(JI.nombre, ', ', JI.apellidos), JI.cargo, CONCAT(ES.nombres, ', ', ES.apellidos), PR.fechaInicio, PR.fechaFin, PR.idPractica FROM PRACTICA PR INNER JOIN ESTUDIANTE ES ON ES.idEstudiante = PR.idEstudiante INNER JOIN JEFE_INMEDIATO JI ON JI.idJefe = PR.idJefe INNER JOIN EMPRESA EM ON EM.idEmpresa = JI.idEmpresa WHERE PR.idPractica = %s",(idPractica))
        info = cursor.fetchone()
    conexion.close()
    return info
def concat_labores(labores):
    cont = 1
    concat = ''
    for labor in labores:
        if cont < len(labores):
          concat += labor + ' | '
        else: concat += labor
        cont += 1
    return concat

def desconcat_labores(labores):
  labor = ['']
  cont = 0
  cond2 = ''
  for letra in labores:
    if(letra == ' '):
      if(cond2 == '|'):
        continue
      cond2 = ' '
    elif(letra != '|'): 
      if(cond2 == ' '):
        labor[cont] += ' '
      labor[cont] += letra
      cond2 = ''
      continue
    if((cond2 == ' ') & (letra == '|')) | (letra == '|') :
      cont+=1
      labor.append('')
      cond2 = '|'
  return labor

def observar_informe(observacion,idInforme):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE INFORME_INICIAL_EMPRESA SET estado='O', observacion = %s WHERE idInformeInicialEmpresa = %s",
                       (observacion,idInforme))
    conexion.commit()
    conexion.close()

def aceptar_informe(idInforme):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE INFORME_INICAL_EMPRESA SET estado='A', observacion = '' WHERE idInformeInicialEmpresa = %s",
                       (idInforme))
    conexion.commit()
    conexion.close()