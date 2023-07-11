import os
import jinja2
import pdfkit
import pandas as pd  #instalar
import mysql.connector #instalar
from os.path import join, dirname, realpath
from PyPDF2 import PdfMerger , PdfReader 
from flask import Flask, flash, request, jsonify, render_template, redirect, session, url_for, send_file, send_from_directory, make_response
import datetime
from werkzeug.utils import secure_filename
import controladores.controlador_inicioSesion as cont_ini
import controladores.controlador_informe_estudiante as cont_infes
import controladores.controlador_semestre as cont_sem
import controladores.controlador_facultad as cont_fac
import controladores.controlador_escuela as cont_esc
import controladores.controlador_empresa as cont_emp
import controladores.controlador_detalle_practica as cont_dp
import controladores.controlador_nueva_practica as cont_nprac
import controladores.controlador_practica as cont_prac
import controladores.controlador_reporte as cont_rep
import controladores.controlador_seguimiento_practica as cont_seg
import controladores.controlador_informe_final_estudiante as cont_inf_final_est
import controladores.controlador_informe_final_empresa as cont_inf_final_emp
import controladores.controlador_informe_inicial_empresa as cont_iie
import controladores.controlador_estudiante as cont_est
import controladores.controlador_usuario as cont_usu
import controladores.controlador_ubicacion as cont_ubi
import controladores.controladorGrafico as controladorGrafico
import controladores.controlador_jefe_inmediato as controlador_jefe_inmediato
import controladores.localidad as cont_localidad
import controladores.controlador_informe_estudiante as cont_infes
import controladores.controlador_desempenio as cont_des
import controladores.controlador_lineaDesarrollo as controlador_lineaDesarrollo

app = Flask(__name__)
app.config["DEBUG"] = True
app.config['SECRET_KEY'] = 'ByteSquad S.A.C. - PRACTISOFT'
#app.config.from_object('core.config.SECRET_KEY')

#################################################################################
##                      CONFIGURACION PARA GENERAR PDF                         ##
#################################################################################
config = pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')

#################################################################################
##                              IMPORTE EXCEL                                  ##
#################################################################################
# Upload folder
UPLOAD_FOLDER = 'PractiSoft/static/files'
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER

# Get the uploaded files
@app.route("/estudiantes", methods=['POST'])
def uploadFiles():
    # get the uploaded file
    estudiantes = cont_est.obtener_estudiante()
    usu = session['usuario']
    error_statement=None
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
          # set the file path
        uploaded_file.save(file_path)
        error=cont_est.parseCSV(file_path)
        if error ==-1:
            error_statement="Formato de Excel Incorrecto"
        elif error ==-2:
            error_statement="Datos no válidos"
        elif error==1:
            cont_est.importData(file_path)
            return redirect("/estudiantes")
        return render_template("/estudiante/listarEstudiante.html", error_statement=error_statement, usuario = usu, maestra=session['maestra'], estudiantes = estudiantes)
    return render_template("/estudiante/listarEstudiante.html", usuario = usu, maestra=session['maestra'], estudiantes = estudiantes,error_statement=error_statement)

#################################################################################
##                                  INICIO                                     ##
#################################################################################

@app.route('/')
@app.route('/<mostrar>')
def iniciarSesion(mostrar='no mostrar'):
    return render_template("/login.html", mostrarModal = mostrar)

@app.route('/graficoCajan')
def graficoCajan():   
    lineasPracticas=controladorGrafico.obtener_cantidadPracticasLineaD()
    datos = {}
    for nombre, cantidad in lineasPracticas:
        datos[nombre] = cantidad
    return render_template("/reportes/grafico.html",datos=datos,lineasPracticas=lineasPracticas,maestra=session['maestra'],usuario=session['usuario'])

@app.route('/reporte1')
def reporte1():   
    practicasC=controladorGrafico.obtener_reporte1()
    datos = {}
    for nombre, cantidad in practicasC:
        datos[nombre] = cantidad
    return render_template("/reportes/reporte1.html",datos=datos,practicasC=practicasC,maestra=session['maestra'],usuario=session['usuario'])

@app.route('/reporte2')
def reporte2():   
    practicasA=controladorGrafico.obtener_reporte2()
    datos = {}
    for nombre, cantidad in practicasA:
        datos[nombre] = cantidad
    return render_template("/reportes/reporte2.html",datos=datos,practicasA=practicasA,maestra=session['maestra'],usuario=session['usuario'])


@app.route('/login', methods=["POST"])
def login():
    usuario = request.form["usuario"]
    contra = request.form["contra"]

    usuario_log = cont_ini.verificarUsuario(usu=usuario, contra=contra)

    if usuario_log is None:
        return redirect(url_for("iniciarSesion", mostrar='mostrar') )
    elif usuario_log[3] == 1:
        usu = list(usuario_log)
        usu[4] = 'Estudiante'
        session['usuario'] = usu
        session['maestra'] = "maestra_e.html"
        return redirect("/index_e")
    elif usuario_log[3] == 2:
        usu = list(usuario_log)
        usu[4] = 'Administrador del sistema'
        session['usuario'] = usu
        session['maestra'] = "maestra_a.html"
        return redirect("/index_a")
    elif usuario_log[3] == 3:
        usu = list(usuario_log)
        usu[4] = 'Docente de apoyo'
        session['usuario'] = usu
        session['maestra'] = "maestra_d.html"
        return redirect("/index_d")
    elif usuario_log[3] == 4:
        usu = list(usuario_log)
        usu[4] = 'Responsable de la practica'
        session['usuario'] = usu
        session['maestra'] = "maestra_j.html"
        return redirect("/index_j")



@app.route('/logout')
def logout():
    session.pop('usuario')
    return redirect("/")

#################################################################################
##                                  PERFIL                                     ##
#################################################################################

@app.route('/perfil')
def perfil():
    usu = session['usuario']
    return render_template("perfil.html", usuario = usu, maestra=session['maestra'])

@app.route('/perfileditar')
def perfileditar():
    usu = session['usuario']
    return render_template("editarperfil.html", usuario = usu, maestra=session['maestra'])

@app.route("/actualizar_perfil", methods=["POST"])
def actualizar_perfil():
    usu = session['usuario']
    idUsuario = request.form["idUsuario"]
    nomUsuario = request.form["nomUsuario"]
    contraseña = request.form["contraseña"]
    idTipoU = request.form["idTipoU"]
    cont_usu.actualizar_usuario(nomUsuario, contraseña, idTipoU, idUsuario)
    return redirect("/")

#################################################################################
##                                  INDEX                                      ##
#################################################################################
@app.route("/index_supremo")
def index_s():
    usu = session['usuario']
    if usu[3] is None:
        return "uwu"
    elif usu[3] == 1:
        return redirect("/index_e")
    elif usu[3] == 2:
        return redirect("/index_a")
    elif usu[3] == 4:
        return redirect("/index_j")
    elif usu[3] == 3:
        return redirect("/index_d")


@app.route("/index_d_modulo1")
def index_d_modulo1():
    usu = session['usuario']
    return render_template("/maestra_d_modulo1.html",usuario = usu)

@app.route("/index_d_modulo2")
def index_d_modulo2():
    usu = session['usuario']
    return render_template("/maestra_d_modulo2.html",usuario = usu)
    
@app.route("/index_a")
def index_a():
    usu = session['usuario']
    ma = session['maestra']
    return render_template("/index/index_a.html", usuario = usu,maestra=ma)

@app.route("/index_e")
def index_e():
    usu = session['usuario']
    ma = session['maestra']
    print(ma)
    return render_template("/index/index_e.html", usuario = usu,maestra=ma)

@app.route("/index_d")
def index_d():
    usu = session['usuario']
    return render_template("/index/index_d.html", usuario = usu, maestra=session['maestra'])

@app.route("/index_j")
def index_j():
    usu = session['usuario']
    return render_template("/index/index_j.html", usuario = usu, maestra=session['maestra'])

#################################################################################
##                                  IMÁGENES                                   ##
#################################################################################
@app.route('/images/<path:filepath>')
def get_image(filepath):
    folder_path, filename = os.path.split(filepath)
    return send_from_directory(folder_path, filename)

#################################################################################
##                                  Linea Desarrollo                                   ##
#################################################################################
###     GESTIONAR LINEA
@app.route("/lineaDesarrollo")
def lineaDesarrollo():
    lineas = controlador_lineaDesarrollo.obtener_Lineas()
    return render_template("/lineaDesarrollo/lineaD.html", lineas=lineas, usuario = session['usuario'], maestra=session['maestra'])

@app.route("/NuevalineaDesarrollo")
def NuevalineaDesarrollo():
    return render_template("/lineaDesarrollo/nuevaLinea.html", usuario = session['usuario'], maestra=session['maestra'])

@app.route("/guardar_LINEA", methods=["POST"])
def guardar_LINEA():  
    linea = request.form["linea"]
    controlador_lineaDesarrollo.insertar_linea(linea)
    return redirect("/lineaDesarrollo")

@app.route("/Modificar_LINEA/<int:id>")
def Modificar_LINEA(id):  
    linea=controlador_lineaDesarrollo.obtener_LineaID(id)
    return render_template("/lineaDesarrollo/editarLinea.html",linea=linea, usuario = session['usuario'], maestra=session['maestra'])

@app.route("/Actualizar_LINEA", methods=["POST"])
def Actualizar_LINEA():  
    linea = request.form["linea"]
    id=request.form["id"]
    controlador_lineaDesarrollo.actualizar_Linea(linea,id)
    return redirect("/lineaDesarrollo")

@app.route("/Eliminar_LINEA", methods=["POST"])
def Eliminar_LINEA():  
    id=request.form["id"]
    controlador_lineaDesarrollo.eliminar_Linea(id)
    return redirect("/lineaDesarrollo")

@app.route("/DARBAJA_LINEA", methods=["POST"])
def DARBAJA_LINEA():  
    id=request.form["id"]
    controlador_lineaDesarrollo.DarBaja(id)
    return redirect("/lineaDesarrollo")
