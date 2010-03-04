from helpers.lazyimport import smartimport
from helpers.dictmapper import MappedDict
from collections import UserList

class Null:
    pass

config = None
LAZY_IMPORT_PREFIX = "lazy://"

def prepare(module):
    global config
    config = module
    
def lazy_load_from_data(self, index, item):
    if isinstance(item, str) and item.startswith(LAZY_IMPORT_PREFIX):
        self.data[index] = smartimport(item[len(LAZY_IMPORT_PREFIX):])
        return self.data[index]
    else: return item

#===============================================================================
# Exceptions
#===============================================================================
class ConfigNoSection(Exception):
    
    """
    Исключение, возникающее когда в модуле конфигурации
    нет нужной секции. 
    """
    
    def __init__(self, section):
        self.msg = "No section '{0}' in config module".format(section)
        
    def __str__(self):
        return self.msg  
        
class ConfigNoParameter(Exception):
    
    """
    Исключение, возникающее когда в секции конфигурации
    нет нужного параметра. 
    """    
    
    def __init__(self, section, parameter):
        self.msg = "Missed required configuration parameter '{1}' in section '{0}'".format(
            section, parameter)
    
    def __str__(self):
        return self.msg
#===============================================================================
#===============================================================================

class LazyList(UserList):
    
    """
    Список, поддерживающий ленивый импорт. При попытке обращения к
    элементам списка элемент с нужным индексом будет проверен на
    необходимость ленивого импорта, и если эта необходимость есть,
    производит его и уже после этого возвращает значение элемента.
    """
    
    def __init__(self, lst=[]):
        UserList.__init__(self, lst)
        
    def __getitem__(self, index):
        item = self.data[index]
        return lazy_load_from_data(self, index, item)
        
    def __contains__(self, obj):
        for x in self: pass #import all
        return obj in self.data

class Section(MappedDict):
    
    """
    Секция - словарь, поддерживающий lazy import. 
    См. описание LazyList
    """
            
    def __getitem__(self, key):
        if key in self.keys():
            item = self.data[key]
            return lazy_load_from_data(self, key, item)
        else: raise KeyError(key)
        
    def reconfigure(self, name, value):
        for item in self.keys():
            if item.upper() == name.upper(): 
                self[item] = value
                return True
        return False

        
class Parameter():
    
    """
    Используется как указатель на то, что поле класса
    должно быть загружено из соответствующей секции модуля 
    конфигурации.
    Использование:
    
        class cls():
            
            def __init__(self):
                self.smth = Parameter()
                self.tweak()
                
    Дополнительные параметры:
                
        default - стандартное значение, которое
    будет использовано в том случае, если указанная опция не прописана
    в секции модуля конфигурации
    
        section - замена стандартной секции конфигурации, указанной
    при инициализации конфигурируемого класса
                
    """
    
    def __init__(self, default=Null(), section=None):
        self.name = None
        self.default = default
        self.section = section     

class Tweak():
    
    """
    Класс- конфигуратор. Классы, унаследованные от класса-
    конфигуратора будут получать настройки для своих полей 
    типа Parameter из определенной при вызове __init__ секции
    Section модуля конфигураиции (или другой секции, указанной
    явно в конструкторе Parameter(..)).
    
        class Simple(Tweak):
            
            def __init__(self):
                Tweak.__init__(self, "section") #задаем "section"
                                                #стандартной секцией
                self.param1 = Parameter()
                self.param2 = Parameter(default=...)
                self.param3 = Patameter(section="..")
                
                self.tweak()
                #или self.tweak(site_config = ...)
    
    После выполнения self.tweak переменным self.param* будут присвоены 
    соответствуюшие значения, определенные под именами param* в указанных
    секциях конфигурационного модуля    
    """

    def __init__(self, section):
        
        self.__params = []
        self.__section = section
       
    def load_section(self, config_module, section):
        
        """Загрузка словаря- секции Section из модуля конфигурации"""
              
        if section in dir(config_module):     
            section_dict = getattr(config_module, section);
            assert isinstance(section_dict, Section)
            return section_dict
        
    def combine_sections(self, section):
        
        """
        Комбинирование параметров из нескольких секций в одну секцию.
        Параметры выбираются из указанной секции стандартной конфигурации
        и аналогичной секции в модуле конфигурации сайта. Если в секциях
        существуют одинаковые параметры с разрыми значениями, то приоритет
        получают значения из модуля конфигурации сайта.
        """
        
        assert section 
        
        default_section_dict = self.load_section(config, section)
        site_section_dict = self.load_section(self.site_config, section)
        
        section = None
        
        #выбор секции
        if site_section_dict and default_section_dict:
            #комбинируем обе секции
            section = default_section_dict.copy()
            section.update(site_section_dict)
        elif site_section_dict:
            #секция существуюет только в конфигурации сайта
            section = site_section_dict
        elif default_section_dict:
            #секция существует только в стандартной конфигурации
            section = default_section_dict
        else:
            raise ConfigNoSection(self.__section)
        
        return section
        
        
    def tweak(self, site_config=None):
        
        """
        Непосредственно осуществление конфигурирования полей Parameter
        объекта. Конфигурация читается из двух источников: из стандартной
        конфигурации фреймворка и из конфигурации сайта, причем приоритет
        отдается последней.
        """
        
        self.dir_default_config = (x for x in dir(config) if not x.startswith("_"))
        self.dir_site_config = (x for x in dir(site_config) if not x.startswith("_")) 
        self.site_config = site_config
        
        section = self.combine_sections(self.__section)
        
        params = {name:value for name, value in self.__dict__.items() 
            if isinstance(value, Parameter)}
        
        for name, param in params.items():
            param.name = name
            current_section = section          
            if param.section:      
                current_section = self.combine_sections(param.section)
            if param.name in current_section:
                setattr(self, param.name, current_section[param.name])
            else:
                if isinstance(param.default, Null):
                    raise ConfigNoParameter(current_section, param.name)
                else:
                    setattr(self, param.name, param.default)
        
        #чистим за собой класс
        del self.dir_default_config
        del self.site_config
        del self.dir_site_config
        



