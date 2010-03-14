from vitamin.modules.tpl.loader import ITemplateLoader
from vitamin.config import tweak, Parameter
import os
from vitamin.modules.tpl.template import Template

#$Rev: 122 $     
#$Author: fnight $  
#$Date: 2009-08-28 16:12:56 +0400 (Пт, 28 авг 2009) $ 

#This file is part of Vitamin Project

import logging
logger = logging.getLogger("tpl.loaders.file")

class FileLoader(ITemplateLoader):
    """Класс- загрузчик шаблонов из файлов"""

    def __init__(self, config):    
        self.TEMPLATE_FOLDER = Parameter()
        self.TEMPLATE_EXTENSION = Parameter()
        tweak(self, "Templates", config)
        
        logger.debug("loader configured to use folder '%s'" ,
            self.TEMPLATE_FOLDER)
        
        self.index = [x for x in os.listdir(self.TEMPLATE_FOLDER) 
            if not x.startswith(".") or not x.startswith("_")]
        self.tplExt = self.TEMPLATE_EXTENSION
        
    def __find__(self, ext, name):
        f = name + ext
        if f in self.index:         
            return os.path.join(self.TEMPLATE_FOLDER, f) 
   
    def loadText(self, name, text):
        return Template(text, name)    

    def load(self, name):
        
        path = self.__find__(self.tplExt, name)
        if not path:
            raise Exception("Шаблон {0} не найден!".format(name))
        
        with open(path, "rb") as f:            
            text = f.read().decode()            
            try:
                template = self.loadText(name, text)           
            except Exception as msg:        
                ext = str(msg) + "\n\n" + "Ошибка возникла в шаблоне: \n" + path
                raise Exception(ext)
        return template

    def save(self):
        pass


