from helpers.tweak import Section

Templates = Section(
    TEMPLATE_FOLDER="path://simple.templates",)

Site = Section(
               
    FOLDERS=Section({
                     
        "styles": Section(
            path="path://simple.stuff.styles",
            extensions=[".css"],
            conversions=Section(default="lazy://vitamin.modules.storage.conversions::css_style"),
            fakepath="files/styles"),
            
        "scripts": Section(
            path="path://simple.stuff.scripts",
            extensions=[".js"],
            conversions=Section(default="lazy://vitamin.modules.storage.conversions::jscript"),
            fakepath="files/scripts"),
            
        "images": Section(
            path="path://simple.stuff.images",
            extensions=[".jpg", ".png"],
            conversions=Section(default="lazy://vitamin.modules.storage.conversions::image"),
            fakepath="files/images"),
    }),
    
    
    VIEWS=Section({
        "index" : "lazy://simple.views.index::IndexView",
        "files" : "lazy://simple.views.file::FileGet"
    }),
               
    ROUTES=Section({
        "/" : "index",
        "/wsgi" : "index.wsgi",
        "/files/{storage}/{file}" : "files"
    }),
    
   DATABASE=Section(
        MODELS_INIT="lazy://simple.models")
)