#################################################################################
##                                  PRACTICA                                   ##
#################################################################################
###     GESTIONAR PRACTICA
@app.route("/practicas")
def practicas():
    practica = cont_prac.obtener_practica()
    return render_template("/practica/listarPractica.html", practica=practica, usuario = session['usuario'], maestra=session['maestra'])

@app.route("/actualizar_practica/<int:id>", methods=["POST"])
def actualizar_practica(id):
   # modalidad=request.form[""]
    fechaI=request.form["feI"]
    fechaF=request.form["feF"]
    horas=request.form["hPrac"]
    fechaL=request.form["feLim"]
    cont_nprac.actualizar_practica(fechaI,fechaF,horas,fechaL,id)
    return redirect("/practicas")

@app.route("/practicasE")
def practicasE():
    usu=session['usuario']
    idU=usu[0]
    estudiante=cont_prac.obtener_EstudianteUs(idU)
    idE=estudiante[0]
    practica = cont_prac.obtener_practicaE(idE)
    return render_template("/practica/listarPractica.html", practica=practica, usuario = session['usuario'], maestra=session['maestra'])

@app.route("/EnviarPractica",methods=["POST"])
def EnviarPractica():
    id=request.form["id"]
    cont_prac.EnviarPractica(id)
    return redirect("practicasE")
###     AGREGAR PRACTICA

@app.route("/agregar_practica")
def agregar_practica():
    usu = session['usuario']
    estudiante = cont_nprac.obtener_estudiante(usu[0])
    empresa = cont_nprac.obtener_empresa()
    semestreA = cont_nprac.obtenerSemestres()
    semestreF = cont_nprac.obtenerSemestres()
    linea = cont_nprac.obtener_linea_desarrollo()
    return render_template("/practica/nuevaPractica.html", usuario = session['usuario'], maestra=session['maestra'], estudiante = estudiante, empresa=empresa,semestreA=semestreA,semestreF=semestreF,linea=linea)

@app.route("/buscar_empresa_datos", methods=["GET"])
def buscar_empresa_datos():
    nombre_empresa = request.args.get('empresa')
    datos = cont_nprac.buscar_empresa_datos(nombre_empresa)
    return jsonify(datos)

@app.route("/guardar_practica", methods=["POST"])
def guardar_practica():
    
    usu = session['usuario']
    feI = request.form["feI"]
    feF = request.form["feF"]
    hPrac = request.form["hPrac"]
    feLim = request.form["feLim"]
    mod = request.form["mod"]
    estudiante = cont_nprac.obtener_estudiante(usu[0])
    jefe=request.form["jefe"]
    ruc=request.form["ruc"]
    linDes=request.form["linDes"]
    semI=request.form["semI"]
    semF=request.form["semF"]
    if request.form['action'] == 'Guardar':
        cont_nprac.insertar_practica(feI,feF,hPrac,feLim,mod,estudiante[0],cont_nprac.buscar_id_jefe(jefe,ruc),cont_nprac.obtener_id_personal(),cont_nprac.obtener_id_linea(linDes),cont_nprac.obtener_id_semestre(semI),cont_nprac.obtener_id_semestre(semF))

    elif request.form['action'] == 'Enviar':
        cont_nprac.enviar_practica(feI,feF,hPrac,feLim,mod,estudiante[0],cont_nprac.buscar_id_jefe(jefe,ruc),cont_nprac.obtener_id_personal(),cont_nprac.obtener_id_linea(linDes),cont_nprac.obtener_id_semestre(semI),cont_nprac.obtener_id_semestre(semF))


    return redirect("/practicasE")

###     MOSTRAR DETALLE DE PRACTICA
@app.route("/detalle_practica/<int:id>")
def detalle_practica(id):
    estadoP = cont_prac.obtener_estado(id)
    detalle = cont_dp.listar_detalle_practica(id)
    informe = cont_infes.obtener_informe_iniciales(id)
    informe1=cont_infes.obtener_informe_finales(id)
    informe2=cont_infes.obtener_informe_inicial_em(id)
    informe3=cont_infes.obtener_informe_final_em(id)
    informe4=cont_infes.obtener_informe_desemp(id)
    usu = session['usuario']
    tipou=cont_dp.obtener_tipoUsuario(usu[3])
    return render_template("/practica/detalle_practica.html", estadoP=estadoP, usuario = usu, detalle = detalle,informe=informe,informe1=informe1,informe2=informe2,informe3=informe3,informe4=informe4,mostrar_boton=True,mostrar_boton1=True,tipou=tipou, id=id)

@app.route("/editar_Practica/<int:id>")
def editar_Practica(id):
    practica = cont_prac.obtener_practicaID(id)
    empresa=cont_emp.obtener_empresa()
    semestreF = cont_nprac.obtenerSemestres()
    linea = cont_nprac.obtener_linea_desarrollo()
    return render_template("/practica/editarPractica.html", usuario = session['usuario'], maestra=session['maestra'], practica=practica,empresa=empresa,semestreF=semestreF,linea=linea,id=id)

#################################################################################
##                             SEGUIMIENTO PRACTICA                            ##
#################################################################################

### SEGUIMIENTO PRACTICA
@app.route("/seguimiento_practica/<int:id>")
def seguimiento_practica(id):
    usu = session['usuario']
    idPractica = cont_seg.obtener_idpractica(id)
    seguimiento_practicas = cont_seg.obtener_seguimiento_practica(id)
    return render_template("/practica/listarSeguimiento_practica.html", usuario = usu, maestra=session['maestra'], seguimiento_practicas=seguimiento_practicas, idPractica=idPractica)

###BUSCAR SEGUIMIENTO PRACTICA 
@app.route("/seguimiento_practica", methods=["POST"])
def seguimiento_id():
    idSeguimiento = request.form["idSeguimiento"]
    seguimiento = cont_seg.obtener_seguimiento_practica(idSeguimiento)
    return render_template("/practica/listarSeguimiento_practica.html", usuario = session['usuario'], maestra=session['maestra'], seguimiento = seguimiento, editSeguimiento = None)

@app.route("/agregar_seguimiento_practica/<int:idSeguimiento>")
def agregar_seguimiento_practica(idSeguimiento):
    usu = session['usuario']
    seguimiento_practica = cont_seg.obtener_datos(idSeguimiento)
    return render_template("/practica/nuevoSeguimiento_practica.html", usuario = usu, maestra=session['maestra'], seguimiento_practica=seguimiento_practica)

@app.route("/ver_seguimiento_practica/<int:idSeguimiento>")
def ver_seguimiento_practica(idSeguimiento):
    usu = session['usuario']
    seguimiento_practica = cont_seg.obtener_seguimiento_practica_total(idSeguimiento)
    return render_template("/practica/verSeguimiento_practica.html",usuario = usu, maestra=session['maestra'], seguimiento_practica=seguimiento_practica)

@app.route("/guardar_seguimiento_practica", methods=["POST"])
def guardar_seguimiento_practica():
    usu = session['usuario']
    fechaCreacion = request.form["fechaCreacion"]
    horaCreacion = request.form["horaCreacion"]
    tipo = request.form["tipo"]
    observacion = request.form["observacion"]
    idPractica = request.form["idPractica"]
    cont_seg.insertar_seguimiento_practica(fechaCreacion, horaCreacion, tipo, observacion, idPractica)
    return redirect("/seguimiento_practica/"+idPractica)

#################################################################################
##                              INFORME DESEMPEÑO                              ##
#################################################################################
@app.route('/generar_ide/<int:id>/<int:id1>', methods=['GET'])
def generar_ide(id,id1):
    # Realizar la consulta y obtener los datos
    # Supongamos que los datos se almacenan en una lista llamada 'datos'
    datos = cont_des.listar_desempenio(id1)
    resultados = cont_des.obtener_resultado(id)
    todos = cont_des.listar_todo_desempenio(id1)
    firmas = ['http://127.0.0.1:8000/'+todos[11]]
    # Renderizar el template HTML con los datos
    rendered_template = render_template('/informes/desempenio/htmlpuro.html', datos=datos, resultados = resultados, todos = todos,firmas=firmas)

    # Generar el PDF a partir del HTML renderizado
    pdf = pdfkit.from_string(rendered_template, False,configuration=config, options={"enable-local-file-access": ""})

    # Crear la respuesta con el PDF generado
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=INFORME_DESEMPEÑO.pdf'
    return response


@app.route("/agregarInformeDesempenio/<int:id>")
def agregarInformeDesempenio(id):
    datos = cont_des.listar_desempenio(id)
    return render_template("/informes/desempenio/crudEvaluacionDesempenio.html", usuario = session['usuario'], datos = datos)
@app.route("/eid/<int:id>/<int:id1>")
@app.route("/editarInformeDesempeño/<int:id>/<int:id1>")
def editarInformeDesempeño(id,id1):
    datos = cont_des.listar_desempenio(id1)
    resultados = cont_des.obtener_resultado(id)
    todos = cont_des.listar_todo_desempenio(id1)
    return render_template("/informes/desempenio/editarEvaluacionDesempenio.html", usuario = session['usuario'],datos=datos, resultados = resultados, todos = todos,informe=id1)
@app.route("/vid/<int:id>/<int:id1>")
@app.route("/verInformeDesempenio/<int:id>/<int:id1>")
def verInformeDesempenio(id1,id):
    datos = cont_des.listar_desempenio(id)
    resultados = cont_des.obtener_resultado(id1)
    todos = cont_des.listar_todo_desempenio(id)
    return render_template("/informes/desempenio/verEvaluacionDesempenio.html", usuario = session['usuario'],datos=datos,resultados=resultados,todos=todos)
