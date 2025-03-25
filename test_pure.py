import httpx

from db.duckdb import DuckDBInstance
from retrieval.pure.queries import PureEndpoint, PureRetriever


def rec_print(el, indent=0):
    """
    Recursively prints  XML tree structure with indentation.
    el - XML element to print
    """
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


db = DuckDBInstance()

with httpx.Client() as client:
    retriever = PureRetriever(PureEndpoint.PUBLICATIONS, client)
    retriever.get_and_store_data(db)
