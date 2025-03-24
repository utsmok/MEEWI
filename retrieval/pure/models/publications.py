import traceback
from typing import Any

import xmltodict
from pydantic import BaseModel, Field, model_validator
from rich import print


class Source(BaseModel):
    issue: str | None = None
    title: str | None = None
    publisher: str | None = None
    issn: list[str] = Field(default_factory=list)

    @model_validator(mode="before")
    @classmethod
    def replace_none_with_empty(cls, data) -> dict | Any:
        """Ensure data is a dict and issn is a list"""
        if not isinstance(data, dict):
            return {}

        if not data.get("issn"):
            data["issn"] = []
        elif isinstance(data.get("issn"), str):
            data["issn"] = [data["issn"]]

        return data

    class Config:
        frozen = True


class File(BaseModel):
    title: str | None = None
    location: str | None = None
    visibility: str | None = None
    access: str | None = None

    class Config:
        frozen = True


class Organization(BaseModel):
    type: str | None = None
    name: str | None = None
    uuid: str | None = None
    scopus: list[str] = Field(default_factory=list)  # Changed to required with default
    scopus_id: list[str] = Field(default_factory=list)  # Added this field

    @model_validator(mode="before")
    @classmethod
    def replace_none_with_empty(cls, data) -> dict | Any:
        """Handle scopus fields and ensure valid dict"""
        if not isinstance(data, dict):
            return {}

        # Handle scopus field
        if not data.get("scopus"):
            data["scopus"] = []
        elif isinstance(data.get("scopus"), str):
            data["scopus"] = [data["scopus"]]

        # Handle scopus_id field
        if not data.get("scopus_id"):
            data["scopus_id"] = []
        elif isinstance(data.get("scopus_id"), str):
            data["scopus_id"] = [data["scopus_id"]]

        # Move scopus_id to scopus if empty
        if data.get("scopus_id") and not data.get("scopus"):
            data["scopus"] = data["scopus_id"]

        return data

    class Config:
        frozen = True


class Author(BaseModel):
    pure_username: str | None = None
    given: str | None = None
    family: str | None = None
    uuid: str | None = None
    other_names: list[str]
    isni: str | None = None
    scopus_id: list[str]
    orcid: list[str]
    dai_nl: list[str]
    affiliation: list[str]

    @model_validator(mode="before")
    @classmethod
    def replace_none_with_empty(cls, data) -> dict | Any:
        """
        for each field that expects an object but can be None,
        replace None with an class instance with all fields set to None
        in order to preserve the schema
        """
        if not isinstance(data, dict):
            data = {}

        if data.get("pure-username"):
            data["pure_username"] = data.get("pure-username")
        if data.get("other-names"):
            data["other_names"] = data.get("other-names")
        if data.get("scopus-id"):
            data["scopus_id"] = data.get("scopus-id")
        if data.get("dai-nl"):
            data["dai_nl"] = data.get("dai-nl")

        # Initialize empty lists if fields are None
        list_fields = ["affiliation", "scopus_id", "orcid", "other_names", "dai_nl"]
        for field in list_fields:
            if not data.get(field):
                data[field] = []
            elif isinstance(data.get(field), str):
                data[field] = [data[field]]

        return data

    class Config:
        frozen = True


class Origin(BaseModel):
    issued: str | None = None
    published: str | None = None
    place: str | None = None
    publisher: str | None = None

    class Config:
        frozen = True


