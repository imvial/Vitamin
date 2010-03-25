from vitamin.interfaces import IView
from vitamin.config import tweak, Parameter, Section
from vitamin.modules.routes import RuleFactory
from vitamin.bindings.wsgi import HttpRequest

class ViewSystem(dict):
    
    def __init__(self, config, site):
        
        self.site = site
        self.ROUTES = Parameter()
        self.VIEWS = Parameter()
        tweak(self, "Site", config)
        assert isinstance(self.VIEWS, Section)
        #у секций ленивый импорт     
        self.VIEWS.preload()
        
        self.rules = []
        self.make_rule = RuleFactory()      
        #rule = self.make_rule(name)
        
        for name, value in self.VIEWS.items():
            view = value()
            view.Site = site     
            self.VIEWS[name] = view
        
        for pattern, tpl in self.ROUTES.items():
            
            rule = self.make_rule(pattern)
            arr = tpl.split(".")
            if len(arr) == 2:
                view_name, method_name = arr
            elif len(arr) == 1:
                view_name, method_name = arr[0], "__call__"
            elif len(arr) > 2:
                raise Exception("Слишком детальный маршрут: " + tpl)

            assert view_name in self.VIEWS.keys()
            
            rule.setObject(self.VIEWS[view_name])
            rule.setMethod(method_name)
            
            self.rules.append(rule)
    
    def request(self, httpreq):
        
        for rule in self.rules:
            caller = rule.check(httpreq.PATH)
            if caller:
                result = caller(request=httpreq)
                if result:
                    if isinstance(result, (list, tuple)):
                        httpreq.extend(result)
                    else:
                        httpreq.append(result)
                return httpreq
        
        raise Exception("404")
                
