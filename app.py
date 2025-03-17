"""
This marimo app will serve as the frontend for this application, using the functionality of the modules in the package.
"""

import marimo

__generated_with = "0.11.20"
app = marimo.App(width="columns", app_title="Meeuwi")


@app.cell(column=0, hide_code=True)
def _(mo):
    mo.md(
        """
        # Code

        This column contains the app code: handling logic, creating ui elements, etc.

        Each section has a header that can be collapsed to keep things from being cluttered.
        """
    ).callout("info")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# Init""")
    return


@app.cell
def _():
    # base libs
    import marimo as mo
    import polars as pl
    from collections.abc import Callable
    import httpx
    return Callable, httpx, mo, pl


@app.cell
def _():
    # set up internal modules
    from models.validate import (
        validate_doi,
        validate_isbn,
        validate_scopus_id,
        validate_openaire_id,
        validate_pmid,
        validate_arxiv_id,
        validate_pure_id,
        validate_patent_number,
        validate_orcid,
        get_validator,
    )
    return (
        get_validator,
        validate_arxiv_id,
        validate_doi,
        validate_isbn,
        validate_openaire_id,
        validate_orcid,
        validate_patent_number,
        validate_pmid,
        validate_pure_id,
        validate_scopus_id,
    )


@app.cell
def _():
    from retrieve import Retriever
    from models.enums import Identifier
    return Identifier, Retriever


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# User input""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## UI elements""")
    return


@app.cell(hide_code=True)
def _(mo):
    form = (
        mo.md("""

        # Search for publications

        Enter your search term(s) into the field(s) to find a publication, then press the button to submit.

        The app will parse and validate your input, and it will let you know if there are any errors in the input. It can handle quite a lot of different formats, so don't worry about formatting the input too much. 

        The parsed input will be displayed below the search form for you to review and adjust.

        **by unique identifier**

        - {doi}
        - {isbn}
        - {scopus_id}
        - {openaire_id}
        - {pmid}
        - {arxiv_id}

        - {pure_id}
        - {patent_number}
        - {orcid}

        **by searching for names**

        - {title}
        - {author_name}
        - {journal_name}
        - {publisher_name}

    """)
        .batch(
            doi=mo.ui.text(label="DOI", placeholder="10.xxxx/xxxx"),
            isbn=mo.ui.text(label="ISBN", placeholder="978-3-16-148410-0"),
            scopus_id=mo.ui.text(label="Scopus ID"),
            openaire_id=mo.ui.text(label="Openaire ID"),
            orcid=mo.ui.text(label="ORCID"),
            patent_number=mo.ui.text(label="Patent Number"),
            pure_id=mo.ui.text(label="Pure ID"),
            pmid=mo.ui.text(label="PMID"),
            arxiv_id=mo.ui.text(label="Arxiv ID"),
            title=mo.ui.text(label="Title"),
            author_name=mo.ui.text(label="Author Name"),
            journal_name=mo.ui.text(label="Journal Name"),
            publisher_name=mo.ui.text(label="Publisher Name"),
        )
        .form(show_clear_button=True, submit_button_label="Search")
    )
    return (form,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Logic""")
    return


@app.cell(hide_code=True)
def _(Callable, form, get_validator, mo):
    # Parse, normalize and validate user input
    # then display it for review
    final_stack = ""

    stack = [mo.md("# Parsed search input"), mo.md("---")]
    input_data = {}
    if form.value:
        input_data = {k: v for k, v in form.value.items() if v}

    if input_data:
        entries = 0
        for k, v in input_data.items():
            if not v:
                input_data[k] = ""
                continue
            entries += 1
            validator: Callable[[str], str] = get_validator(k)
            if not validator:
                continue
            try:
                input_data[k] = validator(v)
            except Exception as e:
                input_data[k] = e

        if input_data.get("doi") and input_data.get("doi") != "":
            entries -= 1
            doi_path = "https://doi.org/"
            if isinstance(input_data["doi"], Exception):
                doi_path = ""

            stack.append(
                mo.hstack(
                    [
                        mo.md(f"**DOI**"),
                        mo.md(f"{doi_path}{input_data['doi']}"),
                    ],
                    justify="center",
                    widths=[1, 2],
                )
            )
        if entries:
            stack.extend(
                [
                    mo.hstack(
                        [
                            mo.md(f"**{k.replace('_', ' ').capitalize()}**"),
                            mo.md(f"{v}"),
                        ],
                        justify="center",
                        widths=[1, 2],
                    )
                    for k, v in input_data.items()
                    if all([v, k != "doi"])
                ]
            )

    if len(stack) == 2:
        stack.append(mo.md("No input received."))
    final_stack = mo.vstack(stack)
    return doi_path, entries, final_stack, input_data, k, stack, v, validator


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# Retrieval""")
    return