@app.route("/actualizar_desempenio", methods=["POST"])
def actualizar_desempenio():
    no1=request.form['idInforme']
    est = request.form.get('submit_button')
    re = request.form.get('opcion1')
    pro = request.form.get('opcion2')
    com = request.form.get('opcion3')
    tra = request.form.get('opcion4')
    comp = request.form.get('opcion5')
    org  = request.form.get('opcion6')
    pun  = request.form.get('opcion7')
    con  = request.form['descAreaTrabajo']
    idp= request.form['idPractica']
    n1 = request.form.getlist('resultado1')
    n2 = request.form.getlist('opcionn')
    
    urlBase = "static/practica/"+str(idp)+"/informe/desempenio"
    if not os.path.exists(urlBase):
        os.makedirs(urlBase)

    firmaImg = request.files["firmaImg"]
    datos = cont_des.listar_todo_desempenio(idp)
    print(datos[11])
    if os.path.splitext(firmaImg.filename)[1] != '':
        urlFirma = urlBase + "/firma" + os.path.splitext(firmaImg.filename)[1]
        firmaImg.save(urlFirma)
    else: urlFirma = datos[10]
    

    cont_des.modificar_desempenio(est, re, pro, com, tra, comp, org, pun, con, urlFirma, idp)
    cont_des.eliminar_resultados(no1)

    for i in range(len(n1)):
        cont_des.insertar_resultado(n1[i], n2[i],no1)
    return redirect("/detalle_practica/"+idp)

@app.route("/guardar_desempenio", methods=["POST"])
def guardar_desempenio():

    est = request.form.get('submit_button')
    re = request.form.get('opcion1')
    pro = request.form.get('opcion2')
    com = request.form.get('opcion3')
    tra = request.form.get('opcion4')
    comp = request.form.get('opcion5')
    org  = request.form.get('opcion6')
    pun  = request.form.get('opcion7')
    con  = request.form['descAreaTrabajo']
    idp= request.form['idPractica']
    
    urlBase = "static/practica/"+str(idp)+"/informe/desempenio"
    if not os.path.exists(urlBase):
        os.makedirs(urlBase)

    firmaImg = request.files["firmaImg"]
    urlFirma = urlBase + "/firma" + os.path.splitext(firmaImg.filename)[1]
    firmaImg.save(urlFirma)

    nfilas = int(request.form['nfilas'])

    cont_des.insertar_desempenio(est, re, pro, com, tra, comp, org, pun, con, urlFirma, idp)
    idd = cont_des.obtener_ultimo_desempenio()
    for i in range(nfilas):
        nombre = 'tablita'+str(i+1)
        escala = 'opcionn'+str(i+1)
        no=request.form[nombre]
        es = request.form.get(escala)
        cont_des.insertar_resultado(no, es,idd)
    return redirect("/detalle_practica/"+idp)

#################################################################################
##                        INFORME INICIAL ESTUDIANTE                           ##
#################################################################################
@app.route('/generar_ies/<int:id>/<int:id1>', methods=['GET'])
def generar_ies(id,id1):
    # Realizar la consulta y obtener los datos
    # Supongamos que los datos se almacenan en una lista llamada 'datos'
    datos = cont_infes.listarInforme(id1)
    objetivos= cont_infes.obtener_objetivos(id)
    planes=cont_infes.obtener_plan(id)
    totales=cont_infes.obtener_totalh(id)
    imagenes=cont_infes.obtener_firmas(id)
    firmas = ['http://127.0.0.1:8000/'+imagenes[0],'http://127.0.0.1:8000/'+imagenes[1]]
    # Renderizar el template HTML con los datos
    rendered_template = render_template('/informes/inicial_estudiante/informe_inicial_estudiante.html', datos=datos,objetivos=objetivos,planes=planes,totales=totales,firmas=firmas)
    # Generar el PDF a partir del HTML renderizado
    options={'page-size':'Letter',
             'margin-top': '0.05in',
             'margin-right': '0.05in',
             'margin-bottom': '0.10in',
             'margin-left': '0.05in',
             'encoding': 'UTF-8'}
    pdf = pdfkit.from_string(rendered_template,options=options,configuration=config)

    # Crear la respuesta con el PDF generado
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=INFORME_INICIAL_ESTUDIANTE.pdf'
    return response
@app.route("/ai/<int:id>")
@app.route("/agregarInformeInicialEstudiante/<int:id>")
def agregarInformeInicialEstudiante(id):
    datos=cont_infes.listarInforme(id)
    return render_template("/informes/inicial_estudiante/agregarInformeInicial-Estudiante.html", usuario = session['usuario'],datos=datos)

@app.route("/ei/<int:id>/<int:id1>")
@app.route("/editarInformeInicialEstudiante/<int:id>/<int:id1>")
def editarInformeInicialEstudiante(id,id1):
    datos=cont_infes.listarInforme(id)
    objetivos= cont_infes.obtener_objetivos(id1)
    planes=cont_infes.obtener_plane(id1)
    return render_template("/informes/inicial_estudiante/editarInformeInicial-Estudiante.html", usuario = session['usuario'],datos=datos,objetivos=objetivos,planes=planes,informe=id1)

@app.route("/vie/<int:id>/<int:id1>")
@app.route("/verInformeInicialEstudiante/<int:id>/<int:id1>")
def verInformeInicialEstudiante(id,id1):
    datos=cont_infes.listarInforme(id)
    objetivos= cont_infes.obtener_objetivos(id1)
    planes=cont_infes.obtener_plane(id1)
    return render_template("/informes/inicial_estudiante/verInformeInicial-Estudiante.html", usuario = session['usuario'],datos=datos,objetivos=objetivos,planes=planes,informe=id1)

@app.route("/actualizar_iies", methods=["POST"])
def actualizar_iies():
    no=request.form['idInforme']
    idp  = request.form['idPractica']
    est = request.form.get('submit_button')
    objetivos = request.form.getlist("objetivo")
    n1 = request.form.getlist("nsemana")
    n2 = request.form.getlist("fechai")
    n3 = request.form.getlist("fechaf")
    n4 = request.form.getlist("actividad")
    n5 = request.form.getlist("nhoras")
    urlBase = "static/practica/"+str(idp)+"/informe/inicial_estudiante"
    if not os.path.exists(urlBase):
        os.makedirs(urlBase)
    firmaImg = request.files["firmaImg"]
    urlFirmaE = urlBase + "/firma" + os.path.splitext(firmaImg.filename)[1]
    firmaImg.save(urlFirmaE)
    firmaImg1 = request.files["firmaImg1"]
    urlFirmaJ = urlBase + "/firma" + os.path.splitext(firmaImg1.filename)[1]
    firmaImg1.save(urlFirmaJ)
    cont_infes.eliminar_plan(no)
    cont_infes.eliminar_objetivos(no)
    for i in range(len(objetivos)):
       cont_infes.insertar_objetivos(objetivos[i],no)
    for i in range(len(n1)):
       cont_infes.insertar_plan(n1[i],n2[i],n3[i],n4[i],n5[i],no)           
    cont_infes.modificar_informe_inicial_estudiante(est,urlFirmaE,urlFirmaJ,idp)
    return redirect("/detalle_practica/"+idp)

@app.route("/guardar_iies", methods=["POST"])
def guardar_iies():
    est = request.form.get('submit_button')
    idp  = request.form['idPractica']
    urlBase = "static/practica/"+str(idp)+"/informe/inicial_estudiante"
    if not os.path.exists(urlBase):
        os.makedirs(urlBase)
    firmaImg = request.files["firmaImg"]
    urlFirmaE = urlBase + "/firma" + os.path.splitext(firmaImg.filename)[1]
    firmaImg.save(urlFirmaE)
    firmaImg1 = request.files["firmaImg1"]
    urlFirmaJ = urlBase + "/firma" + os.path.splitext(firmaImg1.filename)[1]
    firmaImg1.save(urlFirmaJ)
    
    nfilas = int(request.form['nfilas'])
    nfilas1 = int(request.form['nfilas1'])
    cont_infes.insertar_informe_inicial_estudiante(est, urlFirmaE,urlFirmaJ,idp)
    idd = cont_infes.obtener_ultimo_ie()
    for i in range(nfilas):
        nombre = 'objetivo'+str(i+1)
        no=request.form[nombre]
        cont_infes.insertar_objetivos(no,idd)
        
    for i in range(nfilas1):
        nsemana = 'nsemana'+str(i+1)
        fechai = 'fechai'+str(i+1)
        fechaf = 'fechaf'+str(i+1)
        actividad = 'actividad'+str(i+1)
        nhoras = 'nhoras'+str(i+1)
        n1=request.form[nsemana]
        n2=request.form[fechai]
        n3=request.form[fechaf]
        n4=request.form[actividad]
        n5=request.form[nhoras]
        cont_infes.insertar_plan(n1,n2,n3,n4,n5,idd)   
    return redirect("/detalle_practica/"+idp)



#################################################################################
##                          INFORME FINAL - ESTUDIANTE                         ##
#################################################################################
separadorText = '/%/'

###     MOSTRAR FORMULARIO DE INFORME FINAL
@app.route("/agregarInformeFinalEstudiante/<int:idPractica>")
def agregarInformeFinalEstudiante(idPractica):
    extraData = cont_inf_final_est.buscarOtraData_idPractica(idPractica)
    data = ["Crear", 1, extraData[0], extraData[1]]
    estado = "-"
    return render_template("/informes/final_estudiante/crudInformeFinal-Estudiante.html", usuario = session['usuario'], maestra=session['maestra'], data = data, estado = estado)

