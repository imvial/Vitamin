
#$Rev: 114 $     
#$Author: fnight $  
#$Date: 2009-08-16 18:32:27 +0400 (Вс, 16 авг 2009) $ 

#This file is part of Vitamin Project

class WrongTemplateIntegrity(Exception):
    """Исключение, говорящее об ошибке разметки шаблона
    
    index - приблизительный индект ошибки в коде шаблона
    """
    def __init__(self, index):
        self.index = index
        self.value = """
       
       Ошибка разметки шаблона. Возможно, нарушено положение
       открывающих или закрывающих тегов. Просим выс исправить
       исходный текст шаблона и повторить попытку.
       
       Некоторая помощь:
            Вероятный индекс: {0}""".format(index)
                    
    def __str__(self):
        return(self.value)
    
class LoopException(Exception):
    """
    Ошибка директивы include, образовался цикл
    """
    def __init__(self,parent,child):        
        self.value = """
       
           Ошибка директивы #include, образовался цикл       
           Некоторая помощь:
                Ошибка в вызове шаблона {0} из шаблона {1}""".format(child,parent)
    def __str__(self):
        return(self.value)
