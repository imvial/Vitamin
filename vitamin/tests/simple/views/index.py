from vitamin.interfaces import IView

class IndexView(IView):
    
    def __call__(self, request):
        
        return "<h1>Hello world</h1>"

    def info(self, request):
        
        s = []
        s.append("<h1>Site info:</h1>")
        s.append("<br>")
        s.append("<h2>name: {0}</h2>".format(self.Site.Info.name))
        s.append("<h2>description: {0}</h2>".format(self.Site.Info.description))
        s.append("<h2>authors: {0}</h2>".format(self.Site.Info.authors))
        s.append("<h2>version: {0}</h2>".format(self.Site.Info.version))
        return s
    
    def wsgi(self, request):
        
        s = []
        for name, value in request.environ.items():
            s.append("{0} ->  {1}<br>".format(name, value))
        return s
