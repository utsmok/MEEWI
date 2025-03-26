---
title: "Person — OpenAIRE Guidelines for CRIS Managers 1.2.0 documentation"
source: "https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/cerif_xml_person_entity.html"
---
| Description: | A human being as an individual. Source: [https://en.oxforddictionaries.com/definition/person](https://en.oxforddictionaries.com/definition/person) The kind of involvement of a Person in the research ecosystem is specified in the links with the organisations, the services, etc. This typically includes: (1) researchers (Persons performing research in an Organisation Unit as employees or students); (2) authors and contributors (Persons signing a publication, creators of data sets, software developers, etc.); (3) investigators and project participants (Persons involved in a Project as principal investigators, co investigators, project managers, consultants, etc.); (4) management (directors, rectors, deans, department heads, etc.); (5) support staffs (technicians, responsible for Equipment, librarians and digital asset curators, administrative staff, etc.). One Person typically has many of these relationships. |
| --- | --- |
| Examples: | [openaire\_cerif\_xml\_example\_persons.xml](https://github.com/openaire/guidelines-cris-managers/blob/v1.2/samples/openaire_cerif_xml_example_persons.xml) |
| Representation: | XML element `Person`; the rest of this section documents children of this element |
| CERIF: | the Person entity ([https://w3id.org/cerif/model#Person](https://w3id.org/cerif/model#Person)) |

## Internal Identifier[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#internal-identifier "Permalink to this headline")

| Use: | mandatory (1) in top level entity. When embedded in other entities the Internal Identifier must be included only for managed information (i.e. entities that have a concrete record in the local CRIS system). See [Metadata representation in CERIF XML](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/implementation.html#metadata-representation-in-cerif-xml) |
| --- | --- |
| Representation: | XML attribute `id` |
| CERIF: | the PersonIdentifier attribute ([https://w3id.org/cerif/model#Person.PersonIdentifier](https://w3id.org/cerif/model#Person.PersonIdentifier)) |

## PersonName[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#personname "Permalink to this headline")

| Description: | The name of the person |
| --- | --- |
| Use: | optional (0..1) |
| Representation: | XML element `PersonName` containing optional `FamilyNames`, optional `FirstNames` and optional `OtherNames` |
| CERIF: | the PersonName entity ([https://w3id.org/cerif/model#PersonName](https://w3id.org/cerif/model#PersonName)) and the corresponding link ([https://w3id.org/cerif/model#Person\_PersonName](https://w3id.org/cerif/model#Person_PersonName)) |

### FamilyNames[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#familynames "Permalink to this headline")

| Use: | optional (0..1) |
| --- | --- |
| Representation: | XML element `FamilyNames` |
| CERIF: | the PersonName.FamilyNames attribute ([https://w3id.org/cerif/model#PersonName.FamilyNames](https://w3id.org/cerif/model#PersonName.FamilyNames)) |

### FirstNames[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#firstnames "Permalink to this headline")

| Use: | optional (0..1) |
| --- | --- |
| Representation: | XML element `FirstNames` |
| CERIF: | the PersonName.FirstNames attribute ([https://w3id.org/cerif/model#PersonName.FirstNames](https://w3id.org/cerif/model#PersonName.FirstNames)) |

### OtherNames[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#othernames "Permalink to this headline")

| Use: | optional (0..1) |
| --- | --- |
| Representation: | XML element `OtherNames` |
| CERIF: | the PersonName.OtherNames attribute ([https://w3id.org/cerif/model#PersonName.OtherNames](https://w3id.org/cerif/model#PersonName.OtherNames)) |

## Gender[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#gender "Permalink to this headline")

| Description: | The gender of the person. Leave out in case the gender is unknown or not communicated. |
| --- | --- |
| Use: | optional (0..1) |
| Representation: | XML element `Gender` |
| CERIF: | the Person.Gender attribute ([https://w3id.org/cerif/model#Person.Gender](https://w3id.org/cerif/model#Person.Gender)) |
| Vocabulary: | Genders (sociocultural, not linguistic)  - **Masculine** (`m`): - **Feminine** (`f`): |

## ORCID[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#orcid "Permalink to this headline")

| Description: | The ORCID identifier in case its value is certain or known to be a preferred one. |
| --- | --- |
| Use: | optional (0..1) |
| Representation: | XML element `ORCID` |
| CERIF: | the FederatedIdentifier entity ([https://w3id.org/cerif/model#FederatedIdentifier](https://w3id.org/cerif/model#FederatedIdentifier)) |
| Format: | any of:  - regular expression `https://orcid\.org/0000-000(1-[5-9]\|2-[0-9]\|3-[0-4])[0-9]{3}-[0-9]{3}[0-9X]` (The original block of 20M identifiers reserved in 2013, as per [https://support.orcid.org/knowledgebase/articles/116780-structure-of-the-orcid-identifier](https://support.orcid.org/knowledgebase/articles/116780-structure-of-the-orcid-identifier)) - regular expression `https://orcid\.org/0009-000[0-9]-[0-9]{4}-[0-9]{3}[0-9X]` (An additional block of 100M identifiers reserved in 2023, as per [https://support.orcid.org/knowledgebase/articles/116780-structure-of-the-orcid-identifier](https://support.orcid.org/knowledgebase/articles/116780-structure-of-the-orcid-identifier)) |

## AlternativeORCID[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#alternativeorcid "Permalink to this headline")

| Description: | The ORCID identifiers in case the value is not certain, e.g. because there is a conflicting statement with a different value. This can also represent deprecated identifiers/profiles that have been merged into a single, current one that is preferred. |
| --- | --- |
| Use: | optional, possibly multiple (0..\*) |
| Representation: | XML element `AlternativeORCID` |
| CERIF: | the FederatedIdentifier entity ([https://w3id.org/cerif/model#FederatedIdentifier](https://w3id.org/cerif/model#FederatedIdentifier)) |
| Format: | any of:  - regular expression `https://orcid\.org/0000-000(1-[5-9]\|2-[0-9]\|3-[0-4])[0-9]{3}-[0-9]{3}[0-9X]` (The original block of 20M identifiers reserved in 2013, as per [https://support.orcid.org/knowledgebase/articles/116780-structure-of-the-orcid-identifier](https://support.orcid.org/knowledgebase/articles/116780-structure-of-the-orcid-identifier)) - regular expression `https://orcid\.org/0009-000[0-9]-[0-9]{4}-[0-9]{3}[0-9X]` (An additional block of 100M identifiers reserved in 2023, as per [https://support.orcid.org/knowledgebase/articles/116780-structure-of-the-orcid-identifier](https://support.orcid.org/knowledgebase/articles/116780-structure-of-the-orcid-identifier)) |

## ResearcherID[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#researcherid "Permalink to this headline")

| Description: | The ResearcherID identifier in case its value is certain or known to be a preferred one. |
| --- | --- |
| Use: | optional (0..1) |
| Representation: | XML element `ResearcherID` |
| CERIF: | the FederatedIdentifier entity ([https://w3id.org/cerif/model#FederatedIdentifier](https://w3id.org/cerif/model#FederatedIdentifier)) |
| Format: | regular expression `[A-Z]{1,3}-[0-9]{4}-(19\|20)[0-9][0-9]` (as per [https://www.wikidata.org/wiki/Property:P1053](https://www.wikidata.org/wiki/Property:P1053)) |

## AlternativeResearcherID[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#alternativeresearcherid "Permalink to this headline")

| Description: | The ResearcherID identifier in case the value is not certain, e.g. because there is a conflicting statement with a different value. This can also represent deprecated identifiers/profiles that have been merged into a single, current one that is preferred. |
| --- | --- |
| Use: | optional, possibly multiple (0..\*) |
| Representation: | XML element `AlternativeResearcherID` |
| CERIF: | the FederatedIdentifier entity ([https://w3id.org/cerif/model#FederatedIdentifier](https://w3id.org/cerif/model#FederatedIdentifier)) |
| Format: | regular expression `[A-Z]{1,3}-[0-9]{4}-(19\|20)[0-9][0-9]` (as per [https://www.wikidata.org/wiki/Property:P1053](https://www.wikidata.org/wiki/Property:P1053)) |

## ScopusAuthorID[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#scopusauthorid "Permalink to this headline")

| Description: | The Scopus Author ID identifier in case its value is certain or known to be a preferred one. |
| --- | --- |
| Use: | optional (0..1) |
| Representation: | XML element `ScopusAuthorID` |
| CERIF: | the FederatedIdentifier entity ([https://w3id.org/cerif/model#FederatedIdentifier](https://w3id.org/cerif/model#FederatedIdentifier)) |
| Format: | regular expression `[0-9]{10,11}` (as per [https://www.wikidata.org/wiki/Property:P1153](https://www.wikidata.org/wiki/Property:P1153)) |

## AlternativeScopusAuthorID[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#alternativescopusauthorid "Permalink to this headline")

| Description: | The Scopus Author ID identifier in case the value is not certain, e.g. because there is a conflicting statement with a different value. This can also represent deprecated identifiers/profiles that have been merged into a single, current one that is preferred. |
| --- | --- |
| Use: | optional, possibly multiple (0..\*) |
| Representation: | XML element `AlternativeScopusAuthorID` |
| CERIF: | the FederatedIdentifier entity ([https://w3id.org/cerif/model#FederatedIdentifier](https://w3id.org/cerif/model#FederatedIdentifier)) |
| Format: | regular expression `[0-9]{10,11}` (as per [https://www.wikidata.org/wiki/Property:P1153](https://www.wikidata.org/wiki/Property:P1153)) |

## ISNI[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#isni "Permalink to this headline")

| Description: | The ISNI identifier in case its value is certain or known to be a preferred one. |
| --- | --- |
| Use: | optional (0..1) |
| Representation: | XML element `ISNI` |
| CERIF: | the FederatedIdentifier entity ([https://w3id.org/cerif/model#FederatedIdentifier](https://w3id.org/cerif/model#FederatedIdentifier)) |
| Format: | regular expression `\d{4} \d{4} \d{4} \d{3}[\dX]` (as per [https://www.wikidata.org/wiki/Property:P213](https://www.wikidata.org/wiki/Property:P213)) |

## AlternativeISNI[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#alternativeisni "Permalink to this headline")

| Description: | The ISNI identifier in case the value is not certain, e.g. because there is a conflicting statement with a different value. This can also represent deprecated identifiers/profiles that have been merged into a single, current one that is preferred. |
| --- | --- |
| Use: | optional, possibly multiple (0..\*) |
| Representation: | XML element `AlternativeISNI` |
| CERIF: | the FederatedIdentifier entity ([https://w3id.org/cerif/model#FederatedIdentifier](https://w3id.org/cerif/model#FederatedIdentifier)) |
| Format: | regular expression `\d{4} \d{4} \d{4} \d{3}[\dX]` (as per [https://www.wikidata.org/wiki/Property:P213](https://www.wikidata.org/wiki/Property:P213)) |

## DAI[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#dai "Permalink to this headline")

| Description: | The Digital Author Identifier in case its value is certain or known to be a preferred one. |
| --- | --- |
| Use: | optional (0..1) |
| Representation: | XML element `DAI` |
| CERIF: | the FederatedIdentifier entity ([https://w3id.org/cerif/model#FederatedIdentifier](https://w3id.org/cerif/model#FederatedIdentifier)) |
| Format: | regular expression `info\:eu\-repo/dai/nl/\d{8}[\dxX]` (as per [https://wiki.surfnet.nl/display/standards/DAI](https://wiki.surfnet.nl/display/standards/DAI)) |

## AlternativeDAI[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#alternativedai "Permalink to this headline")

| Description: | The Digital Author Identifier in case the value is not certain, e.g. because there is a conflicting statement with a different value. This can also represent deprecated identifiers/profiles that have been merged into a single, current one that is preferred. |
| --- | --- |
| Use: | optional, possibly multiple (0..\*) |
| Representation: | XML element `AlternativeDAI` |
| CERIF: | the FederatedIdentifier entity ([https://w3id.org/cerif/model#FederatedIdentifier](https://w3id.org/cerif/model#FederatedIdentifier)) |
| Format: | regular expression `info\:eu\-repo/dai/nl/\d{8}[\dxX]` (as per [https://wiki.surfnet.nl/display/standards/DAI](https://wiki.surfnet.nl/display/standards/DAI)) |

## Identifier[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#identifier "Permalink to this headline")

| Description: | A generic identifier, to be used only if your identifier does not fit in any of the above specific identifier types. This in particular applies to various national and service-specific identifiers that can be relevant in some interchange scenarios. |
| --- | --- |
| Use: | optional, possibly multiple (0..\*) |
| Representation: | XML element `Identifier` with a required `type` attribute (the URI of the identifier scheme) |
| CERIF: | the FederatedIdentifier entity ([https://w3id.org/cerif/model#FederatedIdentifier](https://w3id.org/cerif/model#FederatedIdentifier)) |

## ElectronicAddress[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#electronicaddress "Permalink to this headline")

| Description: | An electronic address associated with the person |
| --- | --- |
| Use: | optional, possibly multiple (0..\*) |
| Representation: | XML element `ElectronicAddress` |
| CERIF: | the ElectronicAddress entity ([https://w3id.org/cerif/model#ElectronicAddress](https://w3id.org/cerif/model#ElectronicAddress)) and the corresponding link ([https://w3id.org/cerif/model#Person\_ElectronicAddress](https://w3id.org/cerif/model#Person_ElectronicAddress)) |

## Affiliation[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#affiliation "Permalink to this headline")

| Description: | The organisation or organisation unit the person is affiliated with |
| --- | --- |
| Use: | optional, possibly multiple (0..\*) |
| Representation: | XML element `Affiliation` with embedded XML element `OrgUnit` |
| CERIF: | the Person\_OrganisationUnit linking entity ([https://w3id.org/cerif/model#Person\_OrganisationUnit](https://w3id.org/cerif/model#Person_OrganisationUnit)) with the [https://w3id.org/cerif/vocab/PersonOrganisationRoles#Affiliation](https://w3id.org/cerif/vocab/PersonOrganisationRoles#Affiliation) semantics |
