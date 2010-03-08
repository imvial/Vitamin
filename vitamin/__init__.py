import os
from vitamin.site import Site
import sys
from helpers import lazyimport
from vitamin.siteinfo import SiteInfo

class SitesManager():
    
    """
    Инструмент для управления сайтами Vitamin, необходим для
    поддержки нескольких сайтов Vitamin на одном интерпретаторе
    Python. Для организации нормальной работы лучше запускать
    на одном интерпретороне один сайт
    """
    
    @property
    def Sites(self):
        return self.__sites
    
    def __init__(self):
        self.__sites = {}
    
    def loadSite(self, path):
        
        assert os.path.exists(path)
        
        templates_part = "templates"        
        info_part = "info"
        config_part = "config"
        logic_part = "logic"     
           
        site = Site()
        site_path, site_name = os.path.split(path)
            
        print("\nLoading site '{0}' from: \n    {1} ".format(site_name, site_path))        
        sys.path.append(site_path)        
        module = lazyimport.loadmodule(site_name)
       
        parts = {x:getattr(module, x) for x in dir(module) if not x.startswith("_")}
        if not config_part in parts:
            raise Exception("No config")
        if not info_part in parts:           
            raise Exception("No info")
        if not logic_part in parts:
            raise Exception("No logic")
        
        print("Parts loaded: ", ", ".join(parts.keys()))
        
        site.setConfig(parts[config_part])
        site.setInfo(parts[info_part])
        
        if templates_part in parts:
            site.loadTemplates()
#        site.loadLogic()
#        site.loadViews()
#        site.loadModels()
        
            
    
    def unloadSite(self, name):
        pass
    
    def reloadSite(self, name):
        pass
    

