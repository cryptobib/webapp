#
# Database db
#

db.define_table(
    "conf",

    Field("type"), # conf / journal

    Field("key"),
    Field("name"),
    Field("full_name"),

    Field("start_year", "integer"),
    Field("end_year", "integer")
)

db.define_table(
    "change",

    Field("date"),
    Field("desc", "text")
)
    

db.define_table(
    "entry",

    Field("type"),                  # proceedings / inproceedings / article

    Field("key_conf"),              # ex: AC
    Field("key_year", "integer"),   # ex: 2009
    Field("key_auth"),              # ex: KatVai
    Field("key_dis"),               # ex: a

    Field("start_page", "integer"), # ex: 636
    Field("end_page", "integer"),   # ex: 652
    
    Field("address"),
    Field("abstract"),
    Field("annote"),
    Field("author"),
    Field("booktitle"),
    Field("chapter"),
    Field("crossref"),
    Field("crossref_expanded"),     # expanded version of crossref, directly give the key of the crossref (no bibtex macro expansion required) - no quote
    Field("doi"),
    Field("edition"),
    Field("editor"),
    Field("eprint"),
    Field("howpublished"),
    Field("institution"),
    Field("journal"),
    Field("key"),
    Field("keywords"),
    Field("month"),
    Field("note"),
    Field("number", "integer"),
    Field("organization"),
    Field("publisher"),
    Field("school"),
    Field("series"),
    Field("title"),
    Field("type"),
    Field("url"),
    Field("volume"),
    Field("year", "integer")
)


#
# Misc
#

# Disable generic views
response.generic_patterns = []

# Use Bootstrap3 in forms
response.formstyle = SQLFORM.formstyles.bootstrap3_inline

    
