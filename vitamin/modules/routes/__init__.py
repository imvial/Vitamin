from vitamin.interfaces import IModuleURL
import re
from .rule import Rule

__all__ = ["RequestManager"]

import logging
logger = logging.getLogger("url")

class RuleFactory():
       
    def __block(self, matchobj):
        
        "Вытаскивает из matchobj имя первой группы и возвращает его"
        
        name = matchobj.group(1)
        vars = matchobj.group(3)
        if vars:
            return "(?P<{0}>{1})".format(name, vars)
        else:
            return "(?P<{0}>.*?)".format(name)
    
    def __convert(self, pretty):    
        
        "Преобразует pretty-look паттерн в регулярное выражение"   
        
        return re.sub("[{](.*?)([[](.*)[]])?[}]", self.__block, pretty)
    
    def __format(self, url):
        
        if url == "/": return url
        if url.endswith("/"): return url[:-1]
        return url
        
    def __make_rule(self, pretty):
        
        pattern = self.__format(self.__convert(pretty))         
        pattern += "$"
        rule = Rule(pretty, re.compile(pattern))
        
        logger.info("rule created: pretty '%s', regexp '%s'", pretty, pattern)
        
        return rule  

    def __call__(self, pretty):
        return self.__make_rule(pretty)

