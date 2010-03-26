
from functools import partial
import os
import logging

logger = logging.getLogger("static")

def conversion(function):    
    return partial(Conversion, function) 

class Conversion():
    
    """
    Conversion - объект- преобразователь. Используется
    для получения файлов из хранилища в необходимом
    пользователю формате. Преобразователи могут объединяться
    в цепочки при помощи операции суммирования, создавая новый
    преобразователь. Действие нового преобразователя будет
    заключаться в вызове цепочки преобразователей с передачей
    результатов выполнения предъидущего преобразователя
    следующему.    
    
    Первый преобразователь в цепочке принимает три аргумента:
        name - имя файла
        full_path - полный путь до файла в файловой системе
        fakepath - фальшивый путь, указанный в файле конфигурации
        
    Преобразователь переопределяет функцию __getattribute__
    для обеспечения прозрачного доступа к файлам как к
    полям класса (см. storage)
    """
    
    def __init__(self, conversion):  
        
        self._storage = None  
        self.go = None
        self.__assign(conversion)  
        
    #===========================================================================
    # Интрфейс комбинатора
    #===========================================================================
        
    def __add__(self, right):
        
        assert isinstance(right, Conversion)
        
        @Conversion
        def __go(name, full_path, fakepath=None):
            res = self.go(name, full_path, fakepath)
            return right.go(res)
        
        return __go
              
        
    def __assign(self, callable):  
             
        function = getattr(callable, "go", callable)
        storage = getattr(callable, "_storage", None)
        
        setattr(self, "go", function)
        if storage:
            self.set_storage(storage)
        
    def set_storage(self, storage):          
        self._storage = storage
        
    def __getattribute__(self, name):
        
        getter = object.__getattribute__
        storage = getter(self, "_storage")
        go = getter(self, "go")
        
        if storage:
            print(storage._name)
            print(storage.files)
        
        if storage and (name in storage.files):
            * names, ext = name.split("_")
            filename = "".join(names) + "." + ext
            return go(filename, self._storage.files[name], self._storage._fakepath)
        else:
            return getter(self, name)
        
    def __call__(self, name):        
        return self.__getattribute__(name.replace(".", "_"))

def _path(name, full, fake):
    
    pos_of_point = name.rfind(".")
    pos_of_space = name.rfind("_")
    
    if pos_of_point < pos_of_space:
        name = name[:pos_of_space] + "." + name[pos_of_space + 1:]

    return os.path.join(fake, name) if fake else full

#===============================================================================
# Стандартные преобразователи
#===============================================================================

@conversion
def css_style(name, full_path, fakepath=None):    
    path = _path(name, full_path, fakepath)
    return """<link href="{0}" rel="stylesheet" type="text/css"/>""".format(path)

@conversion
def jscript(name, full_path, fakepath=None):
    path = _path(name, full_path, fakepath)
    return """<script src="{0}" type="text/javascript">//</script>""".format(path)

@conversion
def file_text(name, full_path, fakepath=None):
    path = _path(name, full_path, fakepath)
    with open(full_path, "rt") as f:
        return f.read()

@conversion
def file_bin(name, full_path, fakepath=None):
    with open(full_path, "rb") as f:
        return f.read()

@conversion
def path_returner(name, full_path, fakepath=None):
    return _path(name, full_path, fakepath)

@conversion
def image(name, full_path, fakepath):
    path = _path(name, full_path, fakepath)
    return "<img src='{0}' alt='{0}'></img>".format(path)
