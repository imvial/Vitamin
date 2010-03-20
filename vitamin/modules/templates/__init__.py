from vitamin.config import tweak, Parameter
from vitamin.modules.templates.mutagen import Mutagen
from vitamin.modules.templates.context import Context

class Templates():
    
    def __init__(self, site_config=None):      
        
        self.LOADER = Parameter()
        tweak(self, "Templates", site_config)        
        self.loader = self.LOADER(site_config)
        self.mutagen = Mutagen()
        
        self.__default_context = None
        
    def set_default_context(self, context):
        
        assert isinstance(context, Context)
        self.__default_context = context

    def __call__(self, name):
        
        """
        Загрузка шаблона из шаблонной системы при помощи
        указанного в конфиге загрузчика. Результатом
        выполнения этой процедуры будет готовый к использованию
        объект класса Template.
        """
               
        return self.mutagen.mutate(
            loader=self.loader,
            template=self.loader.load(name)).set_default_context(self.__default_context)
