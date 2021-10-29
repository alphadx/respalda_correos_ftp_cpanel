import ftplib

#conectará con el FTP
#moverá entre dominios
#moverá entre usuarios
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

    def listas_archivos_usuario(self, usuario, dominio = None, directorios = ["cur", "new"]):
        ret = []
        conexion = self.__conexion()
        if dominio is None:
            dominio = self.__dominio
        for directorio in directorios:
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
