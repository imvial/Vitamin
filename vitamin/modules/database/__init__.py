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

class Data():
    
    """
    Объект- контейнер, который обрабатывает данные
    курсоров базы данных, имитирует курсоры и позволяет
    выполнять некоторые другие операции над данными.
    Создается на этапе выполнения запроса к базе данных
    на основе курсора, который выполнял операцию
    cursor.execute, также может использоваться сам по
    себе для обработки и аггрегации табличных данных
    """
    
    header = None
    rows = None
    row_length = 0
    
    def __init__(self, cursor=None):
        
        self.head = []
        self.rows = []
        if cursor:
            if cursor.description:
                self.description = cursor.description
                self.row_length = len(cursor.description)
                self.head = [name[0] for name in cursor.description]
                self.append_iter(cursor)
        
    def set_head(self, *names):
        
        """
        Используется в том случае, когда класс создается
        без объекта cursor. Устанавливает заголовок таблицы
        и число столбцов в таблице данных.
        """
        
        assert not self.row_length
        self.row_length = len(names)
        self.header = names
        
    def append_row(self, row):
        
        assert row
        assert isinstance(row, (tuple, list))
        assert len(row) == self.row_length, "%s:%s" % (len(row), self.row_length)
        
        self.rows.append(row)
        
    def append_iter(self, cursor):
        
        for row in cursor:
            self.append_row(row)

    def append_items(self, *row):
        
        self.append_row(row)
               
    def __iter__(self):
        
        """
        Стандартное поведение функции __iter__ эквивалентно
        выполнению self.iter_rows
        """
        
        return self.iter_rows()
        
    def iter_rows(self):
        
        """
        Возвращает генератор, итерирующий строки
        таблицы данных
        """
        
        def __iterator():            
            for row in self.rows:
                yield row
            raise StopIteration()
        
        return __iterator()
    
    def iter_columns(self):
        
        """
        Возвращает генератор, итерирующий столбцы
        таблицы данных
        """
        
        def __iterator():
            for i in range(self.row_lenght):
                yield self.column(i)
            raise StopIteration
                            
        return __iterator()
    
    def row(self, index):
        
        """
        Возвращает строку из набора данных с порядковым номером
        @index
        """
        
        return self.rows[index]
    
    def column(self, index):
        
        """
        Возвращает стоблец из набора данных с порядковым номером
        @index
        """
        
        return [r[index] for r in self.rows]      
         

class PDO():
    
    def __init__(self, config=None):
        
        #поля конфигурационного файла
        self.PROVIDER = Parameter()
        self.LOCATION = Parameter()
        self.USER = Parameter()
        self.PASSWD = Parameter()
        self.CONNECT_WITH = Parameter() 
        self.DATA_TYPE = Parameter(Data)
        
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
            cursor = self.connection.execute(function())
            return self.DATA_TYPE(cursor) if self.DATA_TYPE else cursor
        else:
            raise Exception("No connection")
    
    def execute(self, query):
        if self.connection:
            cursor = self.connection.execute(query)
            return self.DATA_TYPE(cursor) if self.DATA_TYPE else cursor
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
        

        
            
