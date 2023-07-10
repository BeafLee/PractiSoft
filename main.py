import os
import jinja2
import pdfkit
import pandas as pd  #instalar
import mysql.connector #instalar
from os.path import join, dirname, realpath
from PyPDF2 import PdfMerger , PdfReader 
from flask import Flask, flash, request, jsonify, render_template, redirect, session, url_for, send_file, send_from_directory
from werkzeug.utils import secure_filename
import controladores.controlador_inicioSesion as cont_ini
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
import controladores.controlador_informe_inicial_empresa as cont_iie
import controladores.controlador_estudiante as cont_est
import controladores.controlador_usuario as cont_usu
import controladores.controlador_ubicacion as cont_ubi
import controladores.controladorGrafico as controladorGrafico
import controladores.controlador_jefe_inmediato as controlador_jefe_inmediato
import controladores.localidad as cont_localidad

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


@app.route('/login', methods=["POST"])
def login():
    usuario = request.form["usuario"]
    contra = request.form["contra"]

    usuario_log = list(cont_ini.verificarUsuario(usu=usuario, contra=contra))

    if usuario_log is None:
        return redirect(url_for("iniciarSesion", mostrar='mostrar') )
    elif usuario_log[3] == 1:
        usuario_log[4] = 'Estudiante'
        session['usuario'] = usuario_log
        session['maestra'] = "maestra_e.html"
        return redirect("/index_e")
    elif usuario_log[3] == 2:
        usuario_log[4] = 'Administrador del sistema'
        session['usuario'] = usuario_log
        session['maestra'] = "maestra_a.html"
        return redirect("/index_a")
    elif usuario_log[3] == 3:
        usuario_log[4] = 'Docente de apoyo'
        session['usuario'] = usuario_log
        session['maestra'] = "maestra_d.html"
        return redirect("/index_d")
    elif usuario_log[3] == 4:
        usuario_log[4] = 'Responsable de la practica'
        session['usuario'] = usuario_log
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
##                                  PRACTICA                                   ##
#################################################################################
###     GESTIONAR PRACTICA
@app.route("/practicas")
def practicas():
    practica = cont_prac.obtener_practica()
    return render_template("/practica/listarPractica.html", practica=practica, usuario = session['usuario'], maestra=session['maestra'])

@app.route("/practicasE")
def practicasE():
    usu=session['usuario']
    idE=usu[0]
    practica = cont_prac.obtener_practicaE(idE)
    return render_template("/practica/listarPractica.html", practica=practica, usuario = session['usuario'], maestra=session['maestra'])
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


    return redirect("/practicas")

###     MOSTRAR DETALLE DE PRACTICA
@app.route("/detalle_practica/<int:id>")
def detalle_practica(id):
    detalle = cont_dp.listar_detalle_practica(id)
    usu = session['usuario']
    return render_template("/practica/detalle_practica.html", usuario = usu, maestra=session['maestra'], detalle = detalle)

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
##                          INFORME FINAL - ESTUDIANTE                         ##
#################################################################################
separadorText = '/%/'

###     MOSTRAR FORMULARIO DE INFORME FINAL
@app.route("/afe/<int:idPractica>")
@app.route("/agregarInformeFinalEstudiante/<int:idPractica>")
def agregarInformeFinalEstudiante(idPractica):
    extraData = cont_inf_final_est.buscarOtraData_idPractica(idPractica)
    data = ["Crear", 1, extraData[0], extraData[1]]
    return render_template("/informes/final_estudiante/crudInformeFinal-Estudiante.html", usuario = session['usuario'], maestra=session['maestra'], data = data)

@app.route("/efe/<int:idPractica>")
@app.route("/editarInformeFinalEstudiante/<int:idPractica>")
def editarInformeFinalEstudiante(idPractica):
    infoData = cont_inf_final_est.buscar_id(idPractica)
    
    #Separar las conclusiones y recomendaciones en listas
    conclusiones = infoData[12].split(separadorText)
    recomendaciones = infoData[13].split(separadorText)
    print(conclusiones)
    print(recomendaciones)

    data = ["Editar", infoData[22], infoData[1], infoData[2], [infoData[15], infoData[16], infoData[17], infoData[18], infoData[19], infoData[7], infoData[8], infoData[9], infoData[10], infoData[11], conclusiones, recomendaciones, infoData[14], infoData[20], infoData[4]], infoData[3]]
    #data = ["Editar", idParactica, "RAZON 1", "DIREC 1", ["giro 1", "repre 1", cantTrabajadoer, "vision", "mision", "infra fisica", "infra tecno", "organigrama.png", "desc area de trabajo", "desc labores", ["conclu 1", "conclu 2", "conclu 3"], ["reco 1", "reco 2", "recomen 34"], "biblio", "anexos.pdf", "introduccion text"]]

    return render_template("/informes/final_estudiante/crudInformeFinal-Estudiante.html", usuario = session['usuario'], maestra=session['maestra'], data = data)

