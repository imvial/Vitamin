from unittest import TestCase
from helpers.tweak import tweak, Parameter, prepare

from tests.helptests import test_site_configuration
prepare(test_site_configuration)

class Simple():
    
    def __init__(self):
        
        self.test = Parameter()
        self.test2 = Parameter(section="Another")
        self.default_one = Parameter(default=1)
        tweak(self, "Simple")

class TweakTest(TestCase):
    
    def test_tweak(self):
        s = Simple()
        self.assertEqual(s.test, 1)
        self.assertEqual(s.test2, 2)
        self.assertEqual(s.default_one, 1)
