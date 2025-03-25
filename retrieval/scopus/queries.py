import httpx
from rich import print


def scopus_query():

    url ="https://api.elsevier.com/content/search/scopus"
    API_KEY = ""
    with open(r"C:\dev\MEEWI\retrieval\scopus\scopus_auth.secret") as f:
        API_KEY = f.read().strip()
    header= {
        "X-ELS-APIKey": API_KEY,
        "Accept": "application/json"
        }
    params = {
            'query':'AFFIL ( "University of Twente" )',
            'cursor':'*',
            'view':'COMPLETE',
        }

    client = httpx.Client()
    client.headers.update(header)

    r = client.get(url, headers=header, params=params)
    print(r.json())