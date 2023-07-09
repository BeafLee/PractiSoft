from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from pydrive2.files import FileNotUploadedError

directorio_credenciales = 'practisoftdrive/credentials_module.json'

# INICIAR SESION
def login():
    GoogleAuth.DEFAULT_SETTINGS['client_config_file'] = directorio_credenciales
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile(directorio_credenciales)
    
    if gauth.credentials is None:
        gauth.LocalWebserverAuth(port_numbers=[8092])
    elif gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()
        
    gauth.SaveCredentialsFile(directorio_credenciales)
    credenciales = GoogleDrive(gauth)
    return credenciales

def crear_archivo_texto(nombre_archivo,contenido,id_folder):
  credenciales = login()
  archivo = credenciales.CreateFile({'title': nombre_archivo,\
                                      'parents': [{"kind": "drive#fileLink",\
                                                  "id": id_folder}]})
  archivo.SetContentString(contenido)
  archivo.Upload()


def subir_archivo(ruta_archivo,id_folder):
  credenciales = login()
  archivo = credenciales.CreateFile({'parents': [{"kind": "drive#fileLink",\
                                                  "id": id_folder}]})
  archivo['title'] = ruta_archivo.split("/")[-1]
  archivo.SetContentFile(ruta_archivo)
  archivo.Upload()

def crear_carpeta(nombre_carpeta,id_folder):
  credenciales = login()
  folder = credenciales.CreateFile({'title': nombre_carpeta, 
                              'mimeType': 'application/vnd.google-apps.folder',
                              'parents': [{"kind": "drive#fileLink",\
                                                  "id": id_folder}]})
  folder.Upload()


def borrar(id_archivo):
  credenciales = login()
  archivo = credenciales.CreateFile({'id': id_archivo})
  archivo.Delete()

  # BUSCAR ARCHIVOS
def buscarID(query):
    resultado = ''
    credenciales = login()
    # Archivos con el nombre 'mooncode': title = 'mooncode'
    # Archivos que contengan 'mooncode' y 'mooncoders': title contains 'mooncode' and title contains 'mooncoders'
    # Archivos que NO contengan 'mooncode': not title contains 'mooncode'
    # Archivos que contengan 'mooncode' dentro del archivo: fullText contains 'mooncode'
    # Archivos en el basurero: trashed=true
    # Archivos que se llamen 'mooncode' y no esten en el basurero: title = 'mooncode' and trashed = false
    lista_archivos = credenciales.ListFile({'q': query}).GetList()
    for f in lista_archivos:
        resultado = f['id']
    return resultado
def buscarLink(query):
    resultado = ''
    credenciales = login()
    lista_archivos = credenciales.ListFile({'q': query}).GetList()
    for f in lista_archivos:
        resultado = f['webContentLink']
    return resultado
def buscarNombre(query):
    resultado = ''
    credenciales = login()
    lista_archivos = credenciales.ListFile({'q': query}).GetList()
    for f in lista_archivos:
        resultado = f['title']
    return resultado
