"""
Match works to each other.

for each table, retrieve all ids
normalize/validate/parse them
then match them up

keep track of items that haven't been matched
either retrieve them with queries from the apis or use other methods to match them (e.g. on title or something)

Current sources+ids+how to retrieve them

openalex: (table: 'work')
    (openalex) id -> id or ids.openalex
    doi -> doi or ids.doi
    pmid -> ids.pmid
    pmcid -> ids.pmcid
    mag -> ids.mag

    urls (can also possibly be dois):
    for location in locations:
        location.landing_page_url or location.pdf_url

pure: (table: 'publication')
    (pure) id -> id
    (pure) uuid -> uuid
    doi -> doi
    isbn -> isbn
    urls:
        -> uri
        -> [location for location in locations]
        -> [ev.get('location') for ev in electronic_versions]
    scopusid -> scopus (or scopus_id?)

openaire: (table: 'research_product')
    (openaire) id -> id

    then for pid in pids:
        type = pid.scheme
        value = pid.value

    for instance in instances:
        for pid in instance.pids:
            type = pid.scheme
            value = pid.value


"""
