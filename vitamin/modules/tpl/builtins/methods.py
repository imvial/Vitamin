
#$Rev: 114 $     
#$Author: fnight $  
#$Date: 2009-08-16 18:32:27 +0400 (Вс, 16 авг 2009) $ 

#This file is part of Vitamin Project

def upper(arg):
    return arg.upper()

def lower(arg):
    return arg.lower()

def format(string, arg):
    return string.format(arg)

def css_style(style_file):
    return """<link href="{0}" rel="stylesheet" type="text/css"/>""".format(style_file)

def jscript(script_file):
    return """<script src="{0}" type="text/javascript">//</script>""".format(script_file)

nulline = "\n"
