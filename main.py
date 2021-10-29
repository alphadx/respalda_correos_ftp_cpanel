#La gracia, es que el remoto siempre será más pequeño que el local.
#Tal vez la rutina que va separando los archivos por año, podría ser otra rutina aparte
def init():
    #obtengo parámetros
    #conecto ftp
    #por cada directorio (en caso de que no exista en local, lo creo)
        #obtengo la lista de subdirectorios (usuarios)
        #por cada usuario
            #obtengo la lista de sus archivos en local y lo almaceno en una tabla de hash
            #obtengo la lista de sus archivos remoto
            #por cada archivo remoto
                #verifico si el archivo existe en la tabla de hash
                    #si existe lo ignoro
                    #si no existe lo descargo
    

        
            #obtengo la lista de sus archivos remoto que tengan una fecha de creación es anterior a la <FECHA_ACTUAL - CANTIDAD_DE_MESES>
            #elimino el archivo

    pass



if __name__ == "__main__":
    init()