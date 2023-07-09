import pymysql

def obtener_conexion():
    return pymysql.connect(host='127.0.0.1',
                                port=3306,
                                user='root',
                                password='',
                                db='ahorasi3')

# def obtener_conexion():
#     return pymysql.connect(host='aws.connect.psdb.cloud',
#                                 user='7mlavszwrfxidtnm3vff',
#                                 password='pscale_pw_2CoADUYVCJNsl1ZgdNxP2RR6IjMs1NfjDXgKGcLYtOR',
#                                 db='practisoft_bd')

# def obtener_conexion():
#     return pymysql.connect(host='db4free.net',
#                                 port=3306,
#                                 user='bytesquad',
#                                 password='bytesquad',
#                                 db='practisoft_bd')