@app.cell
def _(Identifier, Retriever):
    def get_data(form_values: dict) -> dict[str, dict]:
        """
        For a given list of input from the input form, retrieve metadata from applicable sources and return .
        """

        # 1. Get the search terms from the input dict. These should already be normalized and validated.
        # 2. Run each through the pipeline of retrieval functions that handle selecting the correct source and retrieving the metadata.
        # 3. Construct the return dict with the source as the key and the metadata as the value.

        # parse the input
        input: list[tuple[str | Identifier, str]] = []
        for k, v in form_values.items():
            if all([v, not isinstance(v, Exception)]):
                input.append((k, v))
        if not input:
            return {}
        retriever = Retriever()
        retriever.add_id(input)
        return retriever.retrieve()
    return (get_data,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# Parsing""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# Exporting""")
    return


@app.cell(column=1, hide_code=True)
def _(mo):
    mo.md(
        """
        # UI

        This column contains all user interface elements, like forms, buttons, text output, etc.
        """
    ).callout("success")
    return


@app.cell(hide_code=True)
def _(form):
    form
    return


@app.cell(hide_code=True)
def _(final_stack):
    final_stack
    return


@app.cell(hide_code=True)
def _(mo):
    def dict_to_markdown(input_data) -> list[mo.Html]:
        icon = "::hugeicons:pin-02::"
        color_mapping = {
            1: "CornflowerBlue",
            2: "DarkOrange",
            3: "DarkOrchid",
            4: "HotPink",
            5: "SteelBlue",
            6: "GoldenRod",
        }

        def parse_list(input_list, indent=1) -> list:
            markd = []
            color = color_mapping[indent + 1]
            headgap = f"{icon * indent * 2}"
            gap = f"{icon * (indent + 1) * 2}"
            for item in input_list:
                if isinstance(item, dict):
                    markd.extend(parse_dict(item, indent=indent + 1))
                elif isinstance(item, list):
                    markd.extend(parse_list(item, indent=indent + 1))
                else:
                    markd.append(mo.md(f" {gap}{item}"))
            return markd

        def parse_dict(input_dict, indent=1) -> list:
            markd = []
            color = color_mapping[indent + 1]
            headgap = f"{icon * indent * 2}"
            gap = f"{icon * (indent + 1) * 2}"
            for key, value in input_dict.items():
                markd.append(mo.md(f'<span style="color:{color}"> {headgap}{key} </span>'))
                if isinstance(value, dict):
                    markd.extend(parse_dict(value, indent=indent + 1))
                elif isinstance(value, list):
                    markd.extend(parse_list(value, indent=indent + 1))
                else:
                    markd.append(mo.md(f" {gap}{value}"))
            return markd

        print_data = []
        for input_id, data_source in input_data.items():
            print_data.append(mo.md(f"# Data retrieved for {input_id}"))
            if not data_source:
                continue
            for source, itemlist in data_source.items():
                print_data.append(mo.md(f"## from {source}"))
                if not isinstance(itemlist, list):
                    itemlist = [itemlist]
                for data in itemlist:
                    for key, value in data.items():
                        if "abstract" in key:
                            continue
                        indent = 1
                        color = color_mapping[indent]
                        headgap = f"{icon}"
                        gap = f"{icon * 2}"
                        if isinstance(value, dict):
                            print_data.extend(parse_dict(value, indent))
                        elif isinstance(value, list):
                            print_data.extend(parse_list(value, indent))
                        else:
                            print_data.append(
                                mo.md(f'<span style="color:{color}"> {headgap}{key} </span>')
                            )
                            print_data.append(mo.md(f"{gap}{value}"))

        return print_data


    printlist = [
        mo.md(f"""
        # Results   
        ---
    """)
    ]
    # results = get_data(input_data)
    # printlist.extend(dict_to_markdown(results))

    # mo.vstack(printlist)
    return dict_to_markdown, printlist


@app.cell(column=2)
def _(mo):
    mo.md(
        r"""
        # Reference & Misc

        This column contains additional things for dev use, like a todo list, docs, experiments, etc.
        """
    ).callout("warn")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        # To do list

        ## Input
        - [x] Finish validation functions for identifiers
        - [ ] create other validation functions & datamodels?

        ## Retrieval
        - [x] Start working on retrieval functionality
        - [ ] finish openalex retriever
        - [ ] start working on other retrievers

        ## Parsing

        - [ ] ...

        ## Exporting

        - [ ] ...
        """
    )
    return


@app.cell
def _():
    return


@app.cell(column=3)
def _(mo):
    mo.md(
        r"""
        # Autocomplete

        This column contains (test?) cells using the openalex autocomplete endpoint.
        """
    ).callout("danger")
    return


@app.cell
async def _(autocomplete_input, entity_dropdown, httpx, mo, pl):
    async def get_from_autocomplete(input_str:str, client:httpx.AsyncClient, entity_type: str | None = None) -> tuple[int, pl.DataFrame]:
        """
        use the OA autocomplete endpoint to get suggestions for a search string.
        """

        if entity_type not in ["works", "authors", "sources", "institutions", "concepts", "publishers", "funders"]:
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


    async with httpx.AsyncClient() as client:
        new_count, result = await get_from_autocomplete(autocomplete_input.value, client, entity_dropdown.value)
        if new_count > 0:
            autocomple_result_table = mo.ui.table(result,
                                                 pagination=False, selection='multi')
            search_results = mo.vstack([
                    mo.md(f"## `{new_count}` results found for query: `{autocomplete_input.value}` with entity type `{entity_dropdown.value}`"),
                    mo.md(f"### first `{min(new_count, 10)}` shown below."),
                autocomple_result_table
                
            ])
        else:
            search_results = mo.md(f"## No results found for query: `{autocomplete_input.value or '---'} ` with entity type `{entity_dropdown.value or '---'} ` ")
    
    

    return (
        autocomple_result_table,
        client,
        get_from_autocomplete,
        new_count,
        result,
        search_results,
    )


@app.cell
def _(mo):
    mo.output.append(mo.md("""
    # Quick search

    Use the input field below to do a quick search for articles, authors, institutions, publishers, funders, journals, book series.... etc. 

    It will show you the 10 most relevant results. If you want to add any to your overall query, select them and press 'add' to retrieve the full data.

    To achieve better results, you can also select a specific entity type to search for using the dropdown menu.

    *`Search term:`*
    """))
    autocomplete_input = mo.ui.text(full_width=True)
    entity_dropdown = mo.ui.dropdown(
        options=["All", "works", "authors", "sources", "institutions", "concepts", "publishers", "funders"],
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


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