@app.route("/vfe/<int:idPractica>")
@app.route("/InformeFinalEstudiante/<int:idPractica>")
def verInformeFinalEstudiante(idPractica):
    infoData = cont_inf_final_est.buscar_id(idPractica)
    
    #Separar las conclusiones y recomendaciones en listas
    conclusiones = infoData[12].split(separadorText)
    recomendaciones = infoData[13].split(separadorText)
    
    data = ["Ver", infoData[22], infoData[1], infoData[2], [infoData[15], infoData[16], infoData[17], infoData[18], infoData[19], infoData[7], infoData[8], infoData[9], infoData[10], infoData[11], conclusiones, recomendaciones, infoData[14], infoData[20], infoData[4]], infoData[3]]
    #data = ["Ver", idParactica, "RAZON 1", "DIREC 1", ["giro 1", "repre 1", cantTrabajadoer, "vision", "mision", "infra fisica", "infra tecno", "organigrama.png", "desc area de trabajo", "desc labores", ["conclu 1", "conclu 2", "conclu 3"], ["reco 1", "reco 2", "recomen 34"], "biblio", "anexos.pdf", "introduccion text"]]
    return render_template("/informes/final_estudiante/crudInformeFinal-Estudiante.html", usuario = session['usuario'], maestra=session['maestra'], data = data)


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

    estado = "G" #Guardado
    print(conclusiones, recomendaciones)

    #Unir las conclusiones y recomendaciones en un string
    conclusiones = separadorText.join(conclusiones)
    recomendaciones = separadorText.join(recomendaciones)
    print(conclusiones)
    print(recomendaciones)
    cont_inf_final_est.insertar(estado, introduccion, infraFisica, infraTecno, urlOrganigrama, descAreaTrabajo, descLabores, conclusiones, recomendaciones, bibliografia, giro, representante, cantTrabajadores, vision, mision, urlAnexos, idPractica)
    return redirect("/agregarInformeFinalEstudiante")

@app.route("/actualizar_informeFinalEstudiante", methods=["POST"])
def actualizar_informeFinalEstudiante():
    
    idPractica = request.form["idPractica"]
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

    estado = "G" #Guardado
    print(conclusiones, recomendaciones)

    #Unir las conclusiones y recomendaciones en un string
    conclusiones = separadorText.join(conclusiones)
    recomendaciones = separadorText.join(recomendaciones)
    print(conclusiones)
    print(recomendaciones)

    cont_inf_final_est.actualizar(estado, introduccion, infraFisica, infraTecno, urlOrganigrama, descAreaTrabajo, descLabores, conclusiones, recomendaciones, bibliografia, giro, representante, cantTrabajadores, vision, mision, urlAnexos, idPractica, idInforme)
    return redirect("/agregarInformeFinalEstudiante")


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

@app.route("/prueba")
def prueba():
    data = ["Carlos Chung", "Empresa 1", "Direccion 1", 1, "texto de la introduccion", "A", "20/10/2023", "texto de la infra fisica", "texto de la infra tecnologica", "organigrama.png", "descripcion del area relaciones", "descripcion de labores", ["conclu 1", "conclu 2", "conclu 3"], ["reco 1", "reco 2", "recomen 34"], "bibliografia \nreferencia1 \nreferencia 2", "giro de la empresa", "representante legal de la empresa", 20, "vision", "mision", "anexos.pdf", 'observacion hecho por el docente', 1]

    context_caratula = {'nombre_apellido_estudiante': data[0], 'centro_practica': data[1], 'fecha_entrega': data[6]}

    return render_template("/informes/final_estudiante/caratula.html", context = context_caratula)

