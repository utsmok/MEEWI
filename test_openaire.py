from itertools import batched

import httpx

from db.duckdb import DuckDBInstance
from retrieval.openaire import OAIREEndpoint, OAIREFilter, OAIREQuery, OAIREQuerySet
from utils.validate import validate_doi

print("starting")
db = DuckDBInstance()
processed = 0
with httpx.Client() as client:
    counter = 0
    all_dois = db.get_ids("work", "doi")
    validated = []
    for doi in all_dois:
        try:
            doi = validate_doi(doi)
            validated.append(doi)
        except ValueError:
            continue

    all_dois = list(set(validated))  # Remove duplicates
    all_dois = [doi for doi in all_dois if doi]  # Remove empty strings
    queries = []
    for idbatch in batched(all_dois, 10, strict=False):
        batch = []
        for doi in idbatch:
            try:
                doi = validate_doi(doi)
                batch.append(doi)
            except ValueError:
                continue
        if not batch:
            continue
        processed += len(batch)
        queries.append(
            OAIREQuery(
                endpoint=OAIREEndpoint.RESEARCHPRODUCTS,
                filters=[
                    OAIREFilter(
                        filter_type="pid",
                        filter_value=batch,
                    )
                ],
            )
        )
        counter += 1

        if counter >= 100:
            queryset = OAIREQuerySet(
                endpoint=OAIREEndpoint.RESEARCHPRODUCTS, client=client
            )
            queryset.add(queries)
            queryset.store_results(db)
            counter = 0
            queries = []
            print(f"Processed {processed} DOIs")
            queries = []


print(f"done -- Processed {processed} DOIs")
