"""
oai-pmh returns XML data
structure is pretty simple, see below
Take note of the resumption token for pagination
if it's empty, the query is done

example response when calling
https://ris.utwente.nl/ws/oai?verb=ListRecords&set=openaire_cris_publications&metadataPrefix=oai_cerif_openaire

    <OAI-PMH>
        <responseDate>2025-03-21T23:10:52Z</responseDate>
        <request metadataPrefix="oai_cerif_openaire" set="openaire_cris_publications" verb="ListRecords">https://ris.utwente.nl/ws/oai</request>
        <ListRecords>

            [
                <record>
                -data truncated-
                </record>
            ] (100 records)

            <resumptionToken cursor="0" completeListSize="188091">
                oai_cerif_openaire/188091/485920704/100/0/5090373/openaire_cris_publications/x/x
            </resumptionToken>

        </ListRecords>
    </OAI-PMH>

the next request should then be:
https://ris.utwente.nl/ws/oai?verb=ListRecords&resumptionToken=oai_cerif_openaire/188091/485920704/100/0/5090373/openaire_cris_publications/x/x

there are multiple metadata formats available.
mods seems to have the most data
2nd choice is oai_cerif_openaire
other formats definitely have less data
"""

# use pydantic_xml to directly interact with xml data
# https://pydantic-xml.readthedocs.io/en/latest/pages/quickstart.html
