from vitamin.interfaces import IModuleURL
import re
from .rule import Rule

__all__ = ["RequestManager"]

class RequestManager():
       
    def __init__(self):        
       
        self.rules = []
        self._add_rules(self.ROUTES)        
    
    #===========================================================================
    # end
    #===========================================================================

    def __block(self, matchobj):
        "Вытаскивает из matchobj имя первой группы и возвращает его"
        name = matchobj.group(1)
        vars = matchobj.group(3)
        if vars:
            return "(?P<{0}>{1})".format(name, vars)
        else:
            return "(?P<{0}>.*?)".format(name)
    
    def __convert(self, pretty):    
        """Преобразует pretty-look паттерн в вид питоновской
        регулярки"""   
        return re.sub("[{](.*?)([[](.*)[]])?[}]", self.__block, pretty)
        
    def __add_rule(self, pretty, block):
        """Преобразует пару pretty-pattern и 
        func в объект Rule"""
        pattern = self.__format(self.__convert(pretty))
        
        pattern += "$"
        print(pattern)
        rule = Rule(block, re.compile(pattern))
        self.rules.append(rule)
        
    def __format(self, url):
        if url == "/": return url
        if url.endswith("/"): return url[:-1]
        return url
               
    def update(self, dictRoutes):
        for pretty, block in dictRoutes.items():
            self.__add_rule(pretty, block)

