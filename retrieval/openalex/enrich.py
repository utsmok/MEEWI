"""
Contains classes that enriches existing data stored in a 'DB' instance with additional data from OpenAlex.

"""
from collections import defaultdict
from ..base_classes import BaseEnricher, BaseQuery, BaseQuerySet
from db.duckdb import DuckDBInstance
from dataclasses import dataclass, field
from .queries import OAQuery, OAQuerySet
from .mappings import OAEndpoint, ID_TO_ENDPOINT
from rich import print

@dataclass
class OAEnricher(BaseEnricher):
    """
    Class that has methods to create querysets to enrich existing data in a DuckDB instance with additional data from OpenAlex.
    """

    db: DuckDBInstance
    querysets: dict[OAEndpoint, OAQuerySet] = field(default_factory=dict, init=False)


    def retrieve_related_items(self, table_name:str) -> None:
        """
        For a given table name in the DuckDB instance,
        retrieve all fields in the table that hold an OpenAlex id.

        Use the mapping of table name to id fields to determine which fields to retrieve from the db.


        Then, for each found itemtype, create a queryset to retrieve all those items from OpenAlex.
        """
        gathered_ids = set()
        with self.db.conn as conn:
            match table_name:
                case "work":
                    print(f'Enriching works by retrieving related items.')

                    row = conn.execute("""
                    WITH l as (
                    SELECT UNNEST(
                        locations,
                        recursive := true
                    )
                    FROM "work"
                    )

                    SELECT array_agg(DISTINCT id) AS unique_source_ids, array_agg(DISTINCT host_organization) AS unique_host_organizations
                    FROM l
                    """).fetchone()
                    gathered_ids.update(row[0] or [])
                    gathered_ids.update(row[1] or [])
                    # TODO: go through the gathered ids and match them with the appropriate endpoint based on the start of the id (e.g. S for source, P for publisher, I for institution, etc)

                    row = conn.execute("""
                    WITH a as (
                        SELECT UNNEST(
                            authorships,
                            recursive := true
                        )
                        FROM "work"
                    )
                    SELECT array_agg(DISTINCT id) AS unique_author_ids
                    FROM a
                    """).fetchone()
                    gathered_ids.update(row[0] or [])
                    print(row[0][0])

                    row =conn.execute("""
                    WITH f as (
                        SELECT UNNEST(
                            grants,
                            recursive := true
                        )
                        FROM "work"
                    )
                    SELECT array_agg(DISTINCT funder) AS unique_funder_ids
                    FROM f
                    """).fetchone()
                    gathered_ids.update(row[0] or [])
                    print(row[0][0])

                    row = conn.execute("""
                    WITH t as (
                        SELECT UNNEST(
                            topics,
                            recursive := true
                        )
                        FROM "work"
                    )
                    SELECT array_agg(DISTINCT id) AS unique_topic_ids
                    from t
                    """).fetchone()
                    gathered_ids.update(row[0] or [])
                    print(row[0][0])

                    row = conn.execute("""
                    SELECT DISTINCT UNNEST(
                        datasets,
                        recursive := true
                    ) as id
                    FROM "work"
                    """).fetchall()
                    print(row[0][0])
                    gathered_ids.update([r[0] for r in row])

                    row = conn.execute("""
                    SELECT DISTINCT UNNEST(
                        versions,
                        recursive := true
                    ) as id
                    FROM "work"
                    """).fetchall()
                    print(row[0][0])
                    gathered_ids.update([r[0] for r in row])
                case _:
                    print(f'Only works are supported for now.')
                    ...

            print(f"done gathering {len(gathered_ids)} ids.")
            gathered_ids = {i for i in gathered_ids if i}
            print(f'ids remaining after removing empty strings: {len(gathered_ids)}')
            # group the ids by endpoint by using their id prefix
            ids_grouped = defaultdict(set)
            [ids_grouped[ID_TO_ENDPOINT[str(id)[0:22]]].add(id) for id in gathered_ids]
            print(f"grouped per endpoint:")
            for endpoint, ids in ids_grouped.items():
                print(f"{endpoint.value}: {len(ids)}")
            # substract ids already in the table per endpoint
            # create a queryset for each endpoint if there are ids to retrieve
            # then run them
            for endpoint in ids_grouped.keys():
                tablename = endpoint.value.rstrip("s")
                existing_ids = self.db.retrieve_ids(tablename)
                ids_grouped[endpoint] -= existing_ids
                if ids_grouped[endpoint]:
                    print(f'retrieving {len(ids_grouped[endpoint])} new ids for {endpoint.value}')

                    self.querysets[endpoint] = OAQuerySet(endpoint=endpoint).add_id_batch(ids_grouped[endpoint], "openalex_id")
                    self.querysets[endpoint].store_results(self.db)
                else:
                    print(f'no new ids to retrieve for {endpoint.value}')