class Publication(BaseModel):
    """
    Model for metadata for a single publication retrieved from the OAI-PMH endpoint openaire_cris_publications
    with the 'mods' metadata format
    """

    id: int
    uuid: str
    researchoutputwizard: list[str] | None = None
    nbn_id: str | None = None
    uri: str | None = None
    isbn: list[str] | None = None
    doi: str | None = None
    orcid: list[str] | None = None
    scopus: list[str] | None = None

    title: str | None = None
    subtitles: list[str] | None = None
    bibliographic_reference: str | None = None
    pages: str | None = None
    subject: list[str] | None = None
    locations: list[str] | None = None
    language: str | None = None
    item_type: str | None = None
    abstract: str | None = None

    oa: bool = False
    authors: list[Author] | None = None
    organizations: list[Organization] | None = None
    source: list[Source] | None = None
    electronic_versions: list[File] | None = None

    @model_validator(mode="before")
    @classmethod
    def replace_none_with_empty_classes(cls, data) -> dict | Any:
        """
        for each field that expects an object but can be None,
        replace None with an class instance with all fields set to None
        in order to preserve the schema
        """

        if not isinstance(data, dict):
            data = {}

        # Initialize empty lists for all list fields
        list_fields = [
            "authors",
            "organizations",
            "source",
            "electronic_versions",
            "subject",
            "locations",
            "isbn",
            "orcid",
            "scopus",
            "researchoutputwizard",
            "subtitles",
        ]
        if data.get("item-type"):
            data["item_type"] = data.get("item-type")
        if data.get("bibliographic-reference"):
            data["bibliographic_reference"] = data.get("bibliographic-reference")
        if data.get("nbn-id"):
            data["nbn_id"] = data.get("nbn-id")
        for field in list_fields:
            if not data.get(field):
                data[field] = []
            elif not isinstance(data[field], list):
                data[field] = [data[field]]

        # Convert nested objects
        if data.get("authors"):
            data["authors"] = [
                Author.model_validate(author) for author in data["authors"]
            ]

        if data.get("organizations"):
            data["organizations"] = [
                Organization.model_validate(org) for org in data["organizations"]
            ]

        if data.get("source"):
            data["source"] = [Source.model_validate(src) for src in data["source"]]

        if data.get("electronic_versions"):
            data["electronic_versions"] = [
                File.model_validate(file) for file in data["electronic_versions"]
            ]

        return data

    class Config:
        frozen = True


class Publications(BaseModel):
    publications: list[Publication] = Field(default_factory=list)

    def __len__(self) -> int:
        return len(self.publications)

    class Config:
        frozen = True


