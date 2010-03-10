from iscript import IScript
from vitamin import SiteManager
from wsgiref.simple_server import make_server
import os


class server(IScript):

    def run(self, *args):
        
        path = os.getcwd()
        print("Starting server in", path)
        
        sm = SiteManager()
        sm.loadSite(path)
        
        server = make_server("127.0.0.1", 8080, sm)
        server.serve_forever()
