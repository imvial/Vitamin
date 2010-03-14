from vitamin.modules.tpl import Templates
from vitamin.siteinfo import SiteInfo
from vitamin.views import ViewSystem
from vitamin.modules.static import StorageSystem

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
    
    @property
    def Info(self):
        return self.__info
    
    @property
    def Storage(self):
        return self.__storage
    
    #===========================================================================
    # Загрузчики
    #===========================================================================
    
    def load_config(self, config):
        self.__config = config
    
    def load_info(self, info):
        self.__info = SiteInfo().read_module(info)
    
    def load_templates(self):
        self.__templates = Templates(self.Config)
        
        context = dict(
            storage=self.__storage,
            info=self.__info
        )
            
        self.__templates.set_default_context(context)
    
    def load_logic(self, path):
        pass
    
    def load_views(self):
        self.__views = ViewSystem(self.Config, site=self)
    
    def load_models(self, path):
        pass
    
    def load_storage(self):
        self.__storage = StorageSystem(self.Config)

    def __init__(self):
        
        self.__models = None
        self.__views = None
        self.__logic = None
        self.__templates = None
        self.__config = None
        self.__info = None
        self.__storage = None
        
    
    
