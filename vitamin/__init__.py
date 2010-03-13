from vitamin.bindings.wsgi import HttpRequest
import os
from vitamin.site import Site
import sys
from helpers import lazyimport
from vitamin.siteinfo import SiteInfo

class SiteManager():
    
    """
    Инструмент для управления сайтами Vitamin, необходим для
    поддержки нескольких сайтов Vitamin на одном интерпретаторе
    Python. Для организации нормальной работы лучше запускать
    на одном интерпретороне один сайт
    """
    
    @property
    def Site(self):
        return self.__site
    
    def __init__(self):
        self.__site = {}
        
    def __call__(self, env, send_response):
        
        req = HttpRequest(env, send_response)
        self.Site.Views.request(req)
        return req.send()
        
    
    def load_site(self, path):
        
        assert os.path.exists(path)
        
        templates_part = "templates"        
        info_part = "info"
        config_part = "config"
        logic_part = "logic"
        views_part = "views"  
           
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
        if views_part in parts:
            site.loadViews()
            
        self.__site = site

    
    def unload_site(self, name):
        pass
    
    def reload_site(self, name):
        pass
    

