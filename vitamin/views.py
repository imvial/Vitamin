from vitamin.interfaces import IView
from vitamin.config import tweak, Parameter, Section
from vitamin.modules.url import RequestManager

class ViewSystem(dict):
    
    def __init__(self, config):
        
        self.ROUTES = Parameter()
        tweak(self, "Site", config)
        
        self.request_manager = RequestManager()
        
        assert isinstance(self.ROUTES, Section)

        #remember! lazy import        
        self.ROUTES.preload()
        

        for name, value in self.ROUTES.items():
            
        print("views.py: routing table -> ")
        for name, value in self.ROUTES.items():
            print("        route '{0}' -> {1}".format(name, value))
        
