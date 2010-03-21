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
        "styles": Section(default="lazy://vitamin.modules.static.conversions::css_style"),
        "scripts": Section(default="lazy://vitamin.modules.static.conversions::jscript")
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

