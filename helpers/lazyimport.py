import sys
import os
from types import ModuleType
from time import sleep

LAZY_IMPORT_PREFIX = "lazy://"
PATH_RESOLVER_PREFIX = "path://"

class SmartImportError(Exception):
    
    def __init__(self, string):
        self.string = string
    
    def __str__(self):
        return "Wrong prefix for smart import!\nRequested string is:\n    " + self.string
    
def lazy_load(query):
    
    if isinstance(query, str):
        if query.startswith(LAZY_IMPORT_PREFIX):
            return smartimport(query[len(LAZY_IMPORT_PREFIX):])
        elif query.startswith(PATH_RESOLVER_PREFIX):
            module = smartimport(query[len(PATH_RESOLVER_PREFIX):])
            assert "__file__" in dir(module), "По указанному пути не найден модуль"
            return os.path.dirname(module.__file__)
        else:
            return query    
    else:
        return query
    
def lazy_load_from_data(self, index, item):
    
    self.data[index] = lazy_load(item)
    return self.data[index]


def smartimport(path, environment=[]):
    if environment:
        sys.path.extend(environment)
    
    pval = None
    try:
        pmodule, pval = path.split("::")
    except ValueError:
        pmodule = path
        
    imodule = __import__(pmodule, globals={}, locals={}, fromlist=[""])
    if pval:
        return getattr(imodule, pval)
    else: return imodule
    
def load_classes(package, interface=None):
    
    if not isinstance(package, ModuleType):
        return
    
    items = {x:getattr(package, x) for x in dir(package) 
        if not x.startswith("_")}
    
    if interface:
        return {name:value for name, value in items.items()
            if issubclass(value, interface)}
    else:
        return items
    
def loadmodule(name):
    return __import__(name, fromlist=[])
    
def load_classes_deep(package, interface):
    
    print("lazyimport.py: deep import started from -> ", package.__name__)
    result = {}
    _res = load_classes(package, interface)
    if _res:
        result.update(_res)
    
    path = os.path.dirname(package.__file__)
    sys.path.append(path)
    
    for item in (x.replace(".py", "") for x in os.listdir(path)
        if not x.startswith("_") and os.path.splitext(x)[1] == ".py"):
        
        print("lazyimport.py: deep import from -> ", item)
        sleep(1)
        module = loadmodule(item)
        _res = load_classes(module, interface)
        if _res:
            result.update(_res)
            
    del sys.path[sys.path.index(path)]
    return result

    
    
