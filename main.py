from os import path, mkdir, chdir, listdir
import hashlib
import EnlaceFTP, LectorParametros

#La gracia, es que el tamaño de los archivos en remoto siempre será más pequeño que el local.
#Tal vez la rutina que va separando los archivos por año, podría ser otra rutina aparte

def obtener_hash_archivos_locales(ignorar = ['filemap.csv']):
    ret = []
    for f in listdir('.'):
        if path.isfile(f) and f not in ignorar:
            ret.append(f.split('.')[2])
    return ret


def obtenerMD5(string):
    hashed = hashlib.md5(string.encode())
    return hashed.hexdigest()

def verificar_directorio(directorio):
    if(path.exists(directorio)):
        return True
    else:
        try:
            mkdir(directorio)
            return True
        except Exception as e:
            return False

def obtener_archivos_faltantes(lista_archivos_hash, lista_archivos):
    ret = []
    for archivo in lista_archivos:
        if obtenerMD5(archivo) not in lista_archivos_hash:
            ret.append(archivo)
    return ret



class main:
    def __init__(self):
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
                #tuve problemas al querer guardar los archivos con el mismo nombre original, así que deberé crear una lista de archivos redundante
                #y el nombre del archivo que sea un hash
                #porque si quisiera devolverlo al servidor, este debería tener el nombre original
                #obtengo la lista de sus archivos en local y lo almaceno en una tabla de hash
                #Formato de archivos
                    #DATE.ID.directory.HASH.eml - deseo quedarme sólo con el HASH
                    #directory será la 1era letra de Cur, New o Sent
                #archivos_locales_hash = [f.split('.')[2] for f in listdir('.') if path.isfile(f)]
                archivos_locales_hash = obtener_hash_archivos_locales()
                #Deberían ser aquellos archivos que están tanto en el subdirectorio "cur" y "new"
                for directorio in ["cur", "new", ".Sent/cur"]:
                    print(usuario_remoto, dominio, directorio)
                    archivos_descargar = obtener_archivos_faltantes(archivos_locales_hash, enlace.listas_archivos_usuario(usuario_remoto, dominio, directorio))
                    #verifico si el archivo existe en la tabla de hash
                        #si existe lo ignoro
                        #si no existe lo descargo
                    enlace.descargar_archivos(usuario_remoto, dominio, directorio, archivos_descargar)
                    if parametros["eliminar_archivo"]:
                        enlace.elimina_archivo_usuario_meses(usuario_remoto, int(parametros["meses_mantener"])*30, dominio, directorio)
                    print("transferidos:", enlace.archivos_transferidos)
                    print("eliminados:", enlace.archivos_eliminados)

                #me devuelvo del directorio del usuario
                chdir("..")
            #me devuelvo del directorio del dominio
            chdir("..")
        

            
                #obtengo la lista de sus archivos remoto que tengan una fecha de creación es anterior a la <FECHA_ACTUAL - CANTIDAD_DE_MESES>
                #elimino el archivo



if __name__ == "__main__":
    main()
