import sys

import lxml.etree as ET


def transform_xml(input_file, output_file):
    # Parse the input XML
    parser = ET.XMLParser(remove_blank_text=True)
    tree = ET.parse(input_file, parser)
    root = tree.getroot()

    # Create new root element for output
    new_root = ET.Element("ListRecords")

    # Extract records from the input
    records = root.xpath("//ListRecords/record")

    for record in records:
        # Create a new record element
        new_record = ET.SubElement(new_root, "record")

        # Process header identifiers
        header = record.find(".//header")
        if header is not None:
            identifier = header.find("identifier")
            if identifier is not None and identifier.text:
                # Extract the UUID from the identifier
                id_parts = identifier.text.split("/")
                if len(id_parts) > 0:
                    uuid = id_parts[-1]

                    # Add the identifiers
                    id_elem = ET.SubElement(new_record, "identifier", type="uuid")
                    id_elem.text = uuid

        # Process metadata
        metadata = record.find(".//metadata")
        if metadata is not None:
            mods = metadata.find(".//{http://www.loc.gov/mods/v3}mods")
            if mods is not None:
                # Process identifiers
                for mods_id in mods.findall(
                    ".//{http://www.loc.gov/mods/v3}identifier"
                ):
                    id_type = mods_id.get("type")
                    if id_type:
                        new_id = ET.SubElement(new_record, "identifier", type=id_type)
                        new_id.text = mods_id.text

                # Process related items
                for related in mods.findall(
                    ".//{http://www.loc.gov/mods/v3}relatedItem"
                ):
                    rel_type = related.get("type")
                    if rel_type:
                        new_related = ET.SubElement(
                            new_record, "relatedItem", type=rel_type
                        )

                        # Process parts
                        for part in related.findall(
                            ".//{http://www.loc.gov/mods/v3}part"
                        ):
                            new_part = ET.SubElement(new_related, "part")

                            # Process text
                            for text_elem in part.findall(
                                ".//{http://www.loc.gov/mods/v3}text"
                            ):
                                new_text = ET.SubElement(new_part, "text")
                                new_text.text = text_elem.text

                # Process physical description
                for phys in mods.findall(
                    ".//{http://www.loc.gov/mods/v3}physicalDescription"
                ):
                    new_phys = ET.SubElement(new_record, "physicalDescription")

                    # Process extent
                    for extent in phys.findall(".//{http://www.loc.gov/mods/v3}extent"):
                        unit = extent.get("unit")
                        if unit:
                            new_extent = ET.SubElement(new_phys, "extent", unit=unit)
                            new_extent.text = extent.text

                    # Process form, internetMediaType, notes
                    for form in phys.findall(".//{http://www.loc.gov/mods/v3}form"):
                        new_form = ET.SubElement(new_phys, "form")
                        if form.get("authority"):
                            new_form.set("authority", form.get("authority"))
                        new_form.text = form.text

                    for media_type in phys.findall(
                        ".//{http://www.loc.gov/mods/v3}internetMediaType"
                    ):
                        new_media = ET.SubElement(new_phys, "internetMediaType")
                        new_media.text = media_type.text

                    for note in phys.findall(".//{http://www.loc.gov/mods/v3}note"):
                        new_note = ET.SubElement(new_phys, "note")
                        note_type = note.get("type")
                        if note_type:
                            new_note.set("type", note_type)
                        if note.get("xlink:href"):
                            new_note.set(
                                "href", note.get("{http://www.w3.org/1999/xlink}href")
                            )
                        new_note.text = note.text

                # Process notes
                for note in mods.findall(".//{http://www.loc.gov/mods/v3}note"):
                    if (
                        note.getparent().tag
                        != "{http://www.loc.gov/mods/v3}physicalDescription"
                    ):
                        new_note = ET.SubElement(new_record, "note")
                        if note.get("type"):
                            new_note.set("type", note.get("type"))
                        new_note.text = note.text

                # Process title info
                for title_info in mods.findall(
                    ".//{http://www.loc.gov/mods/v3}titleInfo"
                ):
                    new_title_info = ET.SubElement(new_record, "titleInfo")
                    if title_info.get("{http://www.w3.org/XML/1998/namespace}lang"):
                        new_title_info.set(
                            "lang",
                            title_info.get(
                                "{http://www.w3.org/XML/1998/namespace}lang"
                            ),
                        )

                    for title in title_info.findall(
                        ".//{http://www.loc.gov/mods/v3}title"
                    ):
                        new_title = ET.SubElement(new_title_info, "title")
                        new_title.text = title.text

                    for subtitle in title_info.findall(
                        ".//{http://www.loc.gov/mods/v3}subTitle"
                    ):
                        new_subtitle = ET.SubElement(new_title_info, "subTitle")
                        new_subtitle.text = subtitle.text

                # Process names (authors, editors)
                for name in mods.findall(".//{http://www.loc.gov/mods/v3}name"):
                    new_name = ET.SubElement(new_record, "name")
                    name_type = name.get("type")
                    if name_type:
                        new_name.set("type", name_type)

                    if name.get("{http://www.w3.org/XML/1998/namespace}lang"):
                        new_name.set(
                            "lang",
                            name.get("{http://www.w3.org/XML/1998/namespace}lang"),
                        )

                    # Process roles
                    for role in name.findall(".//{http://www.loc.gov/mods/v3}role"):
                        new_role = ET.SubElement(new_name, "role")

                        for role_term in role.findall(
                            ".//{http://www.loc.gov/mods/v3}roleTerm"
                        ):
                            new_role_term = ET.SubElement(new_role, "roleTerm")
                            if role_term.get("authority"):
                                new_role_term.set(
                                    "authority", role_term.get("authority")
                                )
                            if role_term.get("type"):
                                new_role_term.set("type", role_term.get("type"))
                            new_role_term.text = role_term.text

                    # Process name identifiers
                    for name_id in name.findall(
                        ".//{http://www.loc.gov/mods/v3}nameIdentifier"
                    ):
                        new_name_id = ET.SubElement(new_name, "nameIdentifier")
                        id_type = name_id.get("type")
                        if id_type:
                            new_name_id.set("type", id_type)
                        new_name_id.text = name_id.text

                    # Process name parts
                    for name_part in name.findall(
                        ".//{http://www.loc.gov/mods/v3}namePart"
                    ):
                        new_name_part = ET.SubElement(new_name, "namePart")
                        if name_part.get("type"):
                            new_name_part.set("type", name_part.get("type"))
                        new_name_part.text = name_part.text

                    # Process affiliations
                    for affiliation in name.findall(
                        ".//{http://www.loc.gov/mods/v3}affiliation"
                    ):
                        new_affiliation = ET.SubElement(new_name, "affiliation")
                        new_affiliation.text = affiliation.text

                # Process genre
                for genre in mods.findall(".//{http://www.loc.gov/mods/v3}genre"):
                    new_genre = ET.SubElement(new_record, "genre")
                    if genre.get("authority"):
                        new_genre.set("authority", genre.get("authority"))
                    if genre.get("type"):
                        new_genre.set("type", genre.get("type"))
                    new_genre.text = genre.text

                # Process origin info
                for origin in mods.findall(".//{http://www.loc.gov/mods/v3}originInfo"):
                    new_origin = ET.SubElement(new_record, "originInfo")

                    for date_issued in origin.findall(
                        ".//{http://www.loc.gov/mods/v3}dateIssued"
                    ):
                        new_date = ET.SubElement(new_origin, "dateIssued")
                        new_date.text = date_issued.text

                    for date_other in origin.findall(
                        ".//{http://www.loc.gov/mods/v3}dateOther"
                    ):
                        new_date = ET.SubElement(new_origin, "dateOther")
                        if date_other.get("type"):
                            new_date.set("type", date_other.get("type"))
                        new_date.text = date_other.text

                    for place in origin.findall(".//{http://www.loc.gov/mods/v3}place"):
                        new_place = ET.SubElement(new_origin, "place")
                        for place_term in place.findall(
                            ".//{http://www.loc.gov/mods/v3}placeTerm"
                        ):
                            new_place_term = ET.SubElement(new_place, "placeTerm")
                            new_place_term.text = place_term.text

                    for publisher in origin.findall(
                        ".//{http://www.loc.gov/mods/v3}publisher"
                    ):
                        new_publisher = ET.SubElement(new_origin, "publisher")
                        new_publisher.text = publisher.text

                # Process subject
                for subject in mods.findall(".//{http://www.loc.gov/mods/v3}subject"):
                    new_subject = ET.SubElement(new_record, "subject")

                    for topic in subject.findall(
                        ".//{http://www.loc.gov/mods/v3}topic"
                    ):
                        new_topic = ET.SubElement(new_subject, "topic")
                        new_topic.text = topic.text

                # Process language
                for language in mods.findall(".//{http://www.loc.gov/mods/v3}language"):
                    new_lang = ET.SubElement(new_record, "language")

                    for term in language.findall(
                        ".//{http://www.loc.gov/mods/v3}languageTerm"
                    ):
                        new_term = ET.SubElement(new_lang, "languageTerm")
                        if term.get("type"):
                            new_term.set("type", term.get("type"))
                        new_term.text = term.text

                # Process abstract
                for abstract in mods.findall(".//{http://www.loc.gov/mods/v3}abstract"):
                    new_abstract = ET.SubElement(new_record, "abstract")
                    if abstract.get("type"):
                        new_abstract.set("type", abstract.get("type"))
                    if abstract.get("{http://www.w3.org/XML/1998/namespace}lang"):
                        new_abstract.set(
                            "lang",
                            abstract.get("{http://www.w3.org/XML/1998/namespace}lang"),
                        )
                    new_abstract.text = abstract.text

                # Process access condition
                for access in mods.findall(
                    ".//{http://www.loc.gov/mods/v3}accessCondition"
                ):
                    new_access = ET.SubElement(new_record, "accessCondition")
                    if access.get("type"):
                        new_access.set("type", access.get("type"))
                    new_access.text = access.text

    # Add resumptionToken if it exists in the original
    resumption_token = root.find(".//resumptionToken")
    if resumption_token is not None:
        new_token = ET.SubElement(new_root, "resumptionToken")
        new_token.text = resumption_token.text

        # Copy attributes from original token
        for attr_name, attr_value in resumption_token.attrib.items():
            new_token.set(attr_name, attr_value)

    # Write to output file
    tree = ET.ElementTree(new_root)
    tree.write(output_file, pretty_print=True, encoding="UTF-8", xml_declaration=False)
    print(f"Transformed XML has been written to {output_file}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python transform_pure_data.py <input_xml_file> <output_xml_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    transform_xml(input_file, output_file)
