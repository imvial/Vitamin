from abc import ABCMeta, abstractmethod

class IModule(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self): pass
    @abstractmethod
    def go(self, context):pass
    @abstractmethod
    def info(self): pass

class IModuleURL(IModule):
    @abstractmethod
    def __init__(self): pass
    @abstractmethod
    def go(self, context): pass
    
class IView(metaclass=ABCMeta):   

    @abstractmethod
    def __call__(self):
        pass
    
    __site = None
    def __set_site(self, site):
        self.__site = site
    def __get_site(self):
        return self.__site
    Site = property(__get_site, __set_site)

__all__ = ["IModuleURL", "IView"]
