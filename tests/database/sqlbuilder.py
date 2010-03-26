from unittest import TestCase
from vitamin.modules.database import PDO, ORM
from tests.database.models_for_test import User, Parent, Children

    
pdo = PDO(config="tests.framework.simple.config")
orm = ORM(pdo=pdo, config="tests.framework.simple.config")

pdo.connect()   

orm.regiserModel(User)
orm.regiserModel(Parent)
orm.regiserModel(Children)

    
class TestSQL(TestCase):
        
    def test_0create(self):
        User.Create().go()
        
    def test_1insert(self):
        u = User()
        u.name = "Karlson"
        u.address = "roof"
        User.Insert().instance(u).go()
        u2 = User()
        User.Insert().instance(u2).go()
        
    def test_2update(self):
        u = User()
        u.id = 1
        u.name = "Sith"
        User.Update().fields(User.name).instance(u).go()
        
    def test_3select(self):
        query = (User.Select().where(User.id > 0).single().go())
        self.assertTrue(isinstance(query, User))
        self.assertEqual(query.id, 1)
        self.assertEqual(query.name, "Sith")     
        self.assertEqual(query.address, "roof")   
        
    def test_4delete(self):
        User.Delete().where((User.id == 1) & (User.id < 3)).go()
        
    def test_5foreign(self):
        Parent.Create().go()
        Children.Create().go()
        p = Parent()
        p.name = "first"
        p.Append()
        p.name = "second"
        p.Append()
        s = Children()
        parent = Parent.Select().where(Parent.name == "first").single().go()
        s.parent = parent
        s.Append()
        s.Append()
        s.Append()
        s.Append()
        s.Append()
        childrens = parent.Foreign(Children.parent)
        self.assertTrue(len(list(childrens)) == 5)



