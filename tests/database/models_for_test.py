from vitamin.modules.database.features import autoinc, primary, length, default, \
    notnull
from vitamin.modules.database.fields import IntegerField, CharField, \
    ForeignField
from vitamin.modules.database.model import Model

class User(Model):
    
    id = IntegerField(autoinc, primary)    
    name = CharField(default("John"), length(100))
    address = CharField(length(100))

class Parent(Model):
    
    id = IntegerField(autoinc, primary)
    name = CharField(length(100), notnull)

class Children(Model):
    
    id = IntegerField(autoinc, primary)    
    parent = ForeignField(Parent)   