@app.route("/generar_informeFinalEstudiante/<int:idPractica>")
def generar_informeFinalEstudiante(idPractica):
    data = list(cont_inf_final_est.buscar_id(idPractica))

    #base = "practica/" + data[22] + "/informe/final_estudiante/"

    #data = ["Carlos Chung", "Empresa 1", "Direccion 1", 1, "texto de la introduccion", "A", "20/10/2023", "texto de la infra fisica", "texto de la infra tecnologica", "organigrama.png", "descripcion del area relaciones", "descripcion de labores", ["conclu 1", "conclu 2", "conclu 3"], ["reco 1", "reco 2", "recomen 34"], "bibliografia \nreferencia1 \nreferencia 2", "giro de la empresa", "representante legal de la empresa", 20, "vision", "mision", "anexos.pdf", 'observacion hecho por el docente', 1]

    #Separar las conclusiones y recomendaciones en listas
    data[12] = data[12].split(separadorText)
    data[13] = data[13].split(separadorText)
      
    context_caratula = {'nombre_apellido_estudiante': data[0], 'centro_practica': data[1], 'fecha_entrega': data[6]}
    context_contenido = {'introduccion': data[4],'razon_social': data[1],'direccion': data[2],'giro_institucion': data[15],'representante_legal': data[16],'cantidad_trabajadores': data[17],'vision': data[18],'mision': data[19],'infra_fisica': data[7],'infra_tecno': data[8],'organigrama': data[9],'desc_area': data[10],'desc_labores': data[11],'conclusiones': data[12],'recomendaciones': data[13],'bibliografia': data[14]}

    #Generamos la caratula para el informe
    output_text_caratula = render_template("/informes/final_estudiante/caratula.html", context = context_caratula)
    output_pdf_caratula = 'static/practica/' + str(idPractica) + '/informe/final_estudiante/caratula.pdf'
    pdfkit.from_string(output_text_caratula, output_pdf_caratula, configuration=config, options={"enable-local-file-access": ""})

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
##                                  SEMESTRE                                   ##
#################################################################################

###     MOSTRAR SEMESTRES
@app.route("/semestres")
def semestres():
    semestres = cont_sem.obtener_semestre()
    usu = session['usuario']
    #print("Datos:",usu)
    return render_template("/semestre/listarSemestre.html", usuario = usu, maestra=session['maestra'], semestres = semestres)


###     AGREGAR SEMESTRE
@app.route("/agregar_semestre")
def agregar_semestre():
    return render_template("/semestre/nuevoSemestre.html", usuario = session['usuario'], maestra=session['maestra'])

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

    return render_template("/semestre/editarSemestre.html", usuario = session['usuario'], maestra=session['maestra'], semestre=semestre, opt=opt)

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
    facultades = cont_fac.obtener_facultad()
    usu = session['usuario']
    #print("Datos:",usu)
    return render_template("/facultad/listarFacultad.html", usuario = usu, maestra=session['maestra'], facultades = facultades)





###     AGREGAR FACULTAD
@app.route("/agregar_facultad")
def agregar_facultad():
    return render_template("/facultad/nuevaFacultad.html" , usuario = session['usuario'], maestra=session['maestra'])

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

    return render_template("/facultad/editarFacultad.html", usuario = session['usuario'], maestra=session['maestra'], facultad=facultad, opt=opt)

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
    cont_fac.eliminar_facultad(id)
    return redirect("/facultades")



#################################################################################
##                                  ESCUELA                                    ##
#################################################################################


@app.route("/escuelas")
def escuelas():
    escuelas = cont_esc.obtener_escuela()
    usu = session['usuario']
    #print("Datos:",usu)
    return render_template("/escuela/listarEscuela.html", usuario = usu, maestra=session['maestra'], escuelas = escuelas)




###     BUSCAR ESCUELA
@app.route("/escuelas", methods=["POST"])
def escuelas_nombre():
    nombre = request.form["nombre"]
    escuelas = cont_esc.buscar_escuela(nombre)
    return render_template("/escuela/listarEscuela.html", usuario = session['usuario'], maestra=session['maestra'], escuelas = escuelas, editEscuela = None)


###     AGREGAR ESCUELA
@app.route("/agregar_escuela")
def agregar_escuela():
    facultades = cont_esc.listarFacultades()
    return render_template("/escuela/nuevaEscuela.html", usuario = session['usuario'], maestra=session['maestra'],facultades=facultades)

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

    return render_template("/escuela/editarEscuela.html", usuario = session['usuario'], maestra=session['maestra'], escuela=escuela,facultades=facultades, opt=opt)

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
    cont_esc.eliminar_escuela(id)
    return redirect("/escuelas")


#################################################################################
##                                ESTUDIANTE                                   ##
#################################################################################

