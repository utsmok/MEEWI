import marimo

__generated_with = "0.11.20"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _():
    import marimo as mo
    import httpx
    import polars as pl
    return httpx, mo, pl


@app.cell(hide_code=True)
def _(httpx, pl):
    async def get_from_autocomplete(
        input_str: str, client: httpx.AsyncClient, entity_type: str | None = None
    ) -> tuple[int, pl.DataFrame]:
        """
        use the OA autocomplete endpoint to get suggestions for a search string.
        """

        if entity_type not in [
            "works",
            "authors",
            "sources",
            "institutions",
            "concepts",
            "publishers",
            "funders",
        ]:
            entity_type = None
        if not input_str:
            return 0, pl.DataFrame()

        url = "https://api.openalex.org/autocomplete"

        url += f"/{entity_type}?q={input_str}" if entity_type else f"?q={input_str}"
        url += "&mailto=s.mok@utwente.nl"
        response = await client.get(url)
        data = response.json()
        count = data.get("meta", {}).get("count")
        results = data.get("results", [])

        return count, results
    return (get_from_autocomplete,)


@app.cell(hide_code=True)
async def _(
    autocomplete_input,
    entity_dropdown,
    get_from_autocomplete,
    httpx,
    mo,
):
    async with httpx.AsyncClient() as client:
        new_count, result = await get_from_autocomplete(
            autocomplete_input.value, client, entity_dropdown.value
        )
        if new_count > 0:
            autocomple_result_table = mo.ui.table(result, pagination=False, selection="multi")
            search_results = mo.vstack(
                [
                    mo.md(
                        f"## `{new_count}` results found for query: `{autocomplete_input.value}` with entity type `{entity_dropdown.value}`"
                    ),
                    mo.md(f"### first `{min(new_count, 10)}` shown below."),
                    autocomple_result_table,
                ]
            )
        else:
            search_results = mo.md(
                f"## No results found for query: `{autocomplete_input.value or '---'} ` with entity type `{entity_dropdown.value or '---'} ` "
            )
    return autocomple_result_table, client, new_count, result, search_results


@app.cell(hide_code=True)
def _(mo):
    mo.output.append(
        mo.md("""
    # Quick search

    Use the input field below to do a quick search for articles, authors, institutions, publishers, funders, journals, book series, topics, fields of study, ... etc. 

    It will show you the 10 most relevant results. If you want to add any to your overall query, select them and press 'add' to retrieve the full data.

    To achieve better results, you can also select a specific entity type to search for using the dropdown menu.

    *`Search term:`*
    """)
    )
    autocomplete_input = mo.ui.text(full_width=True)
    entity_dropdown = mo.ui.dropdown(
        options=[
            "All",
            "works",
            "authors",
            "sources",
            "institutions",
            "concepts",
            "publishers",
            "funders",
        ],
        label="Entity type to search for:",
        allow_select_none=True,
        value="All",
    )
    mo.output.append(autocomplete_input)
    mo.output.append(entity_dropdown)
    return autocomplete_input, entity_dropdown


@app.cell
def _(search_results):
    search_results
    return


if __name__ == "__main__":
    app.run()