def parse_raw_pure_data(
    raw_data: str, ids_stored: list[str] | None = None
) -> tuple[str | None, list[Publication]]:
    """
    parses the raw XML from the Pure API and returns a list of records.
    Also returns the resumption token for the next call.
    """

    def parse_identifiers(item: list[dict[str, str]]) -> dict[str, str]:
        """ """
        identifiers = {}
        if not isinstance(item, list):
            item = [item]
        for i in item:
            id_value = i.get("#text")
            id_type = i.get("@type")
            if id_type == "local":
                id_type = id_value.split(":")[0].strip()
                id_value = id_value.split(":")[1].strip()
            if "pure" in id_type:
                id_type = id_type.split("/")[-1].strip()

            if id_type in identifiers:
                if isinstance(identifiers[id_type], list):
                    identifiers[id_type].append(id_value)
                else:
                    identifiers[id_type] = [identifiers[id_type], id_value]

            else:
                identifiers[id_type] = id_value
        return {"identifiers": identifiers}

    def parse_related_item(related_item: list[dict]) -> dict[list[dict]]:
        """ """
        related_items = {}
        if not isinstance(related_item, list):
            related_item = [related_item]
        for item in related_item:
            rel_item = {}
            if item.get("part"):
                if item.get("part").get("text"):
                    # this is based on the example, could be something different
                    related_items["bibliographic_reference"] = (
                        item.get("part").get("text").get("#text")
                    )
                    continue

                detail = item.get("part").get("detail") or {}
                if isinstance(detail, list):
                    detail = detail[0]
                if (
                    detail.get("@type") == "issue" or detail.get("@type") == "volume"
                ) and detail.get("number"):
                    rel_item["issue"] = detail.get("number")

            if item.get("titleInfo"):
                rel_item["title"] = item["titleInfo"].get("title")
            if item.get("originInfo") and isinstance(item["originInfo"], dict):
                rel_item.update(item.get("originInfo"))
            if item.get("identifier"):
                rel_item.update(parse_identifiers(item["identifier"]))

            if "publisher" in rel_item or rel_item.get("identifiers", {}).get("issn"):
                related_items["source"] = rel_item
                if related_items["source"].get("identifiers", {}).get("issn"):
                    identifiers = related_items["source"]["identifiers"]
                    del related_items["source"]["identifiers"]
                    try:
                        related_items["source"].update(identifiers)
                    except Exception:
                        print(related_items["source"])
                        print(identifiers)
                        input("continue?")

        return related_items

    def parse_physical_description(item: list[dict]) -> dict:
        """ """

        pages: str = ""
        electronic_versions = []
        if not isinstance(item, list):
            item = [item]
        for component in item:
            unit = component.get("extent", {}).get("@unit")
            if not unit:
                continue
            if unit == "pages":
                # number of pages
                pages = component["extent"].get("#text")
                continue
            if (
                unit == "bytes"
                or component.get("form", {}).get("#text") == "electronic"
            ):
                # electronic version
                version = {}
                if component.get("note"):
                    if not isinstance(component.get("note"), list):
                        notes = [component["note"]]
                    else:
                        notes = component["note"]
                    for note in notes:
                        version[note.get("@type")] = (
                            note.get("#text")
                            if note.get("#text")
                            else note.get("@x:href")
                        )
                    if version:
                        electronic_versions.append(version)

        result = {}
        if pages:
            result["pages"] = pages
        if electronic_versions:
            result["electronic_versions"] = electronic_versions
        return result

    def parse_title_info(item: list) -> dict:
        """ """
        if not isinstance(item, list):
            item = [item]
        titles = [t.get("title") for t in item if t.get("title")]
        subtitles = [t.get("subTitle") for t in item if t.get("subTitle")]
        if titles:
            result = {"title": titles[0]}
            if len(titles) > 1:
                more = titles[1:]
                if not isinstance(more, list):
                    more = [more]
                result["alternative_titles"] = more
        if subtitles:
            result["subtitles"] = subtitles[0]
            if len(subtitles) > 1:
                if not isinstance(result.get("alternative_titles"), list):
                    more_sub = subtitles[1:]
                    if not isinstance(more_sub, list):
                        more_sub = [more_sub]
                    result["alternative_titles"] = more_sub
                else:
                    result["alternative_titles"].extend(subtitles[1:])

        return result

    def parse_authors(items: list[dict]) -> dict:
        """ """
        authors = []
        orgs = []
        if not isinstance(items, list):
            items = [items]
        for item in items:
            is_author = False
            if item.get("role"):
                if not isinstance(item.get("role"), list):
                    item["role"] = [item["role"]]
                for role in item.get("role"):
                    if any(
                        term in role.get("roleTerm", {}).get("#text", "")
                        for term in ["editor", "author", "contributor"]
                    ):
                        is_author = True
                        break
            if item.get("namePart"):
                namelist = item.get("namePart")
                if not isinstance(namelist, str):
                    if not isinstance(namelist, list):
                        namelist = [namelist]
                    for name in namelist:
                        if (
                            name.get("@type") == "given"
                            or name.get("@type") == "family"
                        ):
                            is_author = True
                            break

            if is_author:
                author = {}
                author["affiliation"] = (
                    list(set(item.get("affiliation")))
                    if isinstance(item.get("affiliation"), list)
                    else [item.get("affiliation")]
                    if isinstance(item.get("affiliation"), str)
                    else []
                )
                ids = (
                    item.get("nameIdentifier", [])
                    if isinstance(item.get("nameIdentifier"), list)
                    else [item.get("nameIdentifier")]
                    if item.get("nameIdentifier")
                    else []
                )
                if ids and ids is not None and len(ids) > 0:
                    author.update(parse_identifiers(ids))
                for role in item.get("role"):
                    if role.get("roleTerm", {}).get("@authority") == "pure/username":
                        author["pure_username"] = role.get("roleTerm", {}).get("#text")
                if item.get("namePart"):
                    namelist = item.get("namePart")
                    if not isinstance(namelist, list):
                        namelist = [namelist]
                    for name in namelist:
                        if name.get("@type") == "given":
                            author["given"] = name.get("#text")
                        elif name.get("@type") == "family":
                            author["family"] = name.get("#text")
                        else:
                            if not author.get("other_names"):
                                author["other_names"] = []
                            author["other_names"].append(name.get("#text"))
                authors.append(author)

            else:
                org = {}
                for role in item.get("role"):
                    if (
                        role.get("roleTerm", {}).get("@authority")
                        == "pure/organisationType"
                    ):
                        org["type"] = (
                            role.get("roleTerm", {})
                            .get("#text")
                            .replace(
                                "/dk/atira/pure/organisation/organisationtypes/organisation/",
                                "",
                            )
                            .replace("_", " ")
                        )
                    if (
                        role.get("roleTerm", {}).get("@authority")
                        == "pure/linkidentifier/scopus_affiliation_id"
                    ):
                        if not org.get("scopus_id"):
                            org["scopus_id"] = []
                        org["scopus_id"].append(role.get("roleTerm", {}).get("#text"))
                if item.get("nameIdentifier"):
                    ids = (
                        item.get("nameIdentifier")
                        if isinstance(item.get("nameIdentifier"), list)
                        else [item.get("nameIdentifier")]
                    )
                    if ids:
                        org.update(parse_identifiers(ids))
                if item.get("namePart"):
                    org["name"] = item.get("namePart")
                orgs.append(org)

        results = {}
        if authors:
            results["authors"] = authors
            for author in authors:
                identifiers = author.get("identifiers", [])
                if not identifiers:
                    continue
                moved = 0
                if identifiers:
                    for identifier in identifiers:
                        if identifier not in author:
                            author[identifier] = identifiers[identifier]
                            moved += 1
                    if moved == len(identifiers) and moved > 0:
                        del author["identifiers"]
        if orgs:
            results["organizations"] = orgs
            for org in orgs:
                identifiers = org.get("identifiers", [])
                moved = 0
                if identifiers:
                    for identifier in identifiers:
                        if identifier not in org:
                            org[identifier] = identifiers[identifier]
                            moved += 1
                    if moved == len(identifiers) and moved > 0:
                        del org["identifiers"]

        return results

    def parse_genre(item: dict | list[dict]) -> dict:
        """ """
        if isinstance(item, list):
            genres = [parse_genre(i) for i in item]
            return {
                "item_type": ", ".join(
                    g.get("item_type") for g in genres if g.get("item_type")
                )
            }
        return {"item_type": item.get("#text")} if item.get("#text") else {}

    def parse_origin_info(item: dict) -> dict:
        """ """

        origin = {}

        if item.get("dateIssued"):
            origin["issued"] = item.get("dateIssued", {}).get("#text")
        if item.get("dateOther"):
            if not isinstance(item.get("dateOther"), list) and item.get("dateOther"):
                item["dateOther"] = [item["dateOther"]]
            for date in item.get("dateOther"):
                origin[date.get("@type")] = date.get("#text")
        if item.get("place"):
            origin["place"] = item.get("place").get("placeTerm")
        if item.get("publisher"):
            origin["publisher"] = item.get("publisher")

        return {"origin": origin} if origin else {}

    def parse_subject(item: dict) -> dict:
        """ """
        return {"subject": item.get("topic")} if item.get("topic") else {}

    def parse_language(item: dict) -> dict:
        """ """
        return (
            {"language": item.get("languageTerm", {}).get("#text")}
            if item.get("languageTerm", {}).get("#text")
            else {}
        )

    def parse_abstract(item: dict) -> dict:
        """ """
        return {"abstract": item.get("#text")} if item.get("#text") else {}

    def parse_location(item: list[dict] | dict) -> dict:
        if not isinstance(item, list):
            item = [item]
        locations = [loc.get("url") for loc in item if loc.get("url")]
        if locations:
            final_locs = []
            for loc in locations:
                if isinstance(loc, dict):
                    final_locs.append(loc.get("#text")) if loc.get("#text") else None
                else:
                    final_locs.append(loc)
            return {"locations": final_locs} if final_locs else {}
        return {"locations": locations} if locations else {}

    def parse_access_condition(item: dict) -> dict:
        """ """
        if "openAccess" in item.get("@type") or "open" in item.get("@type"):
            return {"oa": True}
        return {"oa": False}

    data = xmltodict.parse(
        raw_data,
        process_namespaces=True,
        namespaces={
            "http://www.loc.gov/mods/v3": None,
            "http://www.w3.org/2001/XMLSchema-instance": None,
            "http://www.w3.org/1999/xlink": "x",
            "http://www.openarchives.org/OAI/2.0/": None,
        },
    )
    resumptiontoken = data["OAI-PMH"]["ListRecords"].get("resumptionToken").get("#text")
    skipped = 0
    errors = 0
    parsed_items = []
    for item in data["OAI-PMH"]["ListRecords"]["record"]:
        try:
            item: dict[str, dict | list] = item["metadata"][
                "mods"
            ]  # all data is in item.metadata.mods
            parsed_item = {}  # init the dict
            item_id = (
                parse_identifiers(item.get("identifier")).get("identifiers").get("id")
                or None
            )
            if ids_stored and item_id and item_id in ids_stored:
                skipped += 1
                continue
            parse_dict: dict[str, callable] = {
                "identifier": parse_identifiers,
                "relatedItem": parse_related_item,
                "physicalDescription": parse_physical_description,
                "titleInfo": parse_title_info,
                "name": parse_authors,
                "genre": parse_genre,
                # "note": parse_note,
                "originInfo": parse_origin_info,
                "subject": parse_subject,
                "language": parse_language,
                "abstract": parse_abstract,
                "accessCondition": parse_access_condition,
                "location": parse_location,
            }
        except Exception as e:
            print(f" error while initializing item: {e}")
            print(item)
            traceback.print_exc()
            continue

        try:
            parse_results = [
                func(item.get(key) or {}) for key, func in parse_dict.items()
            ]

            for res in parse_results:
                parsed_item.update(res)

            # Additional:
            # move identifiers from nexted in parsed_item.get('identifiers') to the root if there are no conflicts
            # (shouldnt be?)
            identifiers = parsed_item.get("identifiers", [])
            moved = 0
            if identifiers:
                for identifier in identifiers:
                    if identifier not in parsed_item:
                        parsed_item[identifier] = identifiers[identifier]
                        moved += 1
            if moved == len(identifiers):
                del parsed_item["identifiers"]

            als_raw = "n"
            # als_raw = input("press y to view detailed comparsion, q to quit, other key to continue.")
            if als_raw == "q":
                return None
            if als_raw == "y":
                print("Printing comparsion")
                ignore_keys = [
                    "@version",
                    "@schemaLocation",
                    "@xmlns",
                    "recordInfo",
                    "note",
                    "classification",
                ]
                all_keys_in_raw = [k for k in item if k not in ignore_keys]
                stop = ""

                for key, func in parse_dict.items():
                    if key in item:
                        print("=============================")
                        print("            " + key.capitalize())
                        print("-----------------------------------------------\n")
                        print("    RAW: \n")
                        print(item.get(key))
                        print("-----------------------------------------------\n")
                        print("    PARSED: \n")
                        print(func(item.get(key)))

                        # remove the key from the list of keys in raw
                        all_keys_in_raw.remove(key)
                    else:
                        print(f"Key {key} not found in item")
                    if als_raw == "y":
                        stop = input("press any key to print the next, q to stop")
                        if stop == "q":
                            break
                if all_keys_in_raw and stop != "q":
                    print(
                        f"top level keys in raw item that is not parsed: {all_keys_in_raw}"
                    )
                    for key in all_keys_in_raw:
                        print(f"key: {key}")
                        print("Contents:")
                        print(item.get(key))
                # input("press any key to continue")

            parsed_items.append(parsed_item)
        except Exception as e:
            print(f"Error while parsing item: {e}")
            print(item)
            traceback.print_exc()
            errors += 1

        # now make into object!
        if not parsed_items:
            print(f"No items parsed. {skipped} skipped, {errors} errors.")
            return None, []
        for parsed_item in parsed_items:
            try:
                Publication.model_validate(parsed_item)
            except Exception as e:
                print(f"Error while parsing xml tree to Publication instance: {e}")
                print(parsed_item)
                traceback.print_exc()

        final_parsed_items = Publications(publications=parsed_items).publications
    return resumptiontoken, final_parsed_items
