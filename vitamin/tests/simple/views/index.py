from vitamin.interfaces import IView

class IndexView(IView):
    
    def __call__(self, request):
        
        template = self.Site.Templates("index")
        return template.render()
   
    def wsgi(self, request):
        
        s = []
        for name, value in request.environ.items():
            s.append("{0} ->  {1}<br>".format(name, value))
        return s