@app.route("/editarInformeFinalEstudiante/<int:idPractica>")
def editarInformeFinalEstudiante(idPractica):
    infoData = cont_inf_final_est.buscar_id(idPractica)
    
    #Separar las conclusiones y recomendaciones en listas
    conclusiones = infoData[12].split(separadorText)
    recomendaciones = infoData[13].split(separadorText)
    estado = infoData #se usa para saber el estado y el texto de observacion
    data = ["Editar", infoData[22], infoData[1], infoData[2], [infoData[15], infoData[16], infoData[17], infoData[18], infoData[19], infoData[7], infoData[8], infoData[9], infoData[10], infoData[11], conclusiones, recomendaciones, infoData[14], infoData[20], infoData[4]], infoData[3]]
    #data = ["Editar", idParactica, "RAZON 1", "DIREC 1", ["giro 1", "repre 1", cantTrabajadoer, "vision", "mision", "infra fisica", "infra tecno", "organigrama.png", "desc area de trabajo", "desc labores", ["conclu 1", "conclu 2", "conclu 3"], ["reco 1", "reco 2", "recomen 34"], "biblio", "anexos.pdf", "introduccion text"]]

    return render_template("/informes/final_estudiante/crudInformeFinal-Estudiante.html", usuario = session['usuario'], maestra=session['maestra'], data = data, estado = estado)

@app.route("/InformeFinalEstudiante/<int:idPractica>")
def verInformeFinalEstudiante(idPractica):
    infoData = cont_inf_final_est.buscar_id(idPractica)
    
    #Separar las conclusiones y recomendaciones en listas
    conclusiones = infoData[12].split(separadorText)
    recomendaciones = infoData[13].split(separadorText)
    estado = infoData #se usa para saber el estado y el texto de observacion
    data = ["Ver", infoData[22], infoData[1], infoData[2], [infoData[15], infoData[16], infoData[17], infoData[18], infoData[19], infoData[7], infoData[8], infoData[9], infoData[10], infoData[11], conclusiones, recomendaciones, infoData[14], infoData[20], infoData[4]], infoData[3]]
    #data = ["Ver", idParactica, "RAZON 1", "DIREC 1", ["giro 1", "repre 1", cantTrabajadoer, "vision", "mision", "infra fisica", "infra tecno", "organigrama.png", "desc area de trabajo", "desc labores", ["conclu 1", "conclu 2", "conclu 3"], ["reco 1", "reco 2", "recomen 34"], "biblio", "anexos.pdf", "introduccion text"]]
    return render_template("/informes/final_estudiante/crudInformeFinal-Estudiante.html", usuario = session['usuario'], maestra=session['maestra'], data = data, estado = estado)

@app.route("/revisarInformeFinalEstudiante/<int:idPractica>")
def revisarInformeFinalEstudiante(idPractica):
    infoData = cont_inf_final_est.buscar_id(idPractica)
    
    #Separar las conclusiones y recomendaciones en listas
    conclusiones = infoData[12].split(separadorText)
    recomendaciones = infoData[13].split(separadorText)
    
    estado = infoData#se usa para saber el estado y el texto de observacion 
    data = ["Revisar", infoData[22], infoData[1], infoData[2], [infoData[15], infoData[16], infoData[17], infoData[18], infoData[19], infoData[7], infoData[8], infoData[9], infoData[10], infoData[11], conclusiones, recomendaciones, infoData[14], infoData[20], infoData[4]], infoData[3]]
    #data = ["Revisar", idParactica, "RAZON 1", "DIREC 1", ["giro 1", "repre 1", cantTrabajadoer, "vision", "mision", "infra fisica", "infra tecno", "organigrama.png", "desc area de trabajo", "desc labores", ["conclu 1", "conclu 2", "conclu 3"], ["reco 1", "reco 2", "recomen 34"], "biblio", "anexos.pdf", "introduccion text"]]
    return render_template("/informes/final_estudiante/crudInformeFinal-Estudiante.html", usuario = session['usuario'], maestra=session['maestra'], data = data, estado = estado)

@app.route("/corregir_informeFinalEstudiante", methods=["POST"])
def corregir_informeFinalEstudiante():
    idPractica = request.form["idPractica"]
    idInforme = request.form["idInforme"]

    estado = request.form["btn"]

    if estado == "A":
        cont_inf_final_est.aceptar_informe(idPractica, idInforme)
    else:
        observacion = request.form["observacion"]
        cont_inf_final_est.observar_informe(observacion, idPractica, idInforme)

    return redirect("/detalle_practica/"+idPractica)

@app.route("/guardar_informeFinalEstudiante", methods=["POST"])
def guardar_informeFinalEstudiante():
    
    idPractica = request.form["idPractica"]
    introduccion = request.form["introduccion"]
    giro = request.form["giro"]
    representante = request.form["representante"]
    cantTrabajadores = request.form["cantTrabajadores"]
    vision = request.form["vision"]
    mision = request.form["mision"]
    infraFisica = request.form["infraFisica"]
    infraTecno = request.form["infraTecno"]

    urlBase = "static/practica/" + idPractica + "/informe/final_estudiante"
    if not os.path.exists(urlBase):
        os.makedirs(urlBase)

    organigramaImg = request.files["organigramaImg"]
    urlOrganigrama =  "organigrama" + os.path.splitext(organigramaImg.filename)[1]
    organigramaImg.save(urlBase + "/" + urlOrganigrama)

    descAreaTrabajo = request.form["descAreaTrabajo"]
    descLabores = request.form["descLabores"]
    conclusiones = request.form.getlist("conclusiones")
    recomendaciones = request.form.getlist("recomendaciones")
    bibliografia = request.form["bibliografia"]

    anexosPdf = request.files["anexosPdf"]
    urlAnexos = "anexos" + os.path.splitext(anexosPdf.filename)[1]
    anexosPdf.save(urlBase + "/" + urlAnexos)

    estado = request.form["btn"]

    #Unir las conclusiones y recomendaciones en un string
    conclusiones = separadorText.join(conclusiones)
    recomendaciones = separadorText.join(recomendaciones)
    cont_inf_final_est.insertar(estado, introduccion, infraFisica, infraTecno, urlOrganigrama, descAreaTrabajo, descLabores, conclusiones, recomendaciones, bibliografia, giro, representante, cantTrabajadores, vision, mision, urlAnexos, idPractica)
    return redirect("/detalle_practica/"+idPractica)

@app.route("/actualizar_informeFinalEstudiante", methods=["POST"])
def actualizar_informeFinalEstudiante():
    idPractica = request.form["idPractica"]

    infoData = cont_inf_final_est.buscar_id(idPractica)
    idInforme = request.form["idInforme"]
    introduccion = request.form["introduccion"]
    giro = request.form["giro"]
    representante = request.form["representante"]
    cantTrabajadores = request.form["cantTrabajadores"]
    vision = request.form["vision"]
    mision = request.form["mision"]
    infraFisica = request.form["infraFisica"]
    infraTecno = request.form["infraTecno"]

    urlBase = "static/practica/" + idPractica + "/informe/final_estudiante"
    if not os.path.exists(urlBase):
        os.makedirs(urlBase)

    organigramaImg = request.files["organigramaImg"]
    urlOrganigrama = ''
    if os.path.splitext(organigramaImg.filename)[1] != '':
        urlOrganigrama =  "organigrama" + os.path.splitext(organigramaImg.filename)[1]
        organigramaImg.save(urlBase + "/" + urlOrganigrama)
    else: urlOrganigrama = infoData[9]

    descAreaTrabajo = request.form["descAreaTrabajo"]
    descLabores = request.form["descLabores"]
    conclusiones = request.form.getlist("conclusiones")
    recomendaciones = request.form.getlist("recomendaciones")
    bibliografia = request.form["bibliografia"]

    anexosPdf = request.files["anexosPdf"]
    urlAnexos = ''
    if os.path.splitext(anexosPdf.filename)[1] != '':
        urlAnexos = "anexos" + os.path.splitext(anexosPdf.filename)[1]
        anexosPdf.save(urlBase + "/" + urlAnexos)
    else: urlAnexos = infoData[20]

    estado = request.form["btn"]
    # if "E" in request.form:
    #     estado = "E"
    #Unir las conclusiones y recomendaciones en un string
    conclusiones = separadorText.join(conclusiones)
    recomendaciones = separadorText.join(recomendaciones)

    cont_inf_final_est.actualizar(estado, introduccion, infraFisica, infraTecno, urlOrganigrama, descAreaTrabajo, descLabores, conclusiones, recomendaciones, bibliografia, giro, representante, cantTrabajadores, vision, mision, urlAnexos, idPractica, idInforme)
    return redirect("/detalle_practica/"+idPractica)


@app.route("/visualizar_ife/<int:idPractica>/<string:filename>")
def visualizar_ife(idPractica, filename):
    base = "practica/" + str(idPractica) + "/informe/final_estudiante/"
    url = base + filename
    return send_from_directory('static', url)
     

@app.route("/descargar_pdf/<string:filename>/<int:idPractica>")
def descargar_pdf(filename, idPractica):
    base = "static/practica/" + str(idPractica) + "/informe/final_estudiante/"

    if os.path.splitext(filename)[1] == ".pdf":
        url = base + filename
        return send_file(url, as_attachment=True)
    return None

