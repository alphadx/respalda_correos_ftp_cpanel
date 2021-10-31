import ftplib
import hashlib
from os import remove
import csv
from datetime import datetime

#conectará con el FTP
#moverá entre dominios
#moverá entre usuarios

def agregar_mapa_archivo(origen, destino, archivo = "filemap.csv"):
    with open(archivo, "a", newline='') as f:
        w = csv.DictWriter(f, fieldnames = ["origen", "destino"])
        w.writerow({"origen" : origen, "destino" : destino})


class EnlaceFTP:

    def __init__(self, parametros):
        self.__lista_dominios = parametros["dominios_respaldo"]
        self.__dominio = self.__lista_dominios[0]
        self.__archivos_transferidos = 0
        self.__archivos_eliminados = 0
        self.__host = parametros["host_ftp"]
        self.__usuario = parametros["usuario_ftp"]
        self.__pass = parametros["pass_ftp"]
        self.__ignorados = parametros["ignorados"]
        

    def __conexion(self):
        ftp = ftplib.FTP(self.__host)
        ftp.login(self.__usuario, self.__pass)
        return ftp

    @property
    def archivos_transferidos(self):
        return self.__archivos_transferidos

    @property
    def archivos_eliminados(self):
        return self.__archivos_eliminados

    @property
    def dominios(self):
        return self.__lista_dominios

    @property
    def ignorados(self):
        return self.__ignorados

    def listar_usuarios(self, dominio = None):
        ret = []
        conexion = self.__conexion()
        if dominio is None:
            conexion.cwd("/" + self.__dominio)
        else:
            conexion.cwd("/" + dominio)
        
        data = []
        conexion.retrlines('MLSD', data.append)
        #Cada linea se verá
        #['type=file', 'size=144', 'modify=20191212002854', 'UNIX.mode=0640', 'UNIX.uid=1012', 'UNIX.gid=1014', 'unique=802g60197d', ' dovecot.mailbox.log']
        for line in data:
            dir_name = line.split(";")[-1].strip()
            tipo = line.split(";")[0].split("=")[1].strip()
            #tal vez es redundante, podría bastar con "dir"
            if((dir_name != '.' or dir_name != '..') and tipo == "dir"):
                if dir_name + "@" + dominio not in self.__ignorados:
                    ret.append(dir_name)
        conexion.quit()
        return ret

    def listas_archivos_usuario(self, usuario, dominio = None, directorio = "cur"):
        ret = []
        conexion = self.__conexion()
        if dominio is None:
            dominio = self.__dominio
        conexion.cwd(f"/{dominio}/{usuario}/{directorio}")
        data = []
        conexion.retrlines('MLSD', data.append)
        for line in data:
            filename = line.split(";")[-1].strip()
            tipo = line.split(";")[0].split("=")[1].strip()
            if((filename != '.' or filename != '..') and tipo == "file"):
                ret.append(filename)
        conexion.quit()
        return ret

#eliminará todos los archivos que se encuentre a N dias del día de hoy
    def elimina_archivo_usuario_meses(self, usuario, dias = 180,dominio = None, directorio = "cur"):
        fecha_actual_timestamp = datetime.now(tz=None).timestamp()
        ret = []
        conexion = self.__conexion()
        if dominio is None:
            dominio = self.__dominio
        conexion.cwd(f"/{dominio}/{usuario}/{directorio}")
        data = []
        conexion.retrlines('MLSD', data.append)
        for line in data:
            filename = line.split(";")[-1].strip()
            tipo = line.split(";")[0].split("=")[1].strip()
            if((filename != '.' or filename != '..') and tipo == "file"):
                fecha_archivo_timestamp = int(filename.split(".")[0])
                if fecha_archivo_timestamp < (fecha_actual_timestamp - dias*24*60*60):
                    conexion.delete(filename)
                    self.__archivos_eliminados += 1
                
        conexion.quit()

    def descargar_archivos(self, usuario, dominio, directorio, lista_archivos):
        conexion = self.__conexion()
        conexion.cwd(f"/{dominio}/{usuario}/{directorio}")
        for archivo in lista_archivos:
            self.descargar_archivo(archivo, conexion)
        conexion.quit()

    def descargar_archivo(self, nombre_archivo, enlace):
        err = False
        file_size = enlace.size(nombre_archivo)
        nombre_string = f"{nombre_archivo.split('.')[0]}.{nombre_archivo.split('.')[1]}.{hashlib.md5(nombre_archivo.encode()).hexdigest()}.eml"
        file = open(nombre_string, 'wb')
        while file_size != file.tell():
            try:
                if file.tell() != 0:
                    enlace.retrbinary(f'RETR {nombre_archivo}', file.write, file.tell())
                else:
                    enlace.retrbinary(f'RETR {nombre_archivo}', file.write)
            except Exception as e:
                print(f"error en {nombre_archivo} : {e}")
                file.close()
                err = True
                remove(nombre_string)
                break
        if(not err):
            file.close()
            agregar_mapa_archivo(nombre_string, nombre_archivo)
            self.__archivos_transferidos += 1
        




