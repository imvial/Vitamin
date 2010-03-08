from vitamin.modules.tpl import Templates
from vitamin.siteinfo import SiteInfo

class ModelsCollection():
    pass

class ViewsCollection():
    pass

class LogicCollection():
    pass

class Site():
    
    """
    Модуль, являющийся фасадом нашего сайта, связывает между собой и
    хранит все необходимые для его работы компоненты:
        - модели из каталога /models
        - шаблоны из каталога /templates
        - отображения из каталога /views
        - логику и модули из каталога /logic
    
    Доступ к указанным объектам осуществляется через поля класса,
    названные соответственно models, templates, views, logic
    """
    
    @property
    def Models(self):
        return self.__models
    
    @property
    def Views(self):
        return self.__views
    
    @property
    def Logic(self):
        return self.__logic
    
    @property
    def Templates(self):
        return self.__templates
    
    @property
    def Config(self):
        return self.__config
    
    #===========================================================================
    # Загрузчики
    #===========================================================================
    
    def setConfig(self, config):
        self.__config = config
    
    def setInfo(self, info):
        self.__info = SiteInfo().read_info(info)
    
    def loadTemplates(self):
        self.__templates = Templates(self.Config)
    
    def loadLogic(self, path):
        pass
    
    def loadViews(self, path):
        pass
    
    def loadModels(self, path):
        pass

    def __init__(self):
        
        self.__models = None
        self.__views = None
        self.__logic = None
        self.__templates = None
        self.__config = None
    
    
