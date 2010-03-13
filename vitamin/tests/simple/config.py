from helpers.tweak import Section

Templates = Section(
    TEMPLATE_FOLDER="path://simple.templates",)

Site = Section(
               
    FOLDERS=Section({
        "styles": "path://simple.stuff.styles",
        "scripts": "path://simple.stuff.scripts"
    }),
    
    FOLDER_EXTENSIONS=Section({
        "styles": [".css"],
        "scripts": [".js"]
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