@app.route("/gife/<int:idPractica>")
@app.route("/generar_informeFinalEstudiante/<int:idPractica>")
def generar_informeFinalEstudiante(idPractica):
    data = list(cont_inf_final_est.buscar_id(idPractica))

    #base = "practica/" + data[22] + "/informe/final_estudiante/"

    #data = ["Carlos Chung", "Empresa 1", "Direccion 1", 1, "texto de la introduccion", "A", "20/10/2023", "texto de la infra fisica", "texto de la infra tecnologica", "organigrama.png", "descripcion del area relaciones", "descripcion de labores", ["conclu 1", "conclu 2", "conclu 3"], ["reco 1", "reco 2", "recomen 34"], "bibliografia \nreferencia1 \nreferencia 2", "giro de la empresa", "representante legal de la empresa", 20, "vision", "mision", "anexos.pdf", 'observacion hecho por el docente', 1]

    #Separar las conclusiones y recomendaciones en listas
    data[12] = data[12].split(separadorText)
    data[13] = data[13].split(separadorText)
    
    urlLogo = request.scheme + '://'+ request.host +'/static/Logo_USAT.png'
    urlOrganigrama = request.scheme + '://'+ request.host +'/static/practica/1/informe/final_estudiante/' + data[9]
    print(urlLogo)
    print(urlOrganigrama)
    
    context_caratula = {'nombre_apellido_estudiante': data[0], 'centro_practica': data[1], 'fecha_entrega': data[6], 'logo': urlLogo}
    context_contenido = {'introduccion': data[4],'razon_social': data[1],'direccion': data[2],'giro_institucion': data[15],'representante_legal': data[16],'cantidad_trabajadores': data[17],'vision': data[18],'mision': data[19],'infra_fisica': data[7],'infra_tecno': data[8],'organigrama': urlOrganigrama,'desc_area': data[10],'desc_labores': data[11],'conclusiones': data[12],'recomendaciones': data[13],'bibliografia': data[14]}

    #Generamos la caratula para el informe
    output_text_caratula = render_template("/informes/final_estudiante/caratula.html", context = context_caratula)
    output_pdf_caratula = 'static/practica/' + str(idPractica) + '/informe/final_estudiante/caratula.pdf'
    pdfkit.from_string(output_text_caratula, output_pdf_caratula, configuration=config, options={"enable-local-file-access": "", 'encoding': 'UTF-8'})

    #Generamos el contenido para el informe
    output_text_contenido = render_template("/informes/final_estudiante/contenido.html", context = context_contenido)
    output_pdf_contenido = 'static/practica/' + str(idPractica) + '/informe/final_estudiante/contenido.pdf'
    pdfkit.from_string(output_text_contenido, output_pdf_contenido, configuration=config, options={"enable-local-file-access": ""})

    #Unimos la caratula, el contenido y los anexos para obtener el informe completo
    merger = PdfMerger()
    merger.append(PdfReader(output_pdf_caratula))
    merger.append(PdfReader(output_pdf_contenido))
    merger.append(PdfReader('static/practica/' + str(idPractica) + '/informe/final_estudiante/anexos.pdf'))

    merger.write('static/practica/'+ str(idPractica) + '/informe/final_estudiante/informe_final_estudiante.pdf')

    return send_file('static/practica/'+ str(idPractica) + '/informe/final_estudiante/informe_final_estudiante.pdf', as_attachment=True)
    # return redirect("/agregarInformeFinalEstudiante")

#################################################################################
##                          INFORME FINAL - EMPRESA                            ##
#################################################################################

@app.route("/nuevo_ifem/<int:id>")
def nuevo_ifem(id):
    data = cont_inf_final_emp.infoPlantilla(id)
    print(data)
    return render_template("/informes/final_empresa/crudInformeFinal-Empresa.html",data=data,usuario = session['usuario'], maestra=session['maestra'])


###     MOSTRAR FORMULARIO DE INFORME FINAL

@app.route("/guardar_ifem", methods=["POST"])
def guardar_ifem():
    idPractica = request.form["idPractica"]
    fechaEntrega = datetime.date.today()

    observacion = ""
    
    urlBase = "static/practica/"+str(idPractica)+"/informe/final_empresa"
    if not os.path.exists(urlBase):
        os.makedirs(urlBase)
    selloImg = request.files["selloEmpImg"]
    urlSelloEmpresa = urlBase + "/sello" + os.path.splitext(selloImg.filename)[1]
    selloImg.save(urlSelloEmpresa)

    firmaImg = request.files["firmaResImg"]
    urlFirmaResponsable = urlBase + "/firma" + os.path.splitext(firmaImg.filename)[1]
    firmaImg.save(urlFirmaResponsable)


    valoraciones = request.form.getlist('valoraciones')
    
    if 'btnGuardar' in request.form:
        cont_inf_final_emp.insertar_informe_final_empresa(idPractica,"G",fechaEntrega,urlFirmaResponsable,urlSelloEmpresa,observacion,idPractica)
    if 'btnEnviar' in request.form:
        cont_inf_final_emp.insertar_informe_final_empresa(idPractica,"E",fechaEntrega,urlFirmaResponsable,urlSelloEmpresa,observacion,idPractica)

    for valoracion in valoraciones:
        cont_inf_final_emp.insertar_valoracion(valoracion,idPractica)
    
    return redirect("/detalle_practica/"+idPractica)


@app.route("/ver_ifem/<int:id>")
def ver_ifem(id):
    data = list(cont_inf_final_emp.buscar_id(id))
    val = cont_inf_final_emp.buscar_valoracion(id)
    valoraciones = [item[0] for item in val]
    data[6]=request.scheme + '://'+ request.host +'/'+ data[6]
    data[7]=request.scheme + '://'+ request.host +'/'+ data[7]
    return render_template("/informes/final_empresa/verInforme.html",valoraciones=valoraciones, data = data,  usuario = session['usuario'], maestra=session['maestra'])



@app.route("/actualizar_ifem", methods=["POST"])
def actualizar_ifem():
    idInforme = request.form["idInforme"]
    idPractica = request.form["idPractica"]

    urlBase = "static/practica/"+str(idPractica)+"/informe/final_empresa"
    if not os.path.exists(urlBase):
        os.makedirs(urlBase)

    
    selloImg = request.files["selloEmpImg"]
    urlSelloEmpresa = urlBase + "/sello" + os.path.splitext(selloImg.filename)[1]
    selloImg.save(urlSelloEmpresa)
    
    firmaImg = request.files["firmaResImg"]
    urlFirmaResponsable = urlBase + "/firma" + os.path.splitext(firmaImg.filename)[1]
    firmaImg.save(urlFirmaResponsable)

    print(idInforme)
    print(urlSelloEmpresa)
    print(urlFirmaResponsable)

    if 'btnGuardar' in request.form:
        cont_inf_final_emp.actualizar_informe_final_empresa("G",urlFirmaResponsable,urlSelloEmpresa,idInforme)
    if 'btnActualizarEnviar' in request.form:
        cont_inf_final_emp.actualizar_informe_final_empresa("E",urlFirmaResponsable,urlSelloEmpresa,idInforme)
    return redirect("/detalle_practica/"+idPractica)

@app.route("/generar_informeFinalEmpresa/<int:id>")
def generar_informeFinalEmpresa(id):
    #controlador obtener
    data = cont_inf_final_emp.buscar_id(id)
    data2 = cont_inf_final_emp.buscar_valoracion(id)
    lista_resultante = [item[0] for item in data2]
    idPractica = data[14]
    firmas = [request.scheme +'://'+ request.host +'/'+data[6],request.scheme +'://'+ request.host +'/'+data[7]]

    context_contenido = {'nombreEmpresa': data[0],'responsable': data[1],'cargo': data[2],'estudiante': data[3],'fechaInicio': data[4],'fechaFin': data[5],
                         "valoraciones": lista_resultante,'urlFirma': data[6],'urlSello': data[7]}

    #Generamos el contenido para el informe
    output_text_contenido = render_template("/informes/final_empresa/contenido.html", context = context_contenido,firmas=firmas)

    output_pdf_contenido = 'static/practica/' + str(idPractica) + '/informe/final_empresa'
    if not os.path.exists(output_pdf_contenido):
        os.makedirs(output_pdf_contenido)
    output_pdf_contenido += "/informe_final_empresa.pdf"
    pdfkit.from_string(output_text_contenido, output_pdf_contenido, configuration=config, options={"enable-local-file-access": ""})

    return send_file('static/practica/'+ str(idPractica) + '/informe/final_empresa/informe_final_empresa.pdf', as_attachment=True)

#################################################################################
##                                  SEMESTRE                                   ##
#################################################################################

###     MOSTRAR SEMESTRES
@app.route("/semestres")
def semestres():
    semestres = cont_sem.obtener_semestre()
    usu = session['usuario']
    #print("Datos:",usu)
    return render_template("/semestre/listarSemestre.html", usuario = usu, maestra="maestra_d_modulo2.html", semestres = semestres)


###     AGREGAR SEMESTRE
@app.route("/agregar_semestre")
def agregar_semestre():
    return render_template("/semestre/nuevoSemestre.html", usuario = session['usuario'], maestra="maestra_d_modulo2.html")

@app.route("/guardar_semestre", methods=["POST"])
def guardar_semestre():

    nombreSe = request.form["nombreSe"]
    fechaI = request.form["fechaI"]
    fechaF = request.form["fechaF"]
    estado = request.form["estado"]

    cont_sem.insertar_semestre(nombreSe, fechaI,fechaF,estado)
    return redirect("/semestres")


###     EDITAR SEMESTRE
@app.route("/editar_semestre/<int:id>")
def editar_semestre(id):
    semestre = cont_sem.buscar_semestre_id(id)
    opt = False
    if(semestre[4] == 'V'):
        opt = True

    return render_template("/semestre/editarSemestre.html", usuario = session['usuario'], maestra="maestra_d_modulo2.html", semestre=semestre, opt=opt)

@app.route("/actualizar_semestre", methods=["POST"])
def actualizar_semestre():
    idSemestre = request.form["idSemestre"]
    nombreSe = request.form["nombreSe"]
    fechaI = request.form["fechaI"]
    fechaF = request.form["fechaF"]
    estado = request.form["estado"]

    cont_sem.actualizar_semestre(nombreSe, fechaI,fechaF,estado, idSemestre)

    return redirect("/semestres")

###     DAR DE BAJA SEMESTRE
@app.route("/darbaja_semestre/<int:id>")
def darbaja_semestre(id):
    cont_sem.dar_baja(id)
    return redirect("/semestres")

###     DAR DE ALTA SEMESTRE
@app.route("/daralta_semestre/<int:id>")
def daralta_semestre(id):
    cont_sem.dar_alta(id)
    return redirect("/semestres")

###     ELIMINAR SEMESTRE
@app.route("/eliminar_semestre/<int:id>")
def eliminar_semestre(id):
    cont_sem.eliminar_semestre(id)
    return redirect("/semestres")


#################################################################################
##                                  FACULTAD                                   ##
#################################################################################

