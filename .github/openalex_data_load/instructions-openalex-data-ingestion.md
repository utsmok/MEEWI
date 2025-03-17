
# Instructions on loading data into postgres 13+

Overall steps:

1. Setup: Create tables from the schema `openalex-pg-schema.sql`
2. For each type of file, convert the received entries from nested json to flattened separated form; in this example stored as csvs
3. Load the (csv) data into to the tables

## Step 1: Create the schema

`openalex-pg-schema.sql` is a schema that should work for postgres 13+


## Step 2: Flatten json

python script `flatten-openalex-jsonl.py` will turn data stored in JSON lines format into CSV files that fit the schema from step 1.

The script assumes all data is stored as jsonl files, separate files for separate entities. In this app, we will retrieve data from an api as a list of dicts and parse those. We know the entity type of each list of results.

The script stores it output as flat csvs in a subdir as shown below. In this app, hold data in mem and ingest it into the DB straight away.

```
$ tree csv-files/
csv-files/
├── concepts.csv
├── concepts_ancestors.csv
├── concepts_counts_by_year.csv
├── concepts_ids.csv
└── concepts_related_concepts.csv
...
$ cat csv-files/concepts_related_concepts.csv
concept_id,related_concept_id,score
https://openalex.org/C41008148,https://openalex.org/C33923547,253.92
https://openalex.org/C41008148,https://openalex.org/C119599485,153.019
https://openalex.org/C41008148,https://openalex.org/C121332964,143.935
...
```

## Step 3: Load the CSV files to the database

if we created csv files, we can use postgres copy commands to load them into the db, e.g.
```
\copy openalex.concepts_ancestors (concept_id, ancestor_id) from csv-files/concepts_ancestors.csv csv header
```

`copy-openalex-csv.sql` contains all copy commands in a single file.
Use like so:

1. Copy it to the same place as the python script from step 2, right above the folder with your CSV files.
2. Set the environment variable OPENALEX\_SNAPSHOT\_DB to the [connection URI](https://www.postgresql.org/docs/13/libpq-connect.html#LIBPQ-CONNSTRING) for your database.
3. If your CSV files aren't in `csv-files`, replace each occurence of 'csv-files/' in the script with the correct path.
4. Run it like this (from your shell prompt)

```
psql $OPENALEX_SNAPSHOT_DB < copy-openalex-csv.sql
```

or from psql directly:

```
\i copy-openalex-csv.sql
```
