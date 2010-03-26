from abc import ABCMeta, abstractmethod, abstractproperty
from collections import OrderedDict
from vitamin.config import tweak, Parameter
from vitamin.modules.database.expression import Expression
from vitamin.modules.database.fields import CharField, IntegerField, Field
from vitamin.modules.database.queries import QueryCreate, QueryInsert, \
    QuerySelect, QueryUpdate, QueryDelete
from vitamin.modules.database.sqlbuilder import Builder
from vitamin.modules.database.sqlbuilder.constructor import Context
from vitamin.modules.database.sqlbuilder.definitions import Names
import unittest
import sqlite3
import sys

"""
Тут оговорочка. Не будем мутить воду и изобратать
какие- то интерфейсы для провайдеров баз данных,
т.к. существует обкатанный интерфейс 
DB-API 2.0 interface, и все известные провайдеры
баз данных на Python ориентируются на соответствие
этому интерфейсу.

http://www.python.org/dev/peps/pep-0249/
"""

class PDO():
    
    def __init__(self, config=None):
        
        #поля конфигурационного файла
        self.PROVIDER = Parameter()
        self.LOCATION = Parameter()
        self.USER = Parameter()
        self.PASSWD = Parameter()
        self.CONNECT_WITH = Parameter() 
        
        tweak(self, "Database", config)
        
        self.connection = None       
        
    def connect(self):
        _args = []
        for arg in self.CONNECT_WITH:
            try:
                _args.append(getattr(self, arg))
            except AttributeError as err:
                raise err
            self.connection = self.PROVIDER.connect(*_args)
        return self.connection           
               
    def gosql(self, function):
        if self.connection:
            return self.connection.execute(function())
        else:
            raise Exception("No connection")
    
    def execute(self, query):
        if self.connection:
            return self.connection.execute(query)
        else:
            raise Exception("No connection")
        
class ORM():
    
    def __init__(self, pdo, config):
        
        self.builder = Builder()
        self.models = []
        self.pdo = pdo
        self.preload()
        
    def regiserModel(self, model):
        
        model.PDO = self.pdo
        self.models.append(model)   
        
    def preload(self):
        
        QueryCreate.builder = self.builder.create(Names.Create.definition)
        QueryInsert.builder = self.builder.create(Names.Insert.definition)
        QuerySelect.builder = self.builder.create(Names.Select.definition)
        QueryUpdate.builder = self.builder.create(Names.Update.definition)
        QueryDelete.builder = self.builder.create(Names.Delete.definition)
        Expression.builder = self.builder.create(Names.Expression.definition)
        

        
            
