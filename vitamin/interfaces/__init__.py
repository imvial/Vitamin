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

__all__ = ["IModuleURL", "IView"]