###     MOSTRAR ESTUDIANTES
@app.route("/estudiantes")
def estudiantes():
    estudiantes = cont_est.obtener_estudiante()
    usu = session['usuario']
    #print("Datos:",usu)
    return render_template("/estudiante/listarEstudiante.html", usuario = usu, maestra=session['maestra'], estudiantes = estudiantes,error_statement="")



###     DAR DE BAJA ESCUELA
@app.route("/darbaja_estudiante/<int:id>")
def darbaja_estudiante(id):
    cont_est.dar_baja(id)
    return redirect("/estudiantes")

###     DAR DE ALTA ESCUELA
@app.route("/daralta_estudiante/<int:id>")
def daralta_estudiante(id):
    cont_est.dar_alta(id)
    return redirect("/estudiantes")



#################################################################################
##                                   EMPRESA                                   ##
#################################################################################

###     MOSTRAR EMPRESAS
@app.route("/empresas")
def empresas():
    empresas = cont_emp.obtener_empresa()
    usu = session['usuario']
    return render_template("/empresa/listarEmpresa.html", usuario = usu, maestra=session['maestra'], empresas = empresas)



###     BUSCAR EMPRESA
@app.route("/empresas", methods=["POST"])
def empresas_nombre():
    razonSocial = request.form["razonSocial"]
    empresas = cont_emp.buscar_empresa(razonSocial)
    return render_template("/empresa/ListaEmpresa.html", empresas = empresas, maestra=session['maestra'], editEmpresa = None)


###     AGREGAR EMPRESA
@app.route("/agregar_empresa")
def agregar_empresa():
    paises = cont_emp.listar_pais()
    dep = cont_emp.listar_departamento()
    return render_template("/empresa/nuevaEmpresa.html", paises = paises, dep = dep,  usuario = session['usuario'], maestra=session['maestra'])

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

    if pais == '1':
        cont_emp.insertar_empresa_nacional(razonSocial,direccion,ruc,telefono,telefono2,correo,distrito)
    else: cont_emp.insertar_empresa_internacional(razonSocial,direccion,ruc,telefono,telefono2,correo,pais)
    return redirect("/empresas")


###     EDITAR EMPRESA
@app.route("/editar_empresa/<int:id>")
def editar_empresa(id):
    empresa = cont_emp.buscar_empresa_id(id)
    paises = cont_emp.listar_pais()
    dep = cont_emp.listar_departamento()
    if (empresa[8] == None):
        info = cont_emp.empresa_nacional(empresa[7])
        prov = cont_emp.listar_provincia(info[1])
        dis = cont_emp.listar_distrito(info[2])
        bandera = True
        disable = ''
    else: 
        info = cont_emp.nombrePais(empresa[8])
        bandera = False
        disable = 'disabled'
    return render_template("/empresa/editarEmpresa.html", empresa=empresa, paises=paises, dep = dep, info = info, prov = prov, dis = dis, bandera = bandera, disable = disable ,  usuario = session['usuario'], maestra=session['maestra'])

@app.route("/ver_empresa/<int:id>")
def ver_empresa(id):
    empresa = cont_emp.buscar_empresa_id(id)
    paises = cont_emp.listar_pais()
    dep = cont_emp.listar_departamento()
    if (empresa[8] == None):
        info = cont_emp.empresa_nacional(empresa[7])
    else: 
        info = cont_emp.nombrePais(empresa[8])
    return render_template("/empresa/verEmpresa.html", empresa=empresa, paises=paises, dep = dep, info = info ,  usuario = session['usuario'], maestra=session['maestra'])

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
    distrito = 0
    if pais == '1':
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
        cont_iie.insertar_informe_inicial_empresa("P",urlAcept,fechaEntrega,labores,urlFirma,urlSello,idPractica)
    if 'btnEnviar' in request.form:
        cont_iie.insertar_informe_inicial_empresa("E",urlAcept,fechaEntrega,labores,urlFirma,urlSello,idPractica)
    return redirect("/detalle_practica/"+idPractica)

@app.route("/editar_iie/<int:id>")
def editar_iie(id):
    info = cont_iie.infoPlantilla(id)
    iie = cont_iie.buscar_informe_inicial_empresa_id(id)
    acep = iie[1]
    labores = cont_iie.desconcat_labores(iie[3])
    print(iie[1])
    if len(labores) == 1:
        labores[0] = iie[3]
        bandera = False
    else: 
        bandera = True
    return render_template("/informe_inicial_empresa/editarInforme.html", iie=iie, labores=labores, acep = acep,info = info, bandera = bandera,  usuario = session['usuario'], maestra=session['maestra'])

