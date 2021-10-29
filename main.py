from os import path, mkdir, chdir, listdir
import hashlib
import EnlaceFTP, LectorParametros

#La gracia, es que el tamaño de los archivos en remoto siempre será más pequeño que el local.
#Tal vez la rutina que va separando los archivos por año, podría ser otra rutina aparte

def obtener_hash_archivos_locales(archivos):
    ret = []
    for archivo in archivos:
        hashed = hashlib.md5(archivo.encode())

        ret.append(hashed.hexdigest())
    return ret

def verificar_directorio(directorio):
    if(path.exists(directorio)):
        return True
    else:
        try:
            mkdir(directorio)
            return True
        except Exception as e:
            return False




def init():
    #obtengo parámetros
    parametros = LectorParametros.LectorParametros()
    #conecto ftp
    enlace = EnlaceFTP.EnlaceFTP(parametros)
    #por cada directorio (dominio)
    verificar_directorio(parametros["directorio_respaldo"])
    chdir(parametros["directorio_respaldo"])

    for dominio in enlace.dominios:
        #me muevo al directorio del dominio
        verificar_directorio(dominio)
        chdir(dominio)
        #obtengo la lista de subdirectorios (usuarios)
        usuarios_remoto = enlace.listar_usuarios(dominio)
        usuarios_local = listdir()
        #por cada usuario en remoto
        for usuario_remoto in usuarios_remoto:
            #si un usuario no existe en local, entonces lo creo
            verificar_directorio(usuario_remoto)
            #me muevo al directorio del usuario
            chdir(usuario_remoto)
            #obtengo la lista de sus archivos en local y lo almaceno en una tabla de hash
            archivos_locales = [f for f in listdir('.') if path.isfile(f)]
            archivos_locales_hash = obtener_hash_archivos_locales(archivos_locales)
            print(archivos_locales_hash)
            #obtengo la lista de sus archivos remoto
                #Deberían ser aquellos archivos que están tanto en el subdirectorio "cur" y "new"
            #por cada archivo remoto
                #verifico si el archivo existe en la tabla de hash
                    #si existe lo ignoro
                    #si no existe lo descargo
            #me devuelvo del directorio del usuario
            chdir("..")
        #me devuelvo del directorio del dominio
        chdir("..")
    

        
            #obtengo la lista de sus archivos remoto que tengan una fecha de creación es anterior a la <FECHA_ACTUAL - CANTIDAD_DE_MESES>
            #elimino el archivo



if __name__ == "__main__":
    init()