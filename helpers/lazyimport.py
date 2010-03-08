import sys
import os
   
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
    
def loadmodule(name):    
    return __import__(name, fromlist=[])
    
def loadmodules(path, interface=None):
    assert os.path.exists(path)
    names = (x for x in os.listdir(path) if not x.startswith("_")
        and os.path.splitext(x)[1] == ".py") 
    
    sys.path.append(os.path.dirname(path))
    
    
