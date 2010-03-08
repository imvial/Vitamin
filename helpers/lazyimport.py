import sys
import os
from types import ModuleType
from time import sleep

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

    
    
