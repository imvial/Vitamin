from helpers.tweak import Section

Templates = Section(
    TEMPLATE_FOLDER="path://simple.templates",
)

Site = Section(
               
    VIEWS=Section({
        "index" : "lazy://simple.views.index::IndexView",
    }),
               
    ROUTES=Section({
        "/" : "index",
        "/info" : "index.info",
        "/wsgi" : "index.wsgi"
    })
)

