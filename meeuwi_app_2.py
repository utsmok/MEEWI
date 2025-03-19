import marimo

__generated_with = "0.11.20"
app = marimo.App(width="full")


@app.cell
def _():
    # Imports
    import marimo as mo
    import httpx
    import polars as pl
    return httpx, mo, pl


@app.cell(hide_code=True)
def _():
    # Functions
    return


@app.cell
def _():
    # init items

    stored_list = []
    return (stored_list,)


@app.cell
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


@app.cell
def _(mo, search_results, stored_list):
    def remove_stored_items(items):
        if not isinstance(items, list):
            items = [items]
        if not items:
            return
        if items and stored_list:
            remove_ids = [i.get("id") for i in items]
            for item in stored_list.copy():
                if item.get("id") in remove_ids:
                    stored_list.remove(item)

        stored_items_table = mo.ui.table(
            stored_list,
            label="Selected entities",
            pagination=False,
            selection="multi",
            show_column_summaries=False,
            show_download=False
        )


    if isinstance(search_results.value, list):
        selected_items = [
            selected_result_item
            for selected_result_item in search_results.value
        ]
    if selected_items:
        stored_ids = [i.get("id") for i in stored_list]
        for selected_item in selected_items:
            if selected_item.get("id") not in stored_ids:
                stored_list.append(selected_item)
                stored_ids.append(selected_item.get("id"))


    stored_items_table = mo.ui.table(
        stored_list,
        label="Selected entities",
        pagination=False,
        selection="multi",
        show_column_summaries=False,
        show_download=False
    )
    return (
        remove_stored_items,
        selected_item,
        selected_items,
        stored_ids,
        stored_items_table,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# UI""")
    return


@app.cell
def _(mo):
    settings = mo.vstack(
        [
            mo.md("Edit User"),
            first := mo.ui.text(label="First Name"),
            last := mo.ui.text(label="Last Name"),
        ]
    )

    organization = mo.vstack(
        [
            mo.md("Edit Organization"),
            org := mo.ui.text(label="Organization Name", value="..."),
            employees := mo.ui.number(
                label="Number of Employees", start=0, stop=1000
            ),
        ]
    )

    mo.ui.tabs(
        {
            "🧙‍♀ User": settings,
            "🏢 Organization": organization,
        }
    )

    return employees, first, last, org, organization, settings


@app.cell
def _(employees, first, last, mo, org):
    mo.md(
        f"""
        Welcome **{first.value} {last.value}** to **{org.value}**! You are 
        employee no. **{employees.value + 1}**.

        #{"🎉" * (min(employees.value + 1, 1000))} 
        """
    ) if all([first.value, last.value, org.value]) else mo.md(
        "Type a first and last name!"
    )
    return


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    # Search input
    autocomplete_input = mo.ui.text(label="Search for: *(doi, title, name, ...)*")
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
        label="Entity type: *(optional)*",
        allow_select_none=True,
        value="All",
    )


    search_input_element = mo.vstack(
        [
            mo.md("## Search input"),
            autocomplete_input,
            entity_dropdown,
        ]
    )
    mo.vstack([
    mo.md("""
    # Add items

    Enter your search strings in the field below to search the OpenAlex database for various `entity types` (`works`, `authors`, `institutions`, *etc*) using any search term of your choice (`name`, `doi`, `orcid`, `topic`, `keyword`, *etc*). Selecting an `entity type` is optional but narrows down the search results.
    The first 10 results of the query will be shown in the table. Select your desired results there by selecting them.

    You can run as many queries as you want to expand the list. Once done, press 'retrieve' below the list of selected items to retrieve the full data for those items.
    """),
    search_input_element])
    return autocomplete_input, entity_dropdown, search_input_element


@app.cell(hide_code=True)
async def _(
    autocomplete_input,
    entity_dropdown,
    get_from_autocomplete,
    httpx,
    mo,
):
    # Results table (center element)

    async with httpx.AsyncClient() as client:
        new_count, result = await get_from_autocomplete(
            autocomplete_input.value, client, entity_dropdown.value
        )
        if new_count > 0:
            search_results = mo.ui.table(result, pagination=False, selection="multi", show_download=False)
        else:
            search_results = mo.ui.table([], show_download=False)

    if not autocomplete_input.value:
        query_detail = "### No query entered."
    else:
        query_detail = f"### Query: {autocomplete_input.value}"
        if entity_dropdown.value:
            query_detail += f" | filtered to entity type: {entity_dropdown.value}"
    

    return client, new_count, query_detail, result, search_results


@app.cell
def _(mo, query_detail, search_results):
    mo.vstack([
        mo.md("# Query results (max 10)"),
        mo.md(query_detail), 
        search_results
    ])
    

    return


@app.cell
def _(mo, remove_button, retrieve_button, stored_items_table):
    mo.vstack([
            mo.md("# Selected items"),
            stored_items_table, 
            mo.hstack([
                remove_button, 
                retrieve_button
            ], justify="start")
        ])
    return


@app.cell
def _(search_results, stored_items_table, stored_list):
    print(stored_list)
    print(len(stored_list))
    print(stored_items_table.value)
    print(len(stored_items_table.value))
    print(search_results.value)
    print(len(search_results.value))
    return


@app.cell
def _(mo, remove_stored_items, stored_items_table):
    remove_button = mo.ui.button(
        label="Remove selected",
        kind="danger",
        on_click=remove_stored_items(stored_items_table.value),
    )
    retrieve_button = mo.ui.button(
        label="Retrieve selected",
        kind="success",
    )
    return remove_button, retrieve_button


if __name__ == "__main__":
    app.run()
