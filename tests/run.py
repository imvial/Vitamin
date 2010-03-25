#! /usr/bin/python3

import os
import sys
import unittest
from functools import reduce

class TestRunner():
    
    """Класс, производящий последовательный запуск
    тестов проекта и выводящий результаты тестирования
    в удобном виде"""

    def __init__(self, *filters):

        self.filters = list(filters)
        self.modules = []
        self.suites = []
        
        self.filters.append("framework")
        
    def snoop(self):             
        for root, dirs, files in os.walk("../tests"):
            self.modules += [
                os.path.join(root, f)
                .replace("./", "")
                .replace("/", ".")[:-len(".py")] 
                    for f in files
                        if os.path.splitext(f)[1] == ".py" 
                        and f != "__init__.py" 
                        and f != sys.argv[0]
                        and not [True for x in self.filters if x in os.path.join(root, f)] ]

        self.modules = sorted(self.modules)
        print(self.modules)
        
    def load(self):
        loader = unittest.TestLoader()
        for module in self.modules:
            try:
                m = __import__(module[1:] if module.startswith(".") else module, fromlist=[1])
                self.suites.append(loader.loadTestsFromModule(m))
            except Exception as e:
                raise e
            
    def run(self):
        a = reduce(lambda x, y: unittest.TestSuite((x, y)), self.suites)
        runner = unittest.TextTestRunner(stream=sys.stdout, verbosity=2)
        runner.run(a)

sys.path.append(".")
sys.path.append("..")

t = TestRunner()
t.snoop()
t.load()
t.run()
#print(t.modules)     
