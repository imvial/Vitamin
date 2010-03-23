import os
from vitamin.config import Parameter, tweak, Section

import logging
from inspect import getargs
from vitamin.modules.static.conversions import Conversion, file_text, file_bin, \
    path_returner
logger = logging.getLogger("storage")

class Storage():
    
    """
    Файловое хранилище. 
    Данный класс отвечает за обработку файлов определенных
    заранее расширений extensions, расположенных в папке path.
    У каждое хранилище имеет имя, по кторому оно будет доступно
    их шаблонной системы, и обработчик html_conversion, который
    создает обвязку имени файла:
    
        Пример:
        
        html_conversion('style.css') -> 
            <link href="style.css" rel="stylesheet"/>
   
    Обращение к аттрибутам класса:
    
        Создан экземпляр класса Storage и менем styles,
        содержащий файл style.css. При обращении styles.style
        в хранилище производится поиск файла style и если он будет
        обнаружен - вызывается html_conversion и возвращается
        результат преобразования (см. выше)
        
        style.html.styles_css    |
        style.html("styles.css") | -> 
            <link href="/path/to/style/style.css" rel="stylesheet"/>
            
        Получение содержания файла:
        
            Получить содержание файла можно несколькими способами:
            
            1. Получение текста файла
                style.text.styles_css    |
                style.text("styles.css") | -> 'body{margin:0 auto;};'
                
            2. Получение потока
                style.stream.styles_css    |
                style.stream("styles.css") | -> bytes
                
            3. Регистрация альтернативных обработчиков
                (для получения потока gzip, например)
                    TODO
                    
    """
    
    #===============================================================================
    # Добавление и удаление преобразователей файлов
    #===============================================================================
       
    def __add_conversion(self, name, conversion):
        
        """
        Получает на вход два параметра 
            @name - имя преобразователя
            @conversion - класс преобразователя
            
        Процедура создает экземпляр преобразователя @conversion
        и добавляет его к полям класса хранилища, для которого 
        метод был вызван, под указанным именем @name и добавляет
        @name в список зарегистрированных преобразователей.      
        """
        
        conv = conversion()        
        assert isinstance(conv, Conversion)
        
        conv.set_storage(self)
        
        setattr(self, name, conv)
        self.conversions.append(name)
        
        logger.debug("'%s' conversion '%s' ", self._name, name)
        
    def __del_conversion(self, name):
        
        """
        Получает на вход два параметра 
            @name - имя преобразователя
            
        Процедура проверяет наличие @name в списке зарегистрированных
        преобразователей и удаляет преобразователь при его наличии.
        """
        
        assert name in self.conversions

        delattr(self, name)
        del self.conversions[self.conversions.index(name)]
        
    #===========================================================================
    # Инициализация хранилища
    #===========================================================================
    
    def __init__(self, st_name, path=None, extensions=[], conversions=None):
        
        """
        @st_name - имя хранилища в системе (используется в основном
        для вывода отладочных сообщений в лог)
        
        @path - путь в файловой системе, по которому необходимо производить
        поиск файлов хранилища
        
        @extensions - список расширений файлов, которые обрабатывает данное
        хранилище в формате .xyz
        
        @conversions - словарь преобразователей в формате {name:conversion_class}
        """
                
        assert isinstance(st_name, str)
        assert isinstance(path, str)
        assert extensions
        
        self.conversions = []
        self.files = {}
        self.default = None         
        self._name = st_name
        self._path = path
        self._extensions = extensions
        
        #=======================================================================
        # добавление стандартных преобразователей
        #=======================================================================        
        self.__add_conversion("text", file_text)
        self.__add_conversion("stream", file_bin)
        
        #=======================================================================
        # добавление пользовательских преобразоваетелей
        #=======================================================================        
        if conversions:
            assert isinstance(conversions, Section)
            conversions.preload()            
            for name, conversion in conversions.items():
                self.__add_conversion(name, conversion)
        
        #=======================================================================
        # добвление default- преобразователя
        #=======================================================================        
        if not "default" in self.conversions:
            logger.info(" %s's default conversion added automaticly", self._name)
            self.__add_conversion("default", path_returner)
            
        #=======================================================================
        # сканирование файлов в каталоге path
        #=======================================================================
        if path and os.path.exists(path):
            
            self.files = {os.path.splitext(x)[0] + "_" 
                + os.path.splitext(x)[1][1:]:os.path.join(path, x) 
                for x in os.listdir(path) if os.path.splitext(x)[1] in extensions}         
            
            logger.info("files in '%s': %s", self._name ,
                ", ".join([os.path.split(x)[1] for x in self.files]))
            
    def __getattribute__(self, name):
        
        #=======================================================================
        # получение стандартных аттрибутов
        #=======================================================================        
        getter = object.__getattribute__        
        conversions = getter(self, "conversions")
        files = getter(self, "files")
        default = getter(self, "default")
                
        if (not name in conversions) and (name in files):
            return default.go(name, self.files[name])
        else:
            return getter(self, name)
        
    
class StorageSystem(object):
       
    def __init__(self, site_config):
        
        self.storages = {}
        
        self.FOLDERS = Parameter()
        self.FOLDER_EXTENSIONS = Parameter()
        self.DEFAULT_CONVERSIONS = Parameter() 
        tweak(self, "Site", site_config)
        
        assert isinstance(self.FOLDERS, Section)
        assert isinstance(self.FOLDER_EXTENSIONS, (dict, Section))
        
        self.FOLDERS.preload()       

        for name, path in self.FOLDERS.items():
            if name in self.FOLDER_EXTENSIONS:
                self.add_storage(Storage(name, path, self.FOLDER_EXTENSIONS[name],
                    conversions=(self.DEFAULT_CONVERSIONS[name] if name in self.DEFAULT_CONVERSIONS else None)))
            else:
                raise Exception("Укажите расширения файлов для хранилища '{0}'".format(name))
            
    def __getattribute__(self, name):
        
        default = object.__getattribute__
        
        storages = default(self, "storages")
        if name in storages:
            logger.debug("'%s' storage requested", name)
            return storages[name]
        else:
            return default(self, name)

    def add_storage(self, storage):
        
        assert storage
        self.storages[storage._name] = storage
        
    def del_storage(self, storage=None, name=None):
        
        assert storage.name or name in self.categories
        del self.storages[storage.name or name]
    
