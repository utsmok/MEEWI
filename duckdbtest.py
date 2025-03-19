
from rich import print
import duckdb
import httpx
from typing import Dict, List, Any, Optional, Tuple, Union
import json

def fetch_openalex_data(work_id: str = "W4402690901", per_page: int = 50) -> None:
    """
    Fetch paginated data from OpenAlex API and store it in DuckDB.
    
    Args:
        work_id: The OpenAlex work ID to fetch citations for
        per_page: Number of items per page
    """
    # Initialize DuckDB connection
    conn = duckdb.connect(database='duck.db')
    
    # Enable httpfs extension
    conn.execute("INSTALL httpfs;")
    conn.execute("LOAD httpfs;")
    
    # Create the table to store our data
    conn.execute("DROP TABLE IF EXISTS openalex_data;")
    
    # Get first page to determine the total count and establish schema
    first_page_url = f"https://api.openalex.org/works?filter=cites:{work_id}&page=1&per-page=1"
    response = httpx.get(first_page_url)
    data = response.json()
    
    # Get total count
    total_count = data['meta']['count']
    total_pages = (total_count + per_page - 1) // per_page  # Ceiling division
    
    print(f"Total items: {total_count}, Total pages: {total_pages}")
    
    # Create table with the right schema by inserting the first item
    conn.execute(f"""
    CREATE TABLE openalex_data AS
    SELECT * FROM read_json_auto('{first_page_url}', ignore_errors=true);
    """)
    
    # Then truncate it to start fresh
    conn.execute("DELETE FROM openalex_data;")
    
    # Now fetch all pages and insert them one by one
    for page in range(1, total_pages + 1):
        page_url = f"https://api.openalex.org/works?filter=cites:{work_id}&page={page}&per-page={per_page}"
        print(f"Fetching page {page}/{total_pages}: {page_url}")
        if True:
          results = httpx.get(page_url).json().get('results')
          # Pull data directly into DuckDB
          print(results)
          conn.execute(f"""
          INSERT INTO openalex_data
          SELECT * FROM read_json_auto('{results}', ignore_errors=true);
          """)

    
    # Verify the number of rows
    result = conn.execute("SELECT COUNT(*) FROM openalex_data;").fetchone()
    print(f"Total rows inserted: {result[0]}")
    
    # Export to parquet if needed
    conn.execute("COPY openalex_data TO 'openalex_data.parquet' (FORMAT PARQUET);")
    print("Data exported to openalex_data.parquet")
    
    # Return the connection for further use
    return conn

if __name__ == "__main__":
    conn = fetch_openalex_data()
    # Optional: Continue with analysis
    # Example: print the top 5 rows of results
    print(conn.execute("SELECT results FROM openalex_data LIMIT 5;").fetchall())
