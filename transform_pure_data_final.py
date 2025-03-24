import sys

import lxml.etree as ET


def transform_xml(input_file, output_file):
    """
    Transform raw publication XML data into a clean, simplified format.

    Args:
        input_file: Path to input XML file
        output_file: Path to output XML file
    """
    # Define namespaces used in the source XML
    namespaces = {
        "oai": "http://www.openarchives.org/OAI/2.0/",
        "mods": "http://www.loc.gov/mods/v3",
        "xlink": "http://www.w3.org/1999/xlink",
        "xsi": "http://www.w3.org/2001/XMLSchema-instance",
        "xml": "http://www.w3.org/XML/1998/namespace",
    }

    # Parse the input XML
    parser = ET.XMLParser(remove_blank_text=True)
    tree = ET.parse(input_file, parser)
    root = tree.getroot()

    # Create new root element
    new_root = ET.Element("ListRecords")

    # Process each record
    for record in root.xpath("//oai:ListRecords/oai:record", namespaces=namespaces):
        new_record = ET.SubElement(new_root, "record")

        # Get header identifier
        header_identifier = record.xpath(".//oai:identifier", namespaces=namespaces)
        if header_identifier:
            oai_id = header_identifier[0].text
            if oai_id and "/" in oai_id:
                uuid = oai_id.split("/")[-1]  # Extract UUID from OAI identifier

        # Get metadata section
        metadata = record.find(".//mods:mods", namespaces=namespaces)
        if metadata is None:
            continue

        # Process identifiers
        for ident in metadata.findall(".//mods:identifier", namespaces=namespaces):
            id_type = ident.get("type")
            if id_type:
                new_id = ET.SubElement(new_record, "identifier", type=id_type)
                new_id.text = ident.text

        # Process related items
        for related in metadata.findall(".//mods:relatedItem", namespaces=namespaces):
            # Skip nested relatedItems
            if (
                related.find("./ancestor::mods:relatedItem", namespaces=namespaces)
                is not None
            ):
                continue

            rel_type = related.get("type", "")
            new_related = ET.SubElement(new_record, "relatedItem", type=rel_type)

            # Process parts
            for part in related.findall(".//mods:part", namespaces=namespaces):
                new_part = ET.SubElement(new_related, "part")

                # Text elements
                for text_elem in part.findall(".//mods:text", namespaces=namespaces):
                    new_text = ET.SubElement(new_part, "text")
                    new_text.text = text_elem.text

                # Detail elements (for volume, issue numbers, etc.)
                for detail in part.findall(".//mods:detail", namespaces=namespaces):
                    detail_type = detail.get("type")
                    if detail_type:
                        new_detail = ET.SubElement(new_part, "detail", type=detail_type)

                        # Number
                        number = detail.find(".//mods:number", namespaces=namespaces)
                        if number is not None:
                            new_number = ET.SubElement(new_detail, "number")
                            new_number.text = number.text

                        # Caption
                        caption = detail.find(".//mods:caption", namespaces=namespaces)
                        if caption is not None:
                            new_caption = ET.SubElement(new_detail, "caption")
                            new_caption.text = caption.text

            # TitleInfo in relatedItem
            for title_info in related.findall(
                "./mods:titleInfo", namespaces=namespaces
            ):
                new_title_info = ET.SubElement(new_related, "titleInfo")

                # Title
                title = title_info.find(".//mods:title", namespaces=namespaces)
                if title is not None:
                    new_title = ET.SubElement(new_title_info, "title")
                    new_title.text = title.text

            # OriginInfo in relatedItem
            for origin in related.findall("./mods:originInfo", namespaces=namespaces):
                new_origin = ET.SubElement(new_related, "originInfo")

                # Publisher
                publisher = origin.find(".//mods:publisher", namespaces=namespaces)
                if publisher is not None:
                    new_publisher = ET.SubElement(new_origin, "publisher")
                    new_publisher.text = publisher.text

            # Identifiers in relatedItem
            for ident in related.findall("./mods:identifier", namespaces=namespaces):
                id_type = ident.get("type")
                if id_type:
                    new_id = ET.SubElement(new_related, "identifier", type=id_type)
                    new_id.text = ident.text

        # Process physicalDescription
        for phys in metadata.findall(
            "./mods:physicalDescription", namespaces=namespaces
        ):
            new_phys = ET.SubElement(new_record, "physicalDescription")

            # Extent
            for extent in phys.findall("./mods:extent", namespaces=namespaces):
                unit = extent.get("unit")
                new_extent = ET.SubElement(new_phys, "extent", unit=unit)
                new_extent.text = extent.text

            # Form
            for form in phys.findall("./mods:form", namespaces=namespaces):
                new_form = ET.SubElement(new_phys, "form")
                if form.get("authority"):
                    new_form.set("authority", form.get("authority"))
                new_form.text = form.text

            # Note
            for note in phys.findall("./mods:note", namespaces=namespaces):
                new_note = ET.SubElement(new_phys, "note")

                note_type = note.get("type")
                if note_type:
                    new_note.set("type", note_type)

                href = note.get("{http://www.w3.org/1999/xlink}href")
                if href:
                    new_note.set("href", href)

                new_note.text = note.text

            # Internet media type
            for media_type in phys.findall(
                "./mods:internetMediaType", namespaces=namespaces
            ):
                new_media = ET.SubElement(new_phys, "internetMediaType")
                new_media.text = media_type.text

        # Process notes at top level
        for note in metadata.findall("./mods:note", namespaces=namespaces):
            new_note = ET.SubElement(new_record, "note")

            note_type = note.get("type")
            if note_type:
                new_note.set("type", note_type)

            new_note.text = note.text

        # Process titleInfo at top level
        for title_info in metadata.findall("./mods:titleInfo", namespaces=namespaces):
            if (
                title_info.find("./ancestor::mods:relatedItem", namespaces=namespaces)
                is not None
            ):
                continue

            new_title_info = ET.SubElement(new_record, "titleInfo")

            lang = title_info.get("{http://www.w3.org/XML/1998/namespace}lang")
            if lang:
                new_title_info.set("lang", lang)

            # Title
            title = title_info.find("./mods:title", namespaces=namespaces)
            if title is not None:
                new_title = ET.SubElement(new_title_info, "title")
                new_title.text = title.text

            # Subtitle
            subtitle = title_info.find("./mods:subTitle", namespaces=namespaces)
            if subtitle is not None:
                new_subtitle = ET.SubElement(new_title_info, "subTitle")
                new_subtitle.text = subtitle.text

        # Process names (authors, editors)
        for name in metadata.findall("./mods:name", namespaces=namespaces):
            name_type = name.get("type")
            new_name = ET.SubElement(new_record, "name", type=name_type)

            lang = name.get("{http://www.w3.org/XML/1998/namespace}lang")
            if lang:
                new_name.set("lang", lang)

            # Roles
            for role in name.findall("./mods:role", namespaces=namespaces):
                new_role = ET.SubElement(new_name, "role")

                for role_term in role.findall("./mods:roleTerm", namespaces=namespaces):
                    new_role_term = ET.SubElement(new_role, "roleTerm")

                    role_type = role_term.get("type")
                    if role_type:
                        new_role_term.set("type", role_type)

                    authority = role_term.get("authority")
                    if authority:
                        new_role_term.set("authority", authority)

                    new_role_term.text = role_term.text

            # Name identifiers
            for name_id in name.findall("./mods:nameIdentifier", namespaces=namespaces):
                new_name_id = ET.SubElement(new_name, "nameIdentifier")

                id_type = name_id.get("type")
                if id_type:
                    new_name_id.set("type", id_type)

                type_uri = name_id.get("typeURI")
                if type_uri:
                    new_name_id.set("typeURI", type_uri)

                new_name_id.text = name_id.text

            # Name parts
            for name_part in name.findall("./mods:namePart", namespaces=namespaces):
                new_name_part = ET.SubElement(new_name, "namePart")

                part_type = name_part.get("type")
                if part_type:
                    new_name_part.set("type", part_type)

                new_name_part.text = name_part.text

            # Affiliations
            for affiliation in name.findall(
                "./mods:affiliation", namespaces=namespaces
            ):
                new_affiliation = ET.SubElement(new_name, "affiliation")
                new_affiliation.text = affiliation.text

        # Process genre
        for genre in metadata.findall("./mods:genre", namespaces=namespaces):
            new_genre = ET.SubElement(new_record, "genre")

            # Copy simple attributes (without namespaces)
            for attr_name, attr_value in genre.attrib.items():
                if not attr_name.startswith("{"):
                    new_genre.set(attr_name, attr_value)

            new_genre.text = genre.text

        # Process originInfo
        for origin in metadata.findall("./mods:originInfo", namespaces=namespaces):
            if (
                origin.find("./ancestor::mods:relatedItem", namespaces=namespaces)
                is not None
            ):
                continue

            new_origin = ET.SubElement(new_record, "originInfo")

            # Date issued
            for date_issued in origin.findall(
                "./mods:dateIssued", namespaces=namespaces
            ):
                new_date = ET.SubElement(new_origin, "dateIssued")
                new_date.text = date_issued.text

            # Date other
            for date_other in origin.findall("./mods:dateOther", namespaces=namespaces):
                new_date = ET.SubElement(new_origin, "dateOther")

                date_type = date_other.get("type")
                if date_type:
                    new_date.set("type", date_type)

                new_date.text = date_other.text

            # Place
            for place in origin.findall("./mods:place", namespaces=namespaces):
                new_place = ET.SubElement(new_origin, "place")

                for place_term in place.findall(
                    "./mods:placeTerm", namespaces=namespaces
                ):
                    new_place_term = ET.SubElement(new_place, "placeTerm")
                    new_place_term.text = place_term.text

            # Publisher
            for publisher in origin.findall("./mods:publisher", namespaces=namespaces):
                new_publisher = ET.SubElement(new_origin, "publisher")
                new_publisher.text = publisher.text

        # Process subject
        for subject in metadata.findall("./mods:subject", namespaces=namespaces):
            new_subject = ET.SubElement(new_record, "subject")

            for topic in subject.findall("./mods:topic", namespaces=namespaces):
                new_topic = ET.SubElement(new_subject, "topic")
                new_topic.text = topic.text

        # Process URI identifiers
        for uri in metadata.findall(
            "./mods:identifier[@type='uri']", namespaces=namespaces
        ):
            new_uri = ET.SubElement(new_record, "identifier", type="uri")
            new_uri.text = uri.text

        # Process language
        for language in metadata.findall("./mods:language", namespaces=namespaces):
            new_lang = ET.SubElement(new_record, "language")

            for term in language.findall("./mods:languageTerm", namespaces=namespaces):
                new_term = ET.SubElement(new_lang, "languageTerm")

                term_type = term.get("type")
                if term_type:
                    new_term.set("type", term_type)

                authority = term.get("authority")
                if authority:
                    new_term.set("authority", authority)

                new_term.text = term.text

        # Process abstract
        for abstract in metadata.findall("./mods:abstract", namespaces=namespaces):
            new_abstract = ET.SubElement(new_record, "abstract")

            abstract_type = abstract.get("type")
            if abstract_type:
                new_abstract.set("type", abstract_type)

            lang = abstract.get("{http://www.w3.org/XML/1998/namespace}lang")
            if lang:
                new_abstract.set("lang", lang)

            new_abstract.text = abstract.text

        # Process accessCondition
        for access in metadata.findall("./mods:accessCondition", namespaces=namespaces):
            new_access = ET.SubElement(new_record, "accessCondition")

            access_type = access.get("type")
            if access_type:
                new_access.set("type", access_type)

            new_access.text = access.text if access.text else ""

    # Add resumptionToken if present in original
    resumption = root.find(".//oai:resumptionToken", namespaces=namespaces)
    if resumption is not None:
        new_token = ET.SubElement(new_root, "resumptionToken")
        new_token.text = resumption.text

        # Copy attributes
        for attr, value in resumption.attrib.items():
            new_token.set(attr, value)

    # Write to output file
    output_tree = ET.ElementTree(new_root)
    output_tree.write(
        output_file, pretty_print=True, encoding="UTF-8", xml_declaration=False
    )
    print(f"Successfully transformed XML from {input_file} to {output_file}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python transform_pure_data_final.py <input_file> <output_file>")
        sys.exit(1)

    transform_xml(sys.argv[1], sys.argv[2])
