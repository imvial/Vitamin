from unittest import TestCase
from vitamin.modules.tpl import Templates, context
from vitamin.config import Tweak, Parameter
from vitamin.modules.tpl.exceptions import LoopException

import os
def LowerUpper(string):
    return string.title()

class IncludeTest(TestCase, Tweak("Templates")):
    def setUp(self):        
        self.test_folder = os.path.dirname('./templates/include/')
        self.tweak()
        self.system = Templates(self.test_folder)
        self.template1 = self.system.load("includ")
        self.template2 = self.system.load("test_include1")
        self.template3 = self.system.load("includ1")
        
    def test_notInclude(self):        
        assert self.template1.render()=="it is includ"
    def test_simpleInclude(self):        
        assert len(self.template2.render())==13
    def test_insideInclude(self):
        names=[1,2,3]
        assert  len(self.template3.render(context.Context(names=names)))==98
    def test_loopInclude(self):
        try:
            template=self.system.load("loopincludeStart")
        except Exception as err:
            print (err)
            
            