from vitamin.modules.templates.chunks import BlockChunk, ExtendChunk, IncludeChunk
from vitamin.modules.templates.exceptions import LoopException
#$Rev: 117 $     
#$Author: fnight $  
#$Date: 2009-08-20 18:16:18 +0400 (Чт, 20 авг 2009) $ 

#This file is part of Vitamin Project


#$Rev: 117 $     
#$Author: fnight $  
#$Date: 2009-08-20 18:16:18 +0400 (Чт, 20 авг 2009) $ 

#This file is part of Vitamin Project

"""Модуль, содержаший инструмент наследования шаблонов.

Наследование шаблонов происходит на основе директивы {{extend: smth}}
в коде шаблона. Идея наследования подсмотрена в шаблонной системе 
web-framework'a Django. Механизм наследования заключается в следующем:
Шаблон размечается с помощью заголовков {{block: name}}..{{end}}.
Когда базовый блок загружается системой наследования, то в наследующем
шаблоне осуществляется поиск блоков, имена которых совпадают с именами
в базовом блоке. Содержимое таких блоков в базовом шаблоне заменяется 
содержимым блоков наследующего шаблона. Возвращается базовый шаблон с
внесенными изменениями.

ВНИМАНИЕ! Для запуска процедуры наследования необходимо использовать
функцию mutate.

ВНИМАНИЕ! Загрузчики шаблонов автоматически инициируют процедуру наследования.
Нет необходимости самостоятельно запускать наследование вслучае их 
использования"""


    
class Mutagen():
    
    listOfInclude = []
    
    def treeToDict(self, tokenList, tokenType=BlockChunk):
        
        """
        Разворачивает иерархическую структуру токенов в списке 
        tokenList в словарь блоков. Ключами становлятся имена блоков, 
        а значениями - сами объекты блоков
        """
        
        lst = {x.name:x for x in tokenList \
                if type(x) == tokenType}     
                
        for token in tokenList:
            if token.children:
                lst.update(self.treeToDict(token.children,tokenType))
        return lst
                  
                   
                    
                    
        
              
    def mutateBlock(self, baseBlocksDict, block) -> bool:
        
        """
        Заменяет содержимое блока из baseBlocksDict, имя которого совпадает
        с block.name на содержимое блока block
        
        baseBlocksDict - словарь, сгенерированый функцией treeToDict или аналогом
        
        block - экземпляр класса tokens.BlockToken
        
        Функция вернет True, если блоки с одинаковым названием найдены и 
        замена содержимого произведена, или False, если блок с названием 
        block.name не найден в споваре baseBlocksDict
        """
        
        try:
            baseBlock = baseBlocksDict[block.name]      
            baseBlock.children = block.children
            return True
        except KeyError:
            return False
        
    def include(self,loader,template):
        dictofInclud=self.treeToDict(template.chunks, IncludeChunk) 
        for name,token in dictofInclud.items():
            includeToken=loader(name)
            dictofInclude=self.treeToDict(includeToken.chunks, IncludeChunk)
            for n,c in dictofInclude.items():
                if n==template.name:
                    raise LoopException
            includeToken=self.mutate(loader, includeToken)            
            dictofInclud[name].children=includeToken.chunks            
        return template 
      
    def listInclude(self, tokenList, loader):
         
            lst = []
            haveInclud = False
            for token in tokenList:
                if isinstance(token, IncludeChunk):                    
                    lst.extend(self.unpackingInclude(token, loader))
                    haveInclud = True
                else:
                    if token.children:
                        token.children = self.listInclude(token.children, loader)
                    lst.append(token)
            if not(haveInclud):
                try:
                    self.listOfInclude.pop()
                except:
                    pass
            return lst 
          
    def unpackingInclude(self, includToken, loader):
            """
            Распаковывает IncludeChunk, возвращает набор Chunkов из влючаемого шаблона
            Дабы совместить ее с системой наследования пропускает результат через mutate        
            """
            if includToken.name in self.listOfInclude:
                raise LoopException(self.listOfInclude.pop(), includToken.name)
            self.listOfInclude.append(includToken.name)                                   
            includeTemplate = loader(includToken.name)
            includeTemplate = self.mutate(loader, includeTemplate)
            return includeTemplate.chunks
        
    def findInclude(self, loader, template):
        """
        Функция, исполняющая директиву include
        Заменяет IncludeChunk на набор chunkов из включаемого шаблона        
        """
        template.chunks = self.listInclude(template.chunks, loader)
        return template   
                      
                  
    def mutate(self, loader, template):
        
        """
        Основная функция, производящая наследование шаблона.
        Именно её необходимо использовать для инициализации рекурсивного
        механизма наследования. Функция принимает два аргумента:
        
        loader - функция-загрузчик. Вызвав такую функцию с аргументом
        name, полученными из директивы extend, система должна получить
        экземпляр класса Template. Самое очевидное решение- использование
        функций, поставляемых загрузчиками.
        
        template - экземпляр класса Template, который будет унаследован
        от базового шаблона, имя которого определено директивой extend.
        Если директива extend в шаблоне не обнаружена, то функция вернет 
        данный аргумент.
        """

        try:
            extendBlock = [token for token in template.chunks 
                if type(token) == ExtendChunk][0]
        except IndexError:
            return self.findInclude(loader, template)
        
                   
                
                
                
            
            
        print("extending:", extendBlock.name)
        baseTemplate = loader(extendBlock.name)
        baseTemplate = self.mutate(loader, baseTemplate)    
        blocksDict = self.treeToDict(baseTemplate.chunks)
        candidates = [token for token in template.chunks 
                if type(token) == BlockChunk and token.name in blocksDict]                
        [self.mutateBlock(blocksDict, x) for x in candidates]
        
        return self.findInclude(loader, baseTemplate)

mutate = Mutagen().mutate
      