@app.route("/ver_iie/<int:id>")
def ver_iie(id):
    info = cont_iie.infoPlantilla(id)
    iie = cont_iie.buscar_informe_inicial_empresa_id(id)
    acep = iie[1]
    labores = cont_iie.desconcat_labores(iie[3])
    print(iie[1])
    if len(labores) == 1:
        labores[0] = iie[3]
        bandera = False
    else: 
        bandera = True
    return render_template("/informe_inicial_empresa/verInforme.html", iie=iie, labores=labores, acep = acep,info = info, bandera = bandera,  usuario = session['usuario'], maestra=session['maestra'])

@app.route("/actualizar_iie", methods=["POST"])
def actualizar_iie():
    idInforme = request.form["idInforme"]
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
        cont_iie.actualizar_informe_inicial_empresa("P",urlAcept,fechaEntrega,labores,urlFirma,urlSello,idInforme)
    if 'btnEnviar' in request.form:
        cont_iie.actualizar_informe_inicial_empresa("E",urlAcept,fechaEntrega,labores,urlFirma,urlSello,idInforme)
    return redirect("/detalle_practica/"+idPractica)

@app.route("/generar_iie/<int:id>")
def generar_iie(id):

    infoPlantilla = cont_iie.infoPlantilla(id)
    infoInforme = cont_iie.buscar_informe_inicial_empresa_id(id)
    labores = []
    labores = cont_iie.desconcat_labores(infoInforme[3])
    
    html = render_template('/informe_inicial_empresa/plantilla.html', infoP = infoPlantilla, infoI = infoInforme, lab = labores)
    pdfkit.from_string(html, 'static/practica/'+str(id)+'/informe/inicial_empresa/informe_inicial_empresa.pdf', configuration=config)
    return send_file('static/practica/'+str(id)+'/informe/inicial_empresa/informe_inicial_empresa.pdf', as_attachment=True)


#################################################################################
##                                  REPORTE                                   ##
#################################################################################

@app.route("/reporte1")
def reportes1():
    reportes1 = cont_rep.obtener_reporte_1()
    reportes2 = cont_rep.obtener_reporte_2()
    return render_template("/reportes/listarReporte1.html", usuario = session['usuario'], maestra=session['maestra'],reportes1 = reportes1,reportes2 = reportes2)

#################################################################################
##                                DISTRITO                                    ##
#################################################################################

###     MOSTRAR DISTRITO
@app.route("/distrito")
def distrito():
    if 'usuario' in session and session['usuario'][4] == 'Docente de apoyo':
        ubicaciones = cont_ubi.listar_distritos()
        return render_template("/ubicacion/distrito/listarDistritos.html", usuario = session['usuario'], maestra=session['maestra'], ubicaciones = ubicaciones)
    else:
        return redirect('/')


###     AGREGAR DISTRITO
@app.route("/agregar_distrito")
def agregar_distrito():
    datos_paises = cont_ubi.datos_paises()
    return render_template("/ubicacion/distrito/nuevoDistrito.html", usuario = session['usuario'], maestra=session['maestra'], paises = datos_paises)

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
    datos_paises = cont_ubi.datos_paises()
    data = cont_ubi.buscar_distrito(id)

    return render_template("/ubicacion/distrito/editarDistrito.html", usuario = session['usuario'], maestra=session['maestra'], paises = datos_paises, data=data)

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
    return render_template("/Jefe_Inmediato/editarJefe.html", jefes=jefes,UsuarioJefe=usuarioJefe,distritos=distritos,empresas=empresas, usuario = session['usuario'], maestra=session['maestra'])

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
    usuario = request.form["usuario"]
    contraseña = request.form["contraseña"]
    distrito = request.form["distrito"]
    controlador_jefe_inmediato.actualizar_JEFE(nombre ,apellidos,telefono,telefono2,correo ,correo2 ,cargo ,turno ,empresa ,usuario,contraseña,distrito)

    # De cualquier modo, y si todo fue bien, redireccionar
    return redirect("/JefeInmediato")
# Iniciar el servidor
if __name__ == "__main__":
    #app.secret_key = 'ByteSquad S.A.C. - PRACTISOFT'
    app.run(host='0.0.0.0', port=8000, debug=True)