@app.route("/facultades")
def facultades():
    if 'usuario' in session and session['usuario'][4] == 'Docente de apoyo':
        facultades = cont_fac.obtener_facultad()
        usu = session['usuario']
        return render_template("/facultad/listarFacultad.html", usuario = usu, maestra="maestra_d_modulo2.html", facultades = facultades)
    else:
        return redirect('/index_supremo')


###     AGREGAR FACULTAD
@app.route("/agregar_facultad")
def agregar_facultad():
    return render_template("/facultad/nuevaFacultad.html" , usuario = session['usuario'], maestra="maestra_d_modulo2.html")

@app.route("/guardar_facultad", methods=["POST"])
def guardar_facultad():

    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    estado = request.form["estado"]

    cont_fac.insertar_facultad(nombre, descripcion, estado)
    return redirect("/facultades")


###     EDITAR FACULTAD
@app.route("/editar_facultad/<int:id>")
def editar_facultad(id):
    facultad = cont_fac.buscar_facultad_id(id)
    opt = False
    if(facultad[3] == 'V'):
        opt = True

    return render_template("/facultad/editarFacultad.html", usuario = session['usuario'], maestra="maestra_d_modulo2.html", facultad=facultad, opt=opt)

@app.route("/actualizar_facultad", methods=["POST"])
def actualizar_facultad():
    id = request.form["id"]
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    estado = request.form["estado"]
    print("DATOS DE ACTUALIZAR ", id, nombre, descripcion, estado)
    cont_fac.actualizar_facultad(nombre, descripcion, estado, id)

    return redirect("/facultades")

###     DAR DE BAJA FACULTAD
@app.route("/darbaja_facultad/<int:id>")
def darbaja_facultad(id):
    cont_fac.dar_baja(id)
    return redirect("/facultades")

###     DAR DE ALTA FACULTAD
@app.route("/daralta_facultad/<int:id>")
def daralta_facultad(id):
    cont_fac.dar_alta(id)
    return redirect("/facultades")

###     ELIMINAR FACULTAD
@app.route("/eliminar_facultad/<int:id>")
def eliminar_facultad(id):
    try:
        cont_fac.eliminar_facultad(id)
        return redirect("/facultades")
    except Exception as e:
        
        return render_template('error2.html', error_message=str(e))



#################################################################################
##                                  ESCUELA                                    ##
#################################################################################


@app.route("/escuelas")
def escuelas():
    if 'usuario' in session and session['usuario'][4] == 'Docente de apoyo':
        escuelas = cont_esc.obtener_escuela()
        usu = session['usuario']
    #print("Datos:",usu)
        return render_template("/escuela/listarEscuela.html", usuario = usu, maestra="maestra_d_modulo2.html", escuelas = escuelas)
    else:
        return redirect('/index_supremo')




###     BUSCAR ESCUELA
@app.route("/escuelas", methods=["POST"])
def escuelas_nombre():
    nombre = request.form["nombre"]
    escuelas = cont_esc.buscar_escuela(nombre)
    return render_template("/escuela/listarEscuela.html", usuario = session['usuario'], maestra="maestra_d_modulo2.html", escuelas = escuelas, editEscuela = None)


###     AGREGAR ESCUELA
@app.route("/agregar_escuela")
def agregar_escuela():
    facultades = cont_esc.listarFacultades()
    return render_template("/escuela/nuevaEscuela.html", usuario = session['usuario'], maestra="maestra_d_modulo2.html",facultades=facultades)

@app.route("/guardar_escuela", methods=["POST"])
def guardar_escuela():

    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    estado = request.form["estado"]
    idFacultad = request.form["idFacultad"]

    cont_esc.insertar_escuela(nombre, descripcion, estado, idFacultad)
    return redirect("/escuelas")


###     EDITAR ESCUELA
@app.route("/editar_escuela/<int:id>")
def editar_escuela(id):
    facultades = cont_esc.listarFacultades()
    escuela = cont_esc.buscar_escuela_id(id)
    opt = False
    if(escuela[3] == 'V'):
        opt = True

    return render_template("/escuela/editarEscuela.html", usuario = session['usuario'], maestra="maestra_d_modulo2.html", escuela=escuela,facultades=facultades, opt=opt)

@app.route("/actualizar_escuela", methods=["POST"])
def actualizar_escuela():
    id = request.form["id"]
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    estado = request.form["estado"]
    idFacultad = request.form["idFacultad"]
     
    cont_esc.actualizar_escuela(nombre, descripcion, estado, idFacultad, id)

    return redirect("/escuelas")

###     DAR DE BAJA ESCUELA
@app.route("/darbaja_escuela/<int:id>")
def darbaja_escuela(id):
    cont_esc.dar_baja(id)
    return redirect("/escuelas")

###     DAR DE ALTA ESCUELA
@app.route("/daralta_escuela/<int:id>")
def daralta_escuela(id):
    cont_esc.dar_alta(id)
    return redirect("/escuelas")

###     ELIMINAR ESCUELA
@app.route("/eliminar_escuela/<int:id>")
def eliminar_escuela(id):
    try:
        cont_esc.eliminar_escuela(id)
        return redirect("/escuelas")
    except Exception as e:
        
        return render_template('error.html', error_message=str(e))


#################################################################################
##                                ESTUDIANTE                                   ##
#################################################################################

###     MOSTRAR ESTUDIANTES
@app.route("/estudiantes")
def estudiantes():
    if 'usuario' in session and session['usuario'][4] == 'Docente de apoyo':
        estudiantes = cont_est.obtener_estudiante()
        usu = session['usuario']
    #print("Datos:",usu)
        return render_template("/estudiante/listarEstudiante.html", usuario = usu, maestra="maestra_d_modulo2.html", estudiantes = estudiantes,error_statement="")
    else:
        return redirect('/index_supremo')


###     DAR DE BAJA ESTUDIANTE
@app.route("/darbaja_estudiante/<int:id>")
def darbaja_estudiante(id):
    cont_est.dar_baja(id)
    return redirect("/estudiantes")

###     DAR DE ALTA ESTUDIANTE
@app.route("/daralta_estudiante/<int:id>")
def daralta_estudiante(id):
    cont_est.dar_alta(id)
    return redirect("/estudiantes")



#################################################################################
##                                   EMPRESA                                   ##
#################################################################################

@app.route("/empresas")
def empresas():
    empresas = cont_emp.obtener_empresa()
    usu = session['usuario']
    return render_template("/empresa/listarEmpresa.html", usuario = usu, maestra="maestra_d_modulo1.html", empresas = empresas)



###     BUSCAR EMPRESA
@app.route("/empresas", methods=["POST"])
def empresas_nombre():
    razonSocial = request.form["razonSocial"]
    empresas = cont_emp.buscar_empresa(razonSocial)
    return render_template("/empresa/ListaEmpresa.html", empresas = empresas, maestra="maestra_d_modulo1.html", editEmpresa = None)


###     AGREGAR EMPRESA
@app.route("/agregar_empresa")
def agregar_empresa():
    paises = cont_emp.listar_pais()
    dep = cont_emp.listar_departamento()
    return render_template("/empresa/nuevaEmpresa.html", paises = paises, dep = dep,  usuario = session['usuario'], maestra="maestra_d_modulo1.html")

@app.route("/buscar_prov_dep", methods=["GET"])
def buscar_prov_dep():
    dep = request.args.get('departamento')
    prov = cont_emp.listar_provincia(dep)
    return jsonify(prov)

@app.route("/buscar_dis_prov", methods=["GET"])
def buscar_dis_prov():
    prov = request.args.get('provincia')
    dis = cont_emp.listar_distrito(prov)
    return jsonify(dis)

@app.route("/guardar_empresa", methods=["POST"])
def guardar_empresa():

    razonSocial = request.form["razonSocial"]
    ruc = request.form["ruc"]
    direccion = request.form["direccion"]
    telefono = request.form["telefono"]
    telefono2 = request.form["telefono2"]
    correo = request.form["correo"]
    pais = request.form["pais"]
    distrito = request.form["distrito"]

    if pais == '24':
        cont_emp.insertar_empresa_nacional(razonSocial,direccion,ruc,telefono,telefono2,correo,distrito)
    else: cont_emp.insertar_empresa_internacional(razonSocial,direccion,ruc,telefono,telefono2,correo,pais)
    return redirect("/empresas")


###     EDITAR EMPRESA
@app.route("/editar_empresa/<int:id>")
def editar_empresa(id):
    empresa = cont_emp.buscar_empresa_id(id)
    paises = cont_emp.listar_pais()
    dep = cont_emp.listar_departamento()
    if (empresa[9] == None):
        info = cont_emp.empresa_nacional(empresa[8])
        prov = cont_emp.listar_provincia(info[1])
        dis = cont_emp.listar_distrito(info[2])
        bandera = True
        disable = ''
        return render_template("/empresa/editarEmpresa.html", empresa=empresa, paises=paises, dep = dep, info = info, prov = prov, dis = dis, bandera = bandera, disable = disable ,  usuario = session['usuario'], maestra=session['maestra'])
    else: 
        info = cont_emp.nombrePais(empresa[9])
        bandera = False
        disable = 'disabled'
        return render_template("/empresa/editarEmpresa.html", empresa=empresa, paises=paises, dep = dep, info = info, bandera = bandera, disable = disable ,  usuario = session['usuario'], maestra=session['maestra'])

@app.route("/ver_empresa/<int:id>")
def ver_empresa(id):
    empresa = cont_emp.buscar_empresa_id(id)
    paises = cont_emp.listar_pais()
    dep = cont_emp.listar_departamento()
    if (empresa[9] == None):
        info = cont_emp.empresa_nacional(empresa[8])
    else: 
        info = cont_emp.nombrePais(empresa[9])
    return render_template("/empresa/verEmpresa.html", empresa=empresa, paises=paises, dep = dep, info = info ,  usuario = session['usuario'], maestra="maestra_d_modulo1.html")

