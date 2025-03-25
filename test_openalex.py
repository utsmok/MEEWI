import httpx

from db.duckdb import DuckDBInstance
from retrieval.openalex.mappings import OAEndpoint
from retrieval.openalex.queries import OAFilter, OAQuery, OAWorksSet


def get_all_ut_works(client: httpx.Client, db: DuckDBInstance):
    OAWorksSet().add(
        OAQuery(
            endpoint=OAEndpoint.WORKS,
            per_page=50,
            filters=[
                OAFilter(
                    filter_type="institutions.ror",
                    filter_value="https://ror.org/006hf6230",
                ),
            ],
            email="samopsa@gmail.com",
            client=client,
        )
    ).store_results(db)


db = DuckDBInstance()
get_all_ut_works(httpx.Client(), db)
