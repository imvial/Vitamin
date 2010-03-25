from vitamin.interfaces import IView
from vitamin.modules.templates import Context

class IndexView(IView):
    
    def __call__(self, request):
        
        template = self.Site.Templates("index")
        
        context = Context()
        context.header = "Привет, землянин!"
        context.additional_header = "как жизнь?"
        
        return template.render(context)
   
    def wsgi(self, request):
        
        s = []
        for name, value in request.environ.items():
            s.append("{0} ->  {1}<br>".format(name, value))
        return s