@app.route("/actualizar_empresa", methods=["POST"])
def actualizar_empresa():
    id = request.form["idEmpresa"]
    razonSocial = request.form["razonSocial"]
    ruc = request.form["ruc"]
    direccion = request.form["direccion"]
    telefono = request.form["telefono"]
    telefono2 = request.form["telefono2"]
    correo = request.form["correo"]
    pais = request.form["pais"]
    if pais == '24':
        distrito = request.form["distrito"]
        cont_emp.actualizar_empresa_nacional(razonSocial,direccion,ruc,telefono,telefono2,correo,distrito,id)
    else: 
        cont_emp.actualizar_empresa_internacional(razonSocial,direccion,ruc,telefono,telefono2,correo,pais,id)
    return redirect("/empresas")

###     ELIMINAR EMPRESA
@app.route("/eliminar_empresa/<int:id>")
def eliminar_empresa(id):
    cont_emp.eliminar_empresa(id)
    return redirect("/empresas")

#################################################################################
##                         INFORME INICIAL EMPRESA                             ##
#################################################################################

@app.route("/nuevo_iie/<int:id>")
def nuevo_iie(id):
    info = cont_iie.infoPlantilla(id)
    return render_template("/informe_inicial_empresa/nuevoInforme.html",info = info, usuario = session['usuario'], maestra=session['maestra'])

@app.route("/guardar_iie", methods=["POST"])
def guardar_iie():

    idPractica = request.form["idPractica"]
    urlBase = "static/practica/" + idPractica + "/informe/inicial_empresa"
    if not os.path.exists(urlBase):
        os.makedirs(urlBase)

    aceptacion = request.files["aceptArch"]
    urlAcept = urlBase + "/aceptacion" + os.path.splitext(aceptacion.filename)[1]
    aceptacion.save(urlAcept)

    firma = request.files["firma"]
    urlFirma = urlBase + "/firma" + os.path.splitext(firma.filename)[1]
    firma.save(urlFirma)

    sello = request.files["sello"]
    urlSello = urlBase + "/sello" + os.path.splitext(sello.filename)[1]
    sello.save(urlSello)

    fechaEntrega = request.form["fechaE"]
    labores = cont_iie.concat_labores(request.form.getlist("labor"))
    if 'btnGuardar' in request.form:
        cont_iie.insertar_informe_inicial_empresa("G",urlAcept,fechaEntrega,labores,urlFirma,urlSello,idPractica)
    if 'btnEnviar' in request.form:
        cont_iie.insertar_informe_inicial_empresa("E",urlAcept,fechaEntrega,labores,urlFirma,urlSello,idPractica)
    return redirect("/detalle_practica/"+idPractica)

@app.route("/editar_iie/<int:id>")
def editar_iie(id):
    info = cont_iie.infoPlantilla(id)
    iie = cont_iie.buscar_informe_inicial_empresa_id(id)
    acep = iie[1]
    labores = cont_iie.desconcat_labores(iie[3])
    img = ['']
    img[0]=request.scheme + '://'+ request.host +'/'+ iie[1]
    img.append(request.scheme + '://'+ request.host +'/'+ iie[4])
    img.append(request.scheme + '://'+ request.host +'/'+ iie[5])
    print(iie[1])
    if len(labores) == 1:
        labores[0] = iie[3]
        bandera = False
    else: 
        bandera = True
    return render_template("/informe_inicial_empresa/editarInforme.html", iie=iie, labores=labores, acep = acep,info = info, bandera = bandera,img = img,  usuario = session['usuario'], maestra=session['maestra'])

@app.route("/ver_iie/<int:id>")
def ver_iie(id):
    info = cont_iie.infoPlantilla(id)
    iie = cont_iie.buscar_informe_inicial_empresa_id(id)
    acep = iie[1]
    labores = cont_iie.desconcat_labores(iie[3])
    img = ['']
    img[0]=request.scheme + '://'+ request.host +'/'+ iie[1]
    img.append(request.scheme + '://'+ request.host +'/'+ iie[4])
    img.append(request.scheme + '://'+ request.host +'/'+ iie[5])
    print(iie[1])
    if len(labores) == 1:
        labores[0] = iie[3]
        bandera = False
    else: 
        bandera = True
    return render_template("/informe_inicial_empresa/verInforme.html", iie=iie, labores=labores, acep = acep,info = info, bandera = bandera,img = img,  usuario = session['usuario'], maestra=session['maestra'])

@app.route("/actualizar_iie", methods=["POST"])
def actualizar_iie():
    idInforme = request.form["idInforme"]
    idPractica = request.form["idPractica"]
    iie = cont_iie.buscar_informe_inicial_empresa_id(idPractica)
    urlBase = "static/practica/" + idPractica + "/informe/inicial_empresa"
    if not os.path.exists(urlBase):
        os.makedirs(urlBase)

    aceptacion = request.files["aceptArch"]
    if os.path.splitext(aceptacion.filename)[1] != '':
        urlAcept = urlBase + "/aceptacion" + os.path.splitext(aceptacion.filename)[1]
        aceptacion.save(urlAcept)
    else: urlAcept = iie[1]

    firma = request.files["firma"]
    if os.path.splitext(firma.filename)[1] != '':
        urlFirma = urlBase + "/firma" + os.path.splitext(firma.filename)[1]
        firma.save(urlFirma)
    else: urlFirma = iie[4]

    sello = request.files["sello"]
    if os.path.splitext(sello.filename)[1] != '':
        urlSello = urlBase + "/sello" + os.path.splitext(sello.filename)[1]
        sello.save(urlSello)
    else: urlSello = iie[5]

    fechaEntrega = request.form["fechaE"]
    labores = cont_iie.concat_labores(request.form.getlist("labor"))
    if 'btnGuardar' in request.form:
        cont_iie.actualizar_informe_inicial_empresa("G",urlAcept,fechaEntrega,labores,urlFirma,urlSello,idInforme)
    if 'btnEnviar' in request.form:
        cont_iie.actualizar_informe_inicial_empresa("E",urlAcept,fechaEntrega,labores,urlFirma,urlSello,idInforme)
    return redirect("/detalle_practica/"+idPractica)

@app.route("/generar_iie/<int:id>")
def generar_iie(id):

    infoPlantilla = cont_iie.infoPlantilla(id)
    infoInforme = cont_iie.buscar_informe_inicial_empresa_id(id)
    labores = []
    labores = cont_iie.desconcat_labores(infoInforme[3])
    print(infoInforme)
    img = [request.scheme +'://'+ request.host +'/'+infoInforme[1],request.scheme +'://'+ request.host +'/'+infoInforme[4],request.scheme +'://'+ request.host +'/'+infoInforme[5]]

    html = render_template('/informe_inicial_empresa/plantilla.html', infoP = infoPlantilla, infoI = infoInforme, lab = labores, img = img)
    pdfkit.from_string(html, 'static/practica/'+str(id)+'/informe/inicial_empresa/informe_inicial_empresa.pdf', configuration=config)
    return send_file('static/practica/'+str(id)+'/informe/inicial_empresa/informe_inicial_empresa.pdf', as_attachment=True)

#################################################################################
##                                  REPORTE                                   ##
#################################################################################

@app.route("/reporte1aa")
def reportes1():
    reportes1 = cont_rep.obtener_reporte_1()
    reportes2 = cont_rep.obtener_reporte_2()
    return render_template("/reportes/abc.html", usuario = session['usuario'], maestra=session['maestra'],reportes1 = reportes1,reportes2 = reportes2)


#################################################################################
##                                DISTRITO                                    ##
#################################################################################

###     MOSTRAR DISTRITO
@app.route("/distrito")
def distrito():
    if 'usuario' in session and session['usuario'][4] == 'Docente de apoyo':
        ubicaciones = cont_ubi.listar_distritos()
        return render_template("/ubicacion/distrito/listarDistritos.html", usuario = session['usuario'], maestra="maestra_d_modulo2.html", ubicaciones = ubicaciones)
    else:
        return redirect('/index_supremo')


###     AGREGAR DISTRITO
@app.route("/agregar_distrito")
def agregar_distrito():
    #datos_paises = cont_ubi.datos_departamentos(24)
    return render_template("/ubicacion/distrito/nuevoDistrito.html", usuario = session['usuario'], maestra=session['maestra'])

@app.route("/guardar_distrito", methods=["POST"])
def guardar_distrito():
    nombre = request.form["distrito"]
    idPro = request.form["provincia"]

    cont_ubi.insertar_distrito(nombre, idPro)
    flash('Distrito registrado satisfactoriamente', 'message')
    return redirect("/distrito")


###     EDITAR DISTRITO
@app.route("/editar_distrito/<int:id>")
def editar_distrito(id):
    data = cont_ubi.buscar_distrito(id)
    datos_paises = cont_ubi.datos_paises()
    departamentos = cont_ubi.datos_departamentos(data[2])
    provincias = cont_ubi.datos_provincias(data[3])

    return render_template("/ubicacion/distrito/editarDistrito.html", usuario = session['usuario'], maestra="maestra_d_modulo2.html", paises = datos_paises, data=data, departamentos = departamentos, provincias = provincias)

@app.route("/actualizar_distrito", methods=["POST"])
def actualizar_distrito():
    idDistrito = request.form["idDistrito"]
    nombre = request.form["distrito"]
    idPro = request.form["provincia"]
    cont_ubi.actualizar_distrito(nombre, idPro, idDistrito)

    return redirect("/distrito")


###     ELIMINAR DISTRITO
@app.route("/eliminar_distrito/<int:id>")
def eliminar_distrito(id):
    cont_ubi.eliminar_distrito(id)
    return redirect("/distrito")

#################################################################################
##                                PROVINCIA                                    ##
#################################################################################

###     MOSTRAR PROVINCIA
@app.route("/provincia")
def provincia():
    if 'usuario' in session and session['usuario'][4] == 'Docente de apoyo':
        ubicaciones = cont_ubi.listar_provincias()
        return render_template("/ubicacion/provincia/listarProvincia.html", usuario = session['usuario'], maestra="maestra_d_modulo2.html", ubicaciones = ubicaciones)
    else:
        return redirect('/')


