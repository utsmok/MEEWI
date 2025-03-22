import httpx

from db.duckdb import DuckDBInstance
from retrieval.openalex.enrich import OAEnricher
from retrieval.openalex.mappings import OAEndpoint
from retrieval.openalex.queries import OAFilter, OAQuery, OAQuerySet, OAWorksSet

BATCH_SIZE = 50


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


if __name__ == "__main__":
    # data = pl.read_csv("mor_items.csv")
    # dois = data["DOI"].to_list()
    # print(len(dois))
    db = DuckDBInstance()

    with httpx.Client() as client:
        enricher = OAEnricher(db)
        enricher.retrieve_related_items("work")
        if False:
            OAQuerySet(endpoint=OAEndpoint.AUTHORS).add(
                OAQuery(
                    endpoint=OAEndpoint.AUTHORS,
                    per_page=50,
                    filters=[
                        OAFilter(
                            filter_type="openalex_id",
                            filter_value="https://openalex.org/A5077771918",
                        ),
                    ],
                    email="samopsa@gmail.com",
                    client=client,
                )
            ).store_results(db)
            OAQuerySet(endpoint=OAEndpoint.SOURCES).add(
                OAQuery(
                    endpoint=OAEndpoint.SOURCES,
                    per_page=50,
                    filters=[
                        OAFilter(
                            filter_type="openalex_id",
                            filter_value="https://openalex.org/S173256270",
                        ),
                    ],
                    email="samopsa@gmail.com",
                    client=client,
                )
            ).store_results(db)
            OAQuerySet(endpoint=OAEndpoint.INSTITUTIONS).add(
                OAQuery(
                    endpoint=OAEndpoint.INSTITUTIONS,
                    per_page=50,
                    filters=[
                        OAFilter(
                            filter_type="openalex_id",
                            filter_value="https://openalex.org/I865915315",
                        ),
                    ],
                    email="samopsa@gmail.com",
                    client=client,
                )
            ).store_results(db)
            OAQuerySet(endpoint=OAEndpoint.TOPICS).add(
                OAQuery(
                    endpoint=OAEndpoint.TOPICS,
                    per_page=50,
                    filters=[
                        OAFilter(
                            filter_type="id",
                            filter_value="https://openalex.org/T10551",
                        ),
                    ],
                    email="samopsa@gmail.com",
                    client=client,
                )
            ).store_results(db)
            OAQuerySet(endpoint=OAEndpoint.PUBLISHERS).add(
                OAQuery(
                    endpoint=OAEndpoint.PUBLISHERS,
                    per_page=50,
                    filters=[
                        OAFilter(
                            filter_type="openalex_id",
                            filter_value="https://openalex.org/P4310320990",
                        ),
                    ],
                    email="samopsa@gmail.com",
                    client=client,
                )
            ).store_results(db)
            get_all_ut_works(client, db)
