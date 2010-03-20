from collections import OrderedDict
from decimal import self

class FormItem():
    
    def __init__(self, type, name):
        self.type = type
        self.name = name

class TextBox():
    
    def __init__(self, name, row=22, col=3, text=None):
        
        FormItem.__init__(self, None, name)

        self.rows = row
        self.cols = col
        self.text = text
    
class Input(FormItem):
    
    def __init__(self, name, type, value=None, text=None, param=None):
        
        FormItem.__init__(self, type, name)
        
        self.value = value
        self.text = text
        self.param = param

class Option():
    
    def __init__(self, name, size=1, values):
        self.name = name
        self.values = OrderedDict()
        for value, text in values:
            self.values[value] = text
            
class Button(Input):
    
    def __init__(self, name, value=None):
        Input.__init__(self, name=name, type="button", value=value)

class CheckBox(Input):
    
    def __init__(self, name, value, text, param):
        Input.__init__(self, name=name, type="checkbox", value=value, text=text, param=param)        

class RadioButton(Input):
    
    def __init__(self, name, value, text, param):
        Input.__init__(self, name=name, type="radio", value=value, text=text, param=param)        

class ResetButton(Input):
    
    def __init__(self, value):
        Input.__init__(self, type="rest", value=value)        
        
class SubmitButton(Input):
    
    def __init__(self, value):
        Input.__init__(self, type="submit", value=value)        
        
class InputSizable(FormItem):
    
    def __init__(self, name, type, size=16, maxlength=32):
        FormItem.__init__(self, type, name)
        self.size = size
        self.maxlength = maxlength
       
class InputText(InputSizable):
    
    def __init__(self, name, size=16, maxlength=32):
        InputSizable.__init__(name=name, type="text", size=size, maxlength=maxlength)

class InputPassword(InputSizable):
    
    def __init__(self, name, size=16, maxlength=32):
        InputSizable.__init__(name=name, type="password", size=size, maxlength=maxlength)


    
