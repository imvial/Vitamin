from vitamin.modules.templates.lexical import TemplateAnalyzer
from vitamin.modules.templates.context import Context, Aggregator
import logging

#$Rev: 122 $     
#$Author: fnight $  
#$Date: 2009-08-28 16:12:56 +0400 (Пт, 28 авг 2009) $ 

#This file is part of Vitamin Project

_analyse = TemplateAnalyzer().load

TEMPLATE_INFO_STRING = \
"""
    '{0}' template info:
        root.chunks: {1};
        total.chunks: {2}; 
"""

logger = logging.getLogger("template")

class TemplateInfo():
    
    def __init__(self,
        name,
        root_chunks=0,
        total_chunks=0):
    
        self.name = name
        self.root_chunks = root_chunks
        self.total_chunks = total_chunks
        
    def __str__(self):
        return TEMPLATE_INFO_STRING.format(self.name,
                    self.root_chunks,
                    self.total_chunks)
  
class Template():

    def __init__(self, text="", name="default.template.name", default_context=None):
        
        self.name = name
        self.chunks = []
        self.text = text
        self.default_context = default_context
        if text: 
            self.chunks = _analyse(text)           

    def set_default_context(self, context):
        
        assert isinstance(context, Context)
        self.default_context = context
        return self

    def render(self, context=None):
        
        ctx = None
        if self.default_context:
            ctx = Context(self.default_context.copy())
            if context: 
                ctx.update(context)
        
        logger.debug("context: %s", ctx)
        
        aggr = Aggregator()
        [x.render(ctx or context, aggr) for x in self.chunks]
        return aggr.join()
    
    def info(self):
        
        root_chunks = len(self.chunks)
        total_chunks = root_chunks
        
        def count_chunks(chunk):
            nonlocal total_chunks
            total_chunks += len(chunk.children)
            (count_chunks(x) for x in chunk.children)
            
        for chunk in self.chunks:
            count_chunks(chunk)
            
        return TemplateInfo(self.name, root_chunks, total_chunks)
                        
                
                
            

