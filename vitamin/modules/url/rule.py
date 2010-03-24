from functools import partial

import logging
logger = logging.getLogger("url")
    
class Rule():
    
    """Правило обаботки URL. Администратор сервера
    задает правила в виде словаря, содержащего обобщения
    URL, в виде ключей, и пользовательские функции обработки
    в виде значений.    
    """
        
    __slots__ = ["pretty", "regexp", "method", "__object"]
                
    @property
    def Object(self):
        return self.__object
    
    def __init__(self, pretty, regexp):
        
        self.pretty = pretty
        self.regexp = regexp
        self.method = None
        self.__object = None
        
    def setMethod(self, method_name):
        self.method = method_name    
        
    def setObject(self, object_inst):
        self.__object = object_inst
        
    def check(self, url):
        matchobj = self.regexp.match(url)
        logger.debug("rule checking '%s'...", self.regexp)      
        if matchobj:        
            _arguments = matchobj.groupdict()
            try:
                return partial(getattr(self.__object, self.method), **_arguments)
            except AttributeError as err:
                raise err
                
        else:
            return None
