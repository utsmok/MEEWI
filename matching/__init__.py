"""
this module will try to find the same item in different sources as ingested into the db
for each itemtype there is a matcher.

Matches are made using unique ids (like dois, orcids, etc).
Once the initial matching is done, we'll see if it's necessary to do more matching on other fields (like title, authors, etc)

matches are stored in a separate table, e.g. work_matches or author_matches
these tables contain a column for each source (e.g. openalex, openaire, pure, ...)
and then a list of structs with the shade {id_type, id_value} that store how the matches were found, e.g. {"doi", "10.1000/xyz123"}
"""
