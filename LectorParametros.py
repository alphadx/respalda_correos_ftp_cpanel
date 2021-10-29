from json import loads

class LectorParametros:
    def __init__(self, archivo = '.env'):
        with open(archivo, "r") as f:
            self.__parametros = loads(f.read())
            self.__dict__ = self.__parametros
    
    #esto es para verlos en atributo
    @property
    def parametros(self):
        return self.__parametros

    def __getitem__(self, key):
        return self.__dict__[key]

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __delitem__(self, key):
        del self.__dict__[key]

    def __contains__(self, key):
        return key in self.__dict__

    def __len__(self):
        return len(self.__dict__)

    def __repr__(self):
        return repr(self.__dict__)

    
