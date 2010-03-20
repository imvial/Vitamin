import os
from vitamin.config import Parameter, tweak, Section

import logging
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
        
        style.html.styles.css    |
        style.html("styles.css") | -> 
            <link href="/path/to/style/style.css" rel="stylesheet"/>
            
        Получение содержания файла:
        
            Получить содержание файла можно несколькими способами:
            
            1. Получение текста файла
                style.text.styles.css    |
                style.text("styles.css") | -> 'body{margin:0 auto;};'
                
            2. Получение потока
                style.stream.styles.css    |
                style.stream("styles.css") | -> bytes
                
            3. Регистрация альтернативных обработчиков
                (для получения потока gzip, например)
                    TODO
                    
    """
    
    #default
    html_conversion = lambda path: path
    
    def set_conversion(self, conversion):
        
        assert hasattr(conversion, "__call__")
        self.html_conversion = conversion
    
    def __init__(self, name, path=None, extensions=[], conversion=None):
        
        self.files = {}
        
        assert isinstance(name, str)
        assert isinstance(path, str)
        assert extensions
        
        self.name = name
        self.path = path
        self.extensions = extensions
        
        if conversion:
            self.html_conversion = conversion
        
        logger.debug("'%s' conversion %s ", self.name, self.html_conversion("test"))
        
        if path and os.path.exists(path):
            
            self.files = {os.path.splitext(x)[0]:os.path.join(path, x) for x in os.listdir(path)
                          if os.path.splitext(x)[1] in extensions}         
            
            logger.info("files in '%s': %s", self.name ,
                ", ".join([os.path.split(x)[1] for x in self.files]))
            
    def __getattribute__(self, name):
        
        default = object.__getattribute__
        files = default(self, "files")
        if name in files:
            return self.html_conversion(files[name])
        else:
            return default(self, name)
    
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
                    conversion=(self.DEFAULT_CONVERSIONS[name] if name in self.DEFAULT_CONVERSIONS else None)))
            else:
                raise Exception("Укажите расширения файлов для хранилища '{0}'".format(name))
            
    def __getattribute__(self, name):
        
        default = object.__getattribute__
        
        storages = default(self, "storages")
        if name in storages:
            return storages[name]
        else:
            return default(self, name)

    def add_storage(self, storage):
        
        assert storage
        self.storages[storage.name] = storage
        
    def del_storage(self, storage=None, name=None):
        
        assert storage.name or name in self.categories
        del self.storages[storage.name or name]
    
