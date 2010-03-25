from unittest import TestCase
from vitamin.modules.templates import Templates, context
from vitamin.modules.templates.exceptions import LoopException

from vitamin.config import Section

import os
def LowerUpper(string):
    return string.title()

class IncludeTest(TestCase):
    
    def __init__(self, *args, **kwargs):
        
        TestCase.__init__(self, *args, **kwargs)   
             
        config = dict(
            Templates=Section(
                TEMPLATE_FOLDER="path://tests.templates.templates.include"
            ))
        
        self.system = Templates(config)
        
        self.template1 = self.system("include")
        self.template2 = self.system("test_include_one")
        self.template3 = self.system("include_two")
        
    def test_notInclude(self):
       
        self.assertEqual(self.template1.render(), "it is include")
        
    def test_simpleInclude(self):
                
        self.assertEqual(len(self.template2.render()), 14)
        
    def test_insideInclude(self):
        
        names = [1, 2, 3]
        self.assertEqual(len(self.template3.render(context.Context(names=names))), 101)
        
    def test_loopInclude(self):
        
        self.assertRaises(Exception, self.system, "cycle_include_start")

            
            
