from unittest import TestCase
from vitamin import SitesManager

from vitamin.tests import simple
from vitamin.bindings.wsgi import HttpRequest
import os
simple_site_path = os.path.dirname(simple.__file__)

class SiteManagerTest(TestCase):
    
    def test_load(self):
        
        sm = SitesManager()
        sm.loadSite(simple_site_path)
        simple = sm.Sites["simple"]
        
        req = HttpRequest(None, None)
        req.PATH = "/info"
        
        simple.Views.request(req)
        print("------------------------------")
        print(req.join())
