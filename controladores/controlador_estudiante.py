from bd import obtener_conexion
import mysql.connector

import pandas as pd 

mydb= mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="",
    database="proyecto_bytesquad"
    )
mycursormydb = mydb.cursor()  


def obtener_estudiante():
    conexion = obtener_conexion()
    estudiante = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT idEstudiante,codigo,nombres,apellidos,cicloActual,semestreInicio,dni,correo1,correo2,telefono1,telefono2,direccion, CASE estado WHEN 'A' THEN 'Apto' ELSE 'No apto' END AS estado, idPlanEs,idDistrito,idUsuario FROM ESTUDIANTE")
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

def obtener_ultimoidEstudiante():
    conexion = obtener_conexion()
    id=None
    with conexion.cursor() as cursor:
        cursor.execute("SELECT COALESCE((MAX(idEstudiante)),0)+1 as idEstudiante from ESTUDIANTE")
        id = cursor.fetchone()
    conexion.close()
    return id

def obtener_ultimoidUsuario():
    conexion = obtener_conexion()
    id=None
    with conexion.cursor() as cursor:
        cursor.execute("SELECT COALESCE((MAX(idUsuario)),0)+1 as idUsuario from USUARIO")
        id = cursor.fetchone()
    conexion.close()
    return id

def obtener_distrito(nomDistrito):
    conexion = obtener_conexion()
    id=None
    with conexion.cursor() as cursor:
        cursor.execute("SELECT idDistrito from DISTRITO where nombre=%s",(nomDistrito))
        id = cursor.fetchone()
    conexion.close()
    return id

def obtener_pais(nomPais):
    conexion = obtener_conexion()
    id=None
    with conexion.cursor() as cursor:
        cursor.execute("SELECT idPais from PAIS where nombre=%s",(nomPais))
        id = cursor.fetchone()
    conexion.close()
    return id

def obtener_plan(nomPlan):
    conexion = obtener_conexion()
    id=None
    with conexion.cursor() as cursor:
        cursor.execute("SELECT idPlanEs from PLAN_ESTUDIO where nombre=%s",(nomPlan))
        id = cursor.fetchone()
    conexion.close()
    return id

def buscar_estudiante(idCodESt):
    conexion = obtener_conexion()
    estudiante = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT idEstudiante FROM ESTUDIANTE WHERE codigo = %s", (idCodESt,))
        estudiante = cursor.fetchone()
    conexion.close()
    return estudiante

def parseCSV(filePath):
      # CVS Column Names
      col_names = ['codigo_estudiante','nombres','apellidos', 'ciclo_Actual', 'semestre_Inicio', 'dni' , 'correo1', 'correo2', 'telefono1', 'telefono2', 'direccion', 'Plan_de_Estudio','Distrito','Pais']
      # Use Pandas to parse the CSV file
      excelData = pd.read_excel(filePath,names=col_names,index_col=None)
      excelData.dropna(inplace = True)
      # Loop through the Rows
      for i,row in excelData.iterrows():
             
             if (buscar_estudiante(str(row['codigo_estudiante'])) == None):
                    print(row['codigo_estudiante'])
                    print(buscar_estudiante(row['codigo_estudiante']))
                    idU=obtener_ultimoidUsuario()
                    sql1 = "INSERT INTO USUARIO (idUsuario, nomUsuario, contraseña, idTipoU) VALUES (%s, %s, %s, 1)"
                    value1 = (idU[0],row['codigo_estudiante'],str(row['dni']))
                    mycursormydb.execute(sql1, value1)
                    mydb.commit()
                                        
                    idE=obtener_ultimoidEstudiante()
                    plEst=obtener_plan(str(row['Plan_de_Estudio']))
                    dis=obtener_distrito(row['Distrito'])
                    pais=obtener_pais(row['Pais'])
                    print(pais)
                    print(dis)
                    sql2 = "INSERT INTO ESTUDIANTE (idEstudiante, codigo, nombres, apellidos, cicloActual, semestreInicio, dni, correo1, correo2, telefono1, telefono2, direccion, estado, idPlanEs, idUsuario, idDistrito, idPais) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'V', %s, %s, %s, %s)"
                    value2 = (idE[0],row['codigo_estudiante'],row['nombres'],row['apellidos'],row['ciclo_Actual'],row['semestre_Inicio'],str(row['dni']),row['correo1'],row['correo2'],str(row['telefono1']),str(row['telefono2']),row['direccion'],plEst[0],1,dis[0],pais[0])
                    mycursormydb.execute(sql2, value2)
                    mydb.commit()