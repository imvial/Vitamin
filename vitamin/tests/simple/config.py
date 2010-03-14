from helpers.tweak import Section

Templates = Section(
    TEMPLATE_FOLDER="path://simple.templates",)

Site = Section(
               
    FOLDERS=Section({
        "styles": "path://simple.stuff.styles",
        "scripts": "path://simple.stuff.scripts"
    }),
    
    FOLDER_EXTENSIONS={
        "styles": [".css"],
        "scripts": [".js"]
    },
    
    DEFAULT_CONVERSIONS=Section({
        "styles": "lazy://vitamin.modules.tpl.builtins.methods::css_style",
        "scripts": "lazy://vitamin.modules.tpl.builtins.methods::jscript"
    }),
    
    VIEWS=Section({
        "index" : "lazy://simple.views.index::IndexView",
    }),
               
    ROUTES=Section({
        "/" : "index",
        "/info" : "index.info",
        "/wsgi" : "index.wsgi"
    })
)

