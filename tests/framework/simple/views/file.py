from vitamin.interfaces import IView

class FileGet(IView):    
  
    def __call__(self, request, storage, file):
        
        return self.Site.Storage(storage).stream(file)
