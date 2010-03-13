from vitamin.config import tweak, Parameter
from vitamin.modules.tpl.mutagen import Mutagen

class Templates():
    
    def __init__(self, site_config=None):      
        
        self.LOADER = Parameter()
        tweak(self, "Templates", site_config)        
        self.loader = self.LOADER(site_config)
        self.mutagen = Mutagen()  
    
    def __call__(self, name):
        
        """
        Загрузка шаблона из шаблонной системы при помощи
        указанного в конфиге загрузчика. Результатом
        выполнения этой процедуры будет готовый к использованию
        объект класса Template.
        """
               
        return self.mutagen.mutate(
            loader=self.loader,
            template=self.loader.load(name))
