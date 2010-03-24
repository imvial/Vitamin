from helpers.tweak import Section

Templates = Section(
    TEMPLATE_FOLDER="path://simple.templates",)

Site = Section(
               
    FOLDERS=Section({
                     
        "styles": Section(
            path="path://simple.stuff.styles",
            extensions=[".css"],
            conversions=Section(default="lazy://vitamin.modules.static.conversions::css_style"),
            fakepath="files/styles"),
            
        "scripts": Section(
            path="path://simple.stuff.scripts",
            extensions=[".js"],
            conversions=Section(default="lazy://vitamin.modules.static.conversions::jscript"),
            fakepath="files/scripts"),
    }),
    
    
    VIEWS=Section({
        "index" : "lazy://simple.views.index::IndexView",
        "files" : "lazy://simple.views.file::FileGet"
    }),
               
    ROUTES=Section({
        "/" : "index",
        "/info" : "index.info",
        "/wsgi" : "index.wsgi",
        "/files/{storage}/{file}" : "files"
    })
)

