import inspect
import os
from collections import namedtuple

class SiteInfo():
    
    """
    Класс, содержащий информацию о сайте, основанном
    на фреймворке Vitamin. Данный класс является прототипом,
    его заполненная копия помещается в корень vitamin- сайта
    в файл __info__.py и не модифицируется пользователем
    или разработчиками сайта.
    """
    
    def __init__(self, name="", description="", version="", authors=""):

        self.__name = name
        self.__description = description
        self.__version = version
        self.__authors = authors

    @property
    def name(self):
        return self.__name
    
    @property
    def description(self):
        return self.__description
    
    @property
    def version(self):
        return self.__version
    
    @property
    def authors(self):
        return self.__authors
    
    def write_to(self, path):
        
        """
        Записывает исходный текст класса SiteInfo (text) в файл __info__.py,
        расположенный по указанному пути (path)
        """
        
        if os.path.exists(path):
            respath = os.path.join(path, "__info__.py")
            with open(respath, "wt") as f:
                for name, value in dict(
                    (("name", self.name),
                    ("description", self.description),
                    ("version", self.version),
                    ("authors", self.authors))).items():
                    
                    f.write("{0} = \"\"\"{1}\"\"\"\n".format(name, value))
        else:
            raise IOError("path not exists")
    
    def read_info(self, module):
        
        """
        Импортирует модуль __info__ из текущей области видимости
        и возвращает объект SiteInfo
        """
        try:
            self.__name = getattr(module, "name")
            self.__description = getattr(module, "description")
            self.__version = getattr(module, "version")
            self.__authors = getattr(module, "authors")
        except:
            raise Exception("Wrong info file")
