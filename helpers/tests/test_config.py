from unittest import TestCase
from helpers.tweak import Tweak, Parameter, prepare

from helpers.tests import test_site_configuration
prepare(test_site_configuration)

class Simple(Tweak):
    
    def __init__(self):
        
        Tweak.__init__(self, "Simple")
        self.test = Parameter()
        self.test2 = Parameter(section="Another")
        self.default_one = Parameter(default=1)
        self.tweak()

class TweakTest(TestCase):
    
    def test_tweak(self):
        s = Simple()
        self.assertEqual(s.test, 1)
        self.assertEqual(s.test2, 2)
        self.assertEqual(s.default_one, 1)
