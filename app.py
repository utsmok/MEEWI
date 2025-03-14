"""
This marimo app will serve as the frontend for this application, using the functionality of the modules in the package.
"""

import marimo

__generated_with = "0.11.19"
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
    return Callable, mo, pl


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
def _(Callable, form, get_data, get_validator, mo):
    # parse, normalize, validate input
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

    results = get_data(input_data)

    return (
        doi_path,
        entries,
        final_stack,
        input_data,
        k,
        results,
        stack,
        v,
        validator,
    )


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
        input: list[tuple[str|Identifier, str]] = []
        for k,v in form_values.items():
            if all([v, not isinstance(v, Exception)]):
                input.append((k,v))
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


@app.cell(column=2, hide_code=True)
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
        - [ ] Finish validation functions

        ## Retrieval
        - [ ] Start working on retrieval functionality

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


if __name__ == "__main__":
    app.run()
