import httpx
from rich import print

from db.duckdb import DuckDBInstance
from retrieval.openalex.models import Institution
from retrieval.openalex.queries import OAFilter, OAQuery, OAQuerySet, OAWorksSet
from retrieval.openalex.utils import Endpoint
from utils.create_ddl import generate_ddl

BATCH_SIZE = 50


def get_all_ut_works(client: httpx.Client, db: DuckDBInstance):
    queryset = OAWorksSet()

    queryset.add(
        OAQuery(
            endpoint=Endpoint.WORKS,
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
    )

    queryset.store_results(db)


if __name__ == "__main__":
    # data = pl.read_csv("mor_items.csv")
    # dois = data["DOI"].to_list()
    # print(len(dois))
    db = DuckDBInstance()
    print(generate_ddl(Institution, table_name="institutions"))
    with httpx.Client() as client:
        OAQuerySet(endpoint=Endpoint.AUTHORS).add(
            OAQuery(
                endpoint=Endpoint.AUTHORS,
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
        OAQuerySet(endpoint=Endpoint.SOURCES).add(
            OAQuery(
                endpoint=Endpoint.SOURCES,
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
        OAQuerySet(endpoint=Endpoint.INSTITUTIONS).add(
            OAQuery(
                endpoint=Endpoint.INSTITUTIONS,
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
        OAQuerySet(endpoint=Endpoint.TOPICS).add(
            OAQuery(
                endpoint=Endpoint.TOPICS,
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
        OAQuerySet(endpoint=Endpoint.PUBLISHERS).add(
            OAQuery(
                endpoint=Endpoint.PUBLISHERS,
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
        # OAWorksSet().add_id_batch(dois, id_type="doi").store_results(db)
        # get_all_ut_works(client, db)
