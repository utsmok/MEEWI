from pathlib import Path

import httpx
from lxml import etree
from rich import print

from db.duckdb import DuckDBInstance
from retrieval.openalex.mappings import OAEndpoint
from retrieval.openalex.queries import OAFilter, OAQuery, OAWorksSet
from retrieval.pure.models.publications import Publication
from retrieval.pure.queries import PureEndpoint, PureRetriever

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


def rec_print(el, indent=0):
    gap = str(indent) if indent else ""
    indentation = " " * ((indent * 2) - 1) if indent > 0 else ""
    gap += indentation
    try:
        tag = el.tag.replace("{http://www.loc.gov/mods/v3}", "")
        if indent > 0:
            print(f"{gap}└─{tag}")
        else:
            print(f"{gap}{tag}")
        if el.text:
            if indent > 0:
                print(f"{gap}  └─'{el.text}'")
            else:
                print(f"{gap}└─'{el.text}'")
    except Exception:
        ...
    try:
        h = 0
        for child in el.iterchildren():
            h = h + 1
            rec_print(child, indent + 1)
    except Exception:
        ...
    if indent == 0 and h == 0 and not el.text:
        print("└─(NULL)")


if __name__ == "__main__":
    db = DuckDBInstance()

    with httpx.Client() as client:
        retriever = PureRetriever(PureEndpoint.PUBLICATIONS, client)
        retriever.get_and_store_data(db)

    if False:
        with Path("pure_data_example.xml").open("rb") as f:
            parsed: etree._ElementTree = etree.parse(f)

        i = 0
        for el in parsed.getroot().iterchildren():
            print("\n")
            print(f"Record {i}")
            print(" =============================================")
            i += 1
            print(list(el.iterchildren()))
            try:
                for item in el.iterchildren():
                    try:
                        print(list(item.iterchildren()))
                        print(
                            Publication().from_xml_tree(item).model_dump_json(indent=2)
                        )
                    except Exception as e:
                        print(
                            f"Error while parsing xml tree to Publication instance: {e}"
                        )

                    # rec_print(item)
            except Exception as e:
                print(f"error {e}")
