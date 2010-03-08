from helpers.tweak import Section

Templates = Section(
    TEMPLATE_FOLDER="path://simple.templates",
)

Site = Section(
    ROUTES=Section({
        "/" : "lazy://simple.views.index::IndexView"
    })
)

