from extra.server.interfaces.iprogram import IProgram
from vitamin.config import tweak, Parameter

class ServerProgram(IProgram):
    
    def __init__(self):        
        
        self.NEXT_NODE = Parameter()
        tweak(self, "Loader")
        
        self.program = self.NEXT_NODE()
    
    def go(self, iheader):
        self.program.go(iheader)
    
    def info(self):
        return "Vitamin binding for native server system"
        
    def restart(self):
        self.program = self.NEXT_NODE()