###     AGREGAR PROVINCIA
@app.route("/agregar_provincia")
def agregar_provincia():
    datos_paises = cont_ubi.datos_paises()
    return render_template("/ubicacion/provincia/nuevoProvincia.html", usuario = session['usuario'], maestra="maestra_d_modulo2.html", paises = datos_paises)

@app.route("/guardar_provincia", methods=["POST"])
def guardar_provincia():
    nombre = request.form["provincia"]
    idDep = request.form["departamento"]

    cont_ubi.insertar_provincia(nombre, idDep)
    return redirect("/provincia")


###     EDITAR PROVINCIA
@app.route("/editar_provincia/<int:id>")
def editar_provincia(id):
    data = cont_ubi.buscar_provincia(id)
    datos_paises = cont_ubi.datos_paises()
    departamentos = cont_ubi.datos_departamentos(data[2])

    return render_template("/ubicacion/provincia/editarProvincia.html", usuario = session['usuario'], maestra="maestra_d_modulo2.html", paises = datos_paises, data=data, departamentos = departamentos)

@app.route("/actualizar_provincia", methods=["POST"])
def actualizar_provincia():
    idProvincia = request.form["idProvincia"]
    nombre = request.form["provincia"]
    idDep = request.form["departamento"]
    cont_ubi.actualizar_provincia(nombre, idDep, idProvincia)

    return redirect("/provincia")


###     ELIMINAR PROVINCIA
@app.route("/eliminar_provincia/<int:id>")
def eliminar_provincia(id):
    cont_ubi.eliminar_provincia(id)
    return redirect("/provincia")

#################################################################################
##                                DEPARTAMENTO                                    ##
#################################################################################

###     MOSTRAR DEPARTAMENTO
@app.route("/departamento")
def departamento():
    if 'usuario' in session and session['usuario'][4] == 'Docente de apoyo':
        ubicaciones = cont_ubi.listar_departamento()
        return render_template("/ubicacion/departamento/listarDepartamento.html", usuario = session['usuario'], maestra="maestra_d_modulo2.html", ubicaciones = ubicaciones)
    else:
        return redirect('/')


###     AGREGAR DEPARTAMENTO
@app.route("/agregar_departamento")
def agregar_departamento():
    datos_paises = cont_ubi.datos_paises()
    return render_template("/ubicacion/departamento/nuevoDepartamento.html", usuario = session['usuario'], maestra="maestra_d_modulo2.html", paises = datos_paises)

@app.route("/guardar_departamento", methods=["POST"])
def guardar_departamento():
    nombre = request.form["departamento"]
    idPais = request.form["pais"]

    cont_ubi.insertar_departamento(nombre, idPais)
    return redirect("/departamento")


###     EDITAR DEPARTAMENTO
@app.route("/editar_departamento/<int:id>")
def editar_departamento(id):
    data = cont_ubi.buscar_departamento(id)
    datos_paises = cont_ubi.datos_paises()

    return render_template("/ubicacion/departamento/editarDepartamento.html", usuario = session['usuario'], maestra="maestra_d_modulo2.html", paises = datos_paises, data=data)

@app.route("/actualizar_departamento", methods=["POST"])
def actualizar_departamento():
    idDepartamento = request.form["idDepartamento"]
    nombre = request.form["departamento"]
    idPais = request.form["pais"]
    cont_ubi.actualizar_departamento(nombre, idPais, idDepartamento)

    return redirect("/departamento")


###     ELIMINAR DEPARTAMENTO
@app.route("/eliminar_departamento/<int:id>")
def eliminar_departamento(id):
    cont_ubi.eliminar_departamento(id)
    return redirect("/departamento")

#################################################################################
##                                   PAIS                                      ##
#################################################################################

###     MOSTRAR PAIS
@app.route("/pais")
def pais():
    if 'usuario' in session and session['usuario'][4] == 'Docente de apoyo':
        ubicaciones = cont_ubi.listar_pais()
        return render_template("/ubicacion/pais/listarPais.html", usuario = session['usuario'], maestra="maestra_d_modulo2.html", ubicaciones = ubicaciones)
    else:
        return redirect('/')


###     AGREGAR PAIS
@app.route("/agregar_pais")
def agregar_pais():
    return render_template("/ubicacion/pais/nuevoPais.html", usuario = session['usuario'], maestra="maestra_d_modulo2.html")

@app.route("/guardar_pais", methods=["POST"])
def guardar_pais():
    nombre = request.form["pais"]

    cont_ubi.insertar_pais(nombre)
    return redirect("/pais")


###     EDITAR PAIS
@app.route("/editar_pais/<int:id>")
def editar_pais(id):
    data = cont_ubi.buscar_pais(id)

    return render_template("/ubicacion/pais/editarPais.html", usuario = session['usuario'], maestra="maestra_d_modulo2.html", data=data)

@app.route("/actualizar_pais", methods=["POST"])
def actualizar_pais():
    idPais = request.form["idPais"]
    nombre = request.form["pais"]
    cont_ubi.actualizar_pais(nombre, idPais)

    return redirect("/pais")


###     ELIMINAR PAIS
@app.route("/eliminar_pais/<int:id>")
def eliminar_pais(id):
    cont_ubi.eliminar_pais(id)
    return redirect("/pais")


#################################################################################
##                       APIS PARA DATOS DE UBICACION                          ##
#################################################################################
@app.route('/obtener_paises', methods=['GET'])
def obtener_paises():
    datos_paises = cont_ubi.datos_paises()
    return jsonify(paises=datos_paises)

@app.route('/obtener_departamentos', methods=['GET'])
def obtener_departamentos():
    pais_seleccionado = request.args.get('pais')
    departamentos = cont_ubi.datos_departamentos(pais_seleccionado)
    return jsonify(departamentos=departamentos)

@app.route('/obtener_provincias', methods=['GET'])
def obtener_provincias():
    departamento_seleccionado = request.args.get('departamento')
    provincias = cont_ubi.datos_provincias(departamento_seleccionado)
    return jsonify(provincias=provincias)

#################################################################################
##                            Jefe_Inmediato                                   ##
#################################################################################
@app.route("/JefeInmediato")
def JefeInmediato():
    jefes = controlador_jefe_inmediato.obtener_Jefe()
    return render_template("/Jefe_Inmediato/jefe.html", jefes=jefes, usuario = session['usuario'], maestra=session['maestra'])

@app.route("/DetalleJefeInmediato/<int:id>")
def DetalleJefeInmediato(id):
    jefes = controlador_jefe_inmediato.obtener_DetalleJefe(id)
    return render_template("/Jefe_Inmediato/detalle_jefe.html", jefes=jefes, usuario = session['usuario'], maestra=session['maestra'])

@app.route("/AgregarJefeInmediato")
def AgregarJefeInmediato():
    jefes = controlador_jefe_inmediato.obtener_Jefe()
    departamentos=cont_localidad.obtener_Departamento()
    distritos=cont_localidad.obtener_Distrito()
    provincias=cont_localidad.obtener_Provincia()
    empresas=cont_emp.obtener_empresa()
    
    return render_template("/Jefe_Inmediato/nuevoJefe.html",empresas=empresas, jefes=jefes,departamentos=departamentos,distritos=distritos,provincias=provincias, usuario = session['usuario'], maestra=session['maestra'])

@app.route("/guardarJefe", methods=["POST"])
def guardarJefe():
    nombre = request.form["nombre"]
    apellidos = request.form["apellidos"]
    telefono = request.form["telefono"]
    telefono2 = request.form["telefono2"]
    correo = request.form["correo"]
    correo2 = request.form["correo2"]
    cargo = request.form["cargo"]
    turno = request.form["turno"]
    empresa = request.form["empresa"]
    usuario = request.form["usuario"]
    contraseña = request.form["contraseña"]
    distrito = request.form["distrito"]
    controlador_jefe_inmediato.insertar_JEFE(nombre ,apellidos,telefono,telefono2,correo ,correo2 ,cargo ,turno ,empresa ,usuario,contraseña,distrito)
    # De cualquier modo, y si todo fue bien, redireccionar
    return redirect("/JefeInmediato")

@app.route("/JefeInmediatoID/<int:id>")
def JefeInmediatoID(id):
    jefes = controlador_jefe_inmediato.obtener_DetalleJefeID(id)
    idJefe=jefes[0][10]
    usuarioJefe=controlador_jefe_inmediato.obtener_UsuarioJefe(idJefe)
    distritos=cont_localidad.obtener_Distrito()
    empresas=cont_emp.obtener_empresa()
    return render_template("/Jefe_Inmediato/editarJefe.html", jefes=jefes,UsuarioJefe=usuarioJefe,idJefe=idJefe,distritos=distritos,empresas=empresas, usuario = session['usuario'], maestra=session['maestra'])

@app.route("/ActualizarJefe", methods=["POST"])
def ActualizarJefe():
    nombre = request.form["nombre"]
    apellidos = request.form["apellidos"]
    telefono = request.form["telefono"]
    telefono2 = request.form["telefono2"]
    correo = request.form["correo"]
    correo2 = request.form["correo2"]
    cargo = request.form["cargo"]
    turno = request.form["turno"]
    empresa = request.form["empresa"]
    distrito = request.form["distrito"]
    id = request.form["id"]
    controlador_jefe_inmediato.actualizar_JEFE(nombre ,apellidos,telefono,telefono2,correo ,correo2 ,cargo ,turno ,empresa ,distrito,id)

    # De cualquier modo, y si todo fue bien, redireccionar
    return redirect("/JefeInmediato")
# Iniciar el servidor
if __name__ == "__main__":
    #app.secret_key = 'ByteSquad S.A.C. - PRACTISOFT'
    app.run(host='0.0.0.0', port=8000, debug=True)
