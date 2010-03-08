from unittest import TestCase
from vitamin.modules.tpl import Templates
from vitamin.config import tweak, Parameter, Section

import os

class TestSystem(TestCase):
    
    def __init__(self, *args, **kwargs):
        
        TestCase.__init__(self, *args, **kwargs)        
        config = dict(
            Templates=Section(
                TEMPLATE_FOLDER="path://vitamin.modules.tpl.tests.templates"
            ))
        self.system = Templates(config)
        
    def test_init(self):        
        template = self.system.load("test1")
        print(template.info())
        
    def test_extend(self):
        template = self.system.load("test_extend_child")
        print(template.render())
        
