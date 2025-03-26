---
title: "Product — OpenAIRE Guidelines for CRIS Managers 1.2.0 documentation"
source: "https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/cerif_xml_product_entity.html"
---

| Description: | Any result of research other than Publication or Patent. This includes: (1) research datasets, (2) software, (3) visualisations: still or moving images, including maps and other cartographic material, (4) audio recordings, (5) other objects that can be perceived through human senses. |
| --- | --- |
| Examples: | [openaire\_cerif\_xml\_example\_products.xml](https://github.com/openaire/guidelines-cris-managers/blob/v1.2/samples/openaire_cerif_xml_example_products.xml) |
| Representation: | XML element `Product`; the rest of this section documents children of this element |
| CERIF: | the ResultProduct entity ([https://w3id.org/cerif/model#ResultProduct](https://w3id.org/cerif/model#ResultProduct)) |

## Internal Identifier[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#internal-identifier "Permalink to this headline")

| Use: | mandatory (1) in top level entity. When embedded in other entities the Internal Identifier must be included only for managed information (i.e. entities that have a concrete record in the local CRIS system). See [Metadata representation in CERIF XML](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/implementation.html#metadata-representation-in-cerif-xml) |
| --- | --- |
| Representation: | XML attribute `id` |
| CERIF: | the ResultProductIdentifier attribute ([https://w3id.org/cerif/model#ResultProduct.ResultProductIdentifier](https://w3id.org/cerif/model#ResultProduct.ResultProductIdentifier)) |

## Type[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#type "Permalink to this headline")

| Description: | The type of the resulting product (other than publication or patent) |
| --- | --- |
| Use: | mandatory (1) |
| Representation: | XML element `Type` from namespace [https://www.openaire.eu/cerif-profile/vocab/COAR\_Product\_Types](https://www.openaire.eu/cerif-profile/vocab/COAR_Product_Types) |
| CERIF: | the ResultProduct\_Classification ([https://w3id.org/cerif/model#ResultProduct\_Classification](https://w3id.org/cerif/model#ResultProduct_Classification)) |
| Vocabulary: | Product types extracted from the COAR Resource Types concept scheme: Types of products as extracted from the COAR Resource Types concept scheme ([https://vocabularies.coar-repositories.org/resource\_types/](https://vocabularies.coar-repositories.org/resource_types/), all types that do not descend from ‘text’).  - **cartographic material** ([http://purl.org/coar/resource\_type/c\_12cc](http://purl.org/coar/resource_type/c_12cc)): Any material representing the whole or part of the earth or any celestial body at any scale. Cartographic materials include two- and three-dimensional maps and plans (including maps of imaginary places); aeronautical, navigational, and celestial charts; atlases; globes; block diagrams; sections; aerial photographs with a cartographic purpose; bird’s-eye views (map views), etc. \[Source: [http://www.loc.gov/marc/cfmap.html](http://www.loc.gov/marc/cfmap.html)\] 	- **map** ([http://purl.org/coar/resource\_type/c\_12cd](http://purl.org/coar/resource_type/c_12cd)): Defined as a representation normally to scale and on a flat medium, of a selection of material or abstract features on, or in relation to, the surface of the earth or of another celestial body. \[Source: [https://www.loc.gov/marc/bibliographic/bd007a.html](https://www.loc.gov/marc/bibliographic/bd007a.html)\] - **dataset** ([http://purl.org/coar/resource\_type/c\_ddb1](http://purl.org/coar/resource_type/c_ddb1)): A collection of related facts and data encoded in a defined structure. \[Source: Adapted from [http://purl.org/spar/fabio/Dataset](http://purl.org/spar/fabio/Dataset)\] 	- **aggregated data** ([http://purl.org/coar/resource\_type/ACF7-8YT9](http://purl.org/coar/resource_type/ACF7-8YT9)): Statistics that relate to broad classes, groups, or categories. The data are averaged, totaled, or otherwise derived from individual-level data, and it is no longer possible to distinguish the characteristics of individuals within those classes, groups, or categories. For example, the number and age group of the unemployed in specific geographic regions, or national level statistics on the occurrence of specific offences, originally derived from the statistics of individual police districts. \[Source: [https://ddialliance.org/Specification/DDI-CV/ModeOfCollection\_3.0.html](https://ddialliance.org/Specification/DDI-CV/ModeOfCollection_3.0.html)\] 	- **clinical trial data** ([http://purl.org/coar/resource\_type/c\_cb28](http://purl.org/coar/resource_type/c_cb28)): Data resulting from a research study in which one or more human subjects are prospectively assigned to one or more interventions (which may include placebo or other control) to evaluate the effects of those interventions on health-related biomedical or behavioral outcomes. \[Source: Adapted from [https://grants.nih.gov/policy/clinical-trials/definition.htm](https://grants.nih.gov/policy/clinical-trials/definition.htm)\] 	- **compiled data** ([http://purl.org/coar/resource\_type/FXF3-D3G7](http://purl.org/coar/resource_type/FXF3-D3G7)): Data collected or assembled from multiple, often heterogeneous sources that have one or more reference points in common, and at least one of the sources was originally produced for other purposes. The data are incorporated in a new entity. For example, providing data on the number of universities in the last 150 years using a variety of available sources (e.g. finance documents, official statistics, university registers), combining survey data with information about geographical areas from official statistics (e.g. population density, doctors per capita, etc.), or using RSS to collect blog posts or tweets, etc. \[Source: Adapted from [https://ddialliance.org/Specification/DDI-CV/ModeOfCollection\_3.0.html](https://ddialliance.org/Specification/DDI-CV/ModeOfCollection_3.0.html)\] 	- **encoded data** ([http://purl.org/coar/resource\_type/AM6W-6QAW](http://purl.org/coar/resource_type/AM6W-6QAW)): Qualitative data (textual, video, audio or still-image) originally produced for other purposes into quantitative data (expressed in unit-by-variable matrices) by using coding techniques in accordance with pre-defined categorization schemes. For example, coded party manifesto data like the “European Parliament Election Study 2009, Manifesto Study” (doi:10.4232/1.10204)”. \[Source: Adapted from https://ddialliance.org/Specification/DDI-CV/ModeOfCollection\_3.0.html\] 	- **experimental data** ([http://purl.org/coar/resource\_type/63NG-B465](http://purl.org/coar/resource_type/63NG-B465)): Data resulting from the experimental research method involving the manipulation of some or all of the independent variables included in the hypotheses. \[Source: Adapted from [https://ddialliance.org/Specification/DDI-CV/ModeOfCollection\_3.0.html](https://ddialliance.org/Specification/DDI-CV/ModeOfCollection_3.0.html)\] 	- **genomic data** ([http://purl.org/coar/resource\_type/A8F1-NPV9](http://purl.org/coar/resource_type/A8F1-NPV9)): Genomic data refers to the genome and DNA data of an organism. They are used in bioinformatics for collecting, storing and processing the genomes of living things. Genomic data is a more extensive term than sequencing data. However genomic data mostly come from sequencing techniques. It may include non-sequencing data such as data from microarrays, data from real-time PCR panels and data from pharmacogenomics studies. \[Source: Adapted from [https://www.techopedia.com/definition/31247/genomic-data](https://www.techopedia.com/definition/31247/genomic-data)\] 	- **geospatial data** ([http://purl.org/coar/resource\_type/2H0M-X761](http://purl.org/coar/resource_type/2H0M-X761)): Geospatial data are any type of data with spatial coordinates that allow them to be mapped to the Earth’s surface. They can represent physical objects, discrete areas or continuous surfaces. Discrete geospatial data are usually represented using vector data consisting of points, lines and polygons, while continuous geospatial data are usually represented by raster data, consisting of a grid of cells that each has its own value. Any number of applications in a wide range of areas produce geospatial data, such as GIS, Remote Sensing equipment, GPS units, archaeological total stations, manual mapping and computer-aided design (CAD), in a number of formats, including images, vector, text, and tabular data. Vector-based geospatial data include tables listing archaeological sites along with their coordinates, text-based files (e.g., XML) containing coordinates and topology for historic road networks, voting figures for political parties by administrative area. Raster-based geospatial data include satellite images, aerial photographs, scanned maps, and digital maps of elevations, vegetation, land-use, sea surface temperatures, air pollution, soil-types, etc. \[Source: [https://ddialliance.org/Specification/DDI-CV/GeneralDataFormat\_2.0.html](https://ddialliance.org/Specification/DDI-CV/GeneralDataFormat_2.0.html)\] 	- **laboratory notebook** ([http://purl.org/coar/resource\_type/H41Y-FW7B](http://purl.org/coar/resource_type/H41Y-FW7B)): A laboratory notebook (colloq. lab notebook or lab book) is a primary record of research. Researchers use a lab notebook to document their hypotheses, experiments and initial analysis or interpretation of these experiments. This label is used both for traditional and electronic laboratory notebook. \[Source: Adapted from [https://en.wikipedia.org/wiki/Lab\_notebook](https://en.wikipedia.org/wiki/Lab_notebook)\] 	- **measurement and test data** ([http://purl.org/coar/resource\_type/DD58-GFSX](http://purl.org/coar/resource_type/DD58-GFSX)): Data resulting from assessing specific properties (or characteristics) of beings, things, phenomena, (and/ or processes) by applying pre-established standards and/or specialized instruments or techniques. \[Source: Adapted from [https://ddialliance.org/Specification/DDI-CV/ModeOfCollection\_3.0.html](https://ddialliance.org/Specification/DDI-CV/ModeOfCollection_3.0.html)\] 	- **observational data** ([http://purl.org/coar/resource\_type/FF4C-28RK](http://purl.org/coar/resource_type/FF4C-28RK)): Data resulting from observational research, which involves collecting observations as they occur (for example, observing behaviors, events, development of condition or disease, etc.), without attempting to manipulate any of the independent variables. \[Source: Adapted from [https://ddialliance.org/Specification/DDI-CV/ModeOfCollection\_3.0.html](https://ddialliance.org/Specification/DDI-CV/ModeOfCollection_3.0.html)\] 	- **recorded data** ([http://purl.org/coar/resource\_type/CQMR-7K63](http://purl.org/coar/resource_type/CQMR-7K63)): Data registered by mechanical or electronic means, in a form that allows the information to be retrieved and/or reproduced. For example, images or sounds on disc or magnetic tape. \[Source: Adapted from [https://ddialliance.org/Specification/DDI-CV/ModeOfCollection\_3.0.html](https://ddialliance.org/Specification/DDI-CV/ModeOfCollection_3.0.html)\] 	- **simulation data** ([http://purl.org/coar/resource\_type/W2XT-7017](http://purl.org/coar/resource_type/W2XT-7017)): Data resulting from modeling or imitative representation of real-world processes, events, or systems, often using computer programs. For example, a program modeling household consumption responses to indirect tax changes; or a dataset on hypothetical patients and their drug exposure, background conditions, and known adverse events. \[Source: Adapted from [https://ddialliance.org/Specification/DDI-CV/ModeOfCollection\_3.0.html](https://ddialliance.org/Specification/DDI-CV/ModeOfCollection_3.0.html)\] 	- **survey data** ([http://purl.org/coar/resource\_type/NHD0-W6SY](http://purl.org/coar/resource_type/NHD0-W6SY)): Data resulting from a survey, which is defined as an investigation about the characteristics of a given population by means of collecting data from a sample of that population and estimating their characteristics through the systematic use of statistical methodology. Included are censuses, sample surveys, the collection of data from administrative records and derived statistical activities as well as questionnaires. \[Source: Adapted from [https://stats.oecd.org/glossary/detail.asp?ID=2620](https://stats.oecd.org/glossary/detail.asp?ID=2620)\] - **design** ([http://purl.org/coar/resource\_type/542X-3S04](http://purl.org/coar/resource_type/542X-3S04)): Plans, drawing or set of drawings showing how something e.g. building, product is to be made and how it will work and look. \[Source: Adapted from [https://dictionary.cambridge.org/dictionary/english/design](https://dictionary.cambridge.org/dictionary/english/design)\] 	- **industrial design** ([http://purl.org/coar/resource\_type/JBNF-DYAD](http://purl.org/coar/resource_type/JBNF-DYAD)): Industrial designs are applied to a wide variety of industrial products and handicrafts. They refer to the ornamental or aesthetic aspects of a useful article,including compositions of lines or colors or any three-dimensional forms that give a special appearance to a product or handicraft. \[Source: [https://www.wipo.int/edocs/pubdocs/en/wipo\_pub\_943\_2018.pdf](https://www.wipo.int/edocs/pubdocs/en/wipo_pub_943_2018.pdf)\] 	- **layout design** ([http://purl.org/coar/resource\_type/BW7T-YM2G](http://purl.org/coar/resource_type/BW7T-YM2G)): Layout-design (topography) means the three-dimensional disposition, however expressed, of the elements of an integrated circuit (at least one of which is an active element) and of some or all of the interconnections of an integrated circuit, or such a three-dimensional disposition prepared for an integrated circuit intended for manufacture \[Source: [https://www.wipo.int/edocs/lexdocs/laws/en/hk/hk028en.pdf](https://www.wipo.int/edocs/lexdocs/laws/en/hk/hk028en.pdf)\] - **image** ([http://purl.org/coar/resource\_type/c\_c513](http://purl.org/coar/resource_type/c_c513)): A visual representation other than text, including all types of moving image and still image. \[Source: Adapted from [http://purl.org/dc/dcmitype/Image](http://purl.org/dc/dcmitype/Image)\] 	- **moving image** ([http://purl.org/coar/resource\_type/c\_8a7e](http://purl.org/coar/resource_type/c_8a7e)): A moving display, either generated dynamically by a computer program or formed from a series of pre-recorded still images imparting an impression of motion when shown in succession. \[Source: [http://purl.org/spar/fabio/MovingImage](http://purl.org/spar/fabio/MovingImage)\] 		- **video** ([http://purl.org/coar/resource\_type/c\_12ce](http://purl.org/coar/resource_type/c_12ce)): A recording of visual images, usually in motion and with sound accompaniment. \[Source: [http://www.ifla.org/files/assets/cataloguing/isbd/isbd-cons\_20110321.pdf](http://www.ifla.org/files/assets/cataloguing/isbd/isbd-cons_20110321.pdf) \] 	- **still image** ([http://purl.org/coar/resource\_type/c\_ecc8](http://purl.org/coar/resource_type/c_ecc8)): A recorded static visual representation. This class of image includes diagrams, drawings, graphs, graphic designs, plans, photographs and prints. \[Source: Adapted from [http://purl.org/spar/fabio/StillImage](http://purl.org/spar/fabio/StillImage)\] - **interactive resource** ([http://purl.org/coar/resource\_type/c\_e9a0](http://purl.org/coar/resource_type/c_e9a0)): A resource requiring interaction from the user to be understood, executed, or experienced. Examples include forms on Web pages, applets, multimedia learning objects, chat services, or virtual reality environments. Source: [http://purl.org/dc/dcmitype/InteractiveResource](http://purl.org/dc/dcmitype/InteractiveResource) 	- **website** ([http://purl.org/coar/resource\_type/c\_7ad9](http://purl.org/coar/resource_type/c_7ad9)): A collection of related web pages containing text, images, videos and/or other digital assets that are addressed relative to a common Uniform Resource Locator (URL). A web site is hosted on at least one web server, accessible via a network such as the Internet or a private local area network. \[Source: [http://purl.org/spar/fabio/WebSite](http://purl.org/spar/fabio/WebSite)\] - **learning object** ([http://purl.org/coar/resource\_type/c\_e059](http://purl.org/coar/resource_type/c_e059)): A digital resource that can be reused to enhance teaching and learning. \[Source: [https://icas-ca.org/archive/projects/coerc/oer-glossary](https://icas-ca.org/archive/projects/coerc/oer-glossary)\] - **other** ([http://purl.org/coar/resource\_type/c\_1843](http://purl.org/coar/resource_type/c_1843)): A resource type that is not included in existing terms. \[COAR definition\] - **software** ([http://purl.org/coar/resource\_type/c\_5ce6](http://purl.org/coar/resource_type/c_5ce6)): A computer program in source code (text) or compiled form. \[Source: [http://purl.org/dc/dcmitype/Software](http://purl.org/dc/dcmitype/Software)\] 	- **research software** ([http://purl.org/coar/resource\_type/c\_c950](http://purl.org/coar/resource_type/c_c950)): Software that is used to generate, process or analyse results that you intend to appear in a publication (either in a journal, conference paper, monograph, book or thesis). Research software can be anything from a few lines of code written by yourself, to a professionally developed software package. \[Source: [https://datashare.ed.ac.uk/handle/10283/785](https://datashare.ed.ac.uk/handle/10283/785)\] 	- **source code** ([http://purl.org/coar/resource\_type/QH80-2R4E](http://purl.org/coar/resource_type/QH80-2R4E)): Source code is any collection of code, with or without comments, written using a human-readable programming language, usually as plain text. \[Source: [https://en.wikipedia.org/wiki/Source\_code](https://en.wikipedia.org/wiki/Source_code)\] - **sound** ([http://purl.org/coar/resource\_type/c\_18cc](http://purl.org/coar/resource_type/c_18cc)): A resource primarily intended to be heard. Examples include a music playback file format, an audio compact disc, and recorded speech or sounds. \[Source: [http://dublincore.org/documents/dcmi-terms/#dcmitype-Sound](http://dublincore.org/documents/dcmi-terms/#dcmitype-Sound)\] 	- **musical composition** ([http://purl.org/coar/resource\_type/c\_18cd](http://purl.org/coar/resource_type/c_18cd)): Musical composition can refer to an original piece of music, the structure of a musical piece, or the process of creating a new piece of music. \[Source: [https://en.wikipedia.org/wiki/Musical\_composition](https://en.wikipedia.org/wiki/Musical_composition) \] - **trademark** ([http://purl.org/coar/resource\_type/H6QP-SC1X](http://purl.org/coar/resource_type/H6QP-SC1X)): A sign used to distinguish the goods or services of one undertaking from those of others. A trademark may consist of words and combinations of words (for instance, names or slogans), logos, figures and images, letters, numbers, sounds, or, in rare instances, smells or moving images, or a combination thereof. \[Source: [https://www.wipo.int/trademarks/en](https://www.wipo.int/trademarks/en)\] - **workflow** ([http://purl.org/coar/resource\_type/c\_393c](http://purl.org/coar/resource_type/c_393c)): A recorded sequence of connected steps, which may be automated, specifying a reliably repeatable sequence of operations to be undertaken when conducting a particular job, for example an in silico investigation that extracts and processes information from a number of bioinformatics databases. \[Source: Adapted from [http://purl.org/spar/fabio/Workflow](http://purl.org/spar/fabio/Workflow)\] |

## Language[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#language "Permalink to this headline")

| Description: | The language or languages of the product, if applicable. Please use the IETF language tags as described in the IETF BCP 47 document. |
| --- | --- |
| Use: | optional, possibly multiple (0..\*) |
| Representation: | XML element `Language` |
| CERIF: | the ResultProduct\_Classification linking entity ([https://w3id.org/cerif/model#ResultProduct\_Classification](https://w3id.org/cerif/model#ResultProduct_Classification)) with the [http://publications.europa.eu/resource/authority/language](http://publications.europa.eu/resource/authority/language) semantics |

## Name[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#name "Permalink to this headline")

| Use: | optional, possibly multiple (0..\*) |
| --- | --- |
| Representation: | XML element `Name` as a multilingual string |
| CERIF: | the ResultProduct.Name attribute ([https://w3id.org/cerif/model#ResultProduct.Name](https://w3id.org/cerif/model#ResultProduct.Name)) |

## VersionInfo[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#versioninfo "Permalink to this headline")

| Use: | optional, possibly multiple (0..\*) |
| --- | --- |
| Representation: | XML element `VersionInfo` as a multilingual string |
| CERIF: | the ResultProduct.VersionInfo attribute ([https://w3id.org/cerif/model#ResultProduct.VersionInfo](https://w3id.org/cerif/model#ResultProduct.VersionInfo)) |

## ARK[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#ark "Permalink to this headline")

| Use: | optional (0..1) |
| --- | --- |
| Representation: | XML element `ARK` |
| CERIF: | the FederatedIdentifier entity ([https://w3id.org/cerif/model#FederatedIdentifier](https://w3id.org/cerif/model#FederatedIdentifier)) |

## DOI[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#doi "Permalink to this headline")

| Description: | The Digital Object Identifier |
| --- | --- |
| Use: | optional (0..1) |
| Representation: | XML element `DOI` |
| CERIF: | the FederatedIdentifier entity ([https://w3id.org/cerif/model#FederatedIdentifier](https://w3id.org/cerif/model#FederatedIdentifier)) |
| Format: | regular expression `10\.\d{4,}(\.\d+)*/[^\s]+` (as per [https://www.crossref.org/blog/dois-and-matching-regular-expressions/](https://www.crossref.org/blog/dois-and-matching-regular-expressions/)) |

## Handle[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#handle "Permalink to this headline")

| Use: | optional (0..1) |
| --- | --- |
| Representation: | XML element `Handle` |
| CERIF: | the FederatedIdentifier entity ([https://w3id.org/cerif/model#FederatedIdentifier](https://w3id.org/cerif/model#FederatedIdentifier)) |

## URL[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#url "Permalink to this headline")

| Use: | optional (0..1) |
| --- | --- |
| Representation: | XML element `URL` |
| CERIF: | the FederatedIdentifier entity ([https://w3id.org/cerif/model#FederatedIdentifier](https://w3id.org/cerif/model#FederatedIdentifier)) |

## URN[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#urn "Permalink to this headline")

| Use: | optional (0..1) |
| --- | --- |
| Representation: | XML element `URN` |
| CERIF: | the FederatedIdentifier entity ([https://w3id.org/cerif/model#FederatedIdentifier](https://w3id.org/cerif/model#FederatedIdentifier)) |

## Creators[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#creators "Permalink to this headline")

| Description: | The creators of this product |
| --- | --- |
| Use: | optional (0..1) |
| Representation: | XML element `Creators` with ordered embedded XML elements `Creator` that can contain an embedded person with affiliations or organisation unit |

### Creator[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#creator "Permalink to this headline")

| Use: | optional, possibly multiple (0..\*) |
| --- | --- |
| Representation: | XML element `Creator` with embedded XML element `Person` optionally followed by one or several `Affiliation` elements, or `OrgUnit`. A `DisplayName` may be specified, too. |
| CERIF: | the Person\_ResultProduct linking entity ([https://w3id.org/cerif/model#Person\_ResultProduct](https://w3id.org/cerif/model#Person_ResultProduct)) with the [https://w3id.org/cerif/vocab/PersonOutputContributions#Creator](https://w3id.org/cerif/vocab/PersonOutputContributions#Creator) semantics; the OrganisationUnit\_ResultProduct linking entity ([https://w3id.org/cerif/model#OrganisationUnit\_ResultProduct](https://w3id.org/cerif/model#OrganisationUnit_ResultProduct)) with the [https://w3id.org/cerif/vocab/OrganisationOutputContributions#Creator](https://w3id.org/cerif/vocab/OrganisationOutputContributions#Creator) semantics |

## Publishers[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#publishers "Permalink to this headline")

| Description: | The publisher or publishers of this product |
| --- | --- |
| Use: | optional (0..1) |
| Representation: | XML element `Publishers` with ordered embedded XML elements `Publisher` that can contain an embedded organisation unit or person |

### Publisher[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#publisher "Permalink to this headline")

| Use: | optional, possibly multiple (0..\*) |
| --- | --- |
| Representation: | XML element `Publisher` with embedded XML element `OrgUnit` or `Person`. A `DisplayName` may be specified, too. |
| CERIF: | the OrganisationUnit\_ResultProduct linking entity ([https://w3id.org/cerif/model#OrganisationUnit\_ResultProduct](https://w3id.org/cerif/model#OrganisationUnit_ResultProduct)) with the [https://w3id.org/cerif/vocab/OrganisationOutputContributions#Publisher](https://w3id.org/cerif/vocab/OrganisationOutputContributions#Publisher) semantics; the Person\_ResultProduct linking entity ([https://w3id.org/cerif/model#Person\_ResultProduct](https://w3id.org/cerif/model#Person_ResultProduct)) with the [https://w3id.org/cerif/vocab/PersonOutputContributions#Publisher](https://w3id.org/cerif/vocab/PersonOutputContributions#Publisher) semantics |

## License[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#license "Permalink to this headline")

| Description: | The license of the product. We recommend using URIs from the SPDX License List ([https://spdx.org/licenses/](https://spdx.org/licenses/)), which includes the licenses commonly used for software and datasets. |
| --- | --- |
| Use: | optional, possibly multiple (0..\*) |
| Representation: | XML element `License` containing the classification identifier and having a `scheme` attribute to specify the classification scheme identifier |
| CERIF: | the ResultProduct\_Classification ([https://w3id.org/cerif/model#ResultProduct\_Classification](https://w3id.org/cerif/model#ResultProduct_Classification)) |

## Description[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#description "Permalink to this headline")

| Use: | optional, possibly multiple (0..\*) |
| --- | --- |
| Representation: | XML element `Description` as a multilingual string |
| CERIF: | the ResultProduct.Description attribute ([https://w3id.org/cerif/model#ResultProduct.Description](https://w3id.org/cerif/model#ResultProduct.Description)) |

## Subject[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#subject "Permalink to this headline")

| Description: | The subject of the product from a classification |
| --- | --- |
| Use: | optional, possibly multiple (0..\*) |
| Representation: | XML element `Subject` containing the classification identifier and having a `scheme` attribute to specify the classification scheme identifier |
| CERIF: | the ResultProduct\_Classification ([https://w3id.org/cerif/model#ResultProduct\_Classification](https://w3id.org/cerif/model#ResultProduct_Classification)) |

## Keyword[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#keyword "Permalink to this headline")

| Description: | A single keyword or key expression. Please repeat to serialize separate keywords or key expressions. |
| --- | --- |
| Use: | optional, possibly multiple (0..\*) |
| Representation: | XML element `Keyword` as a multilingual string |
| CERIF: | the ResultProduct.Keywords attribute ([https://w3id.org/cerif/model#ResultProduct.Keywords](https://w3id.org/cerif/model#ResultProduct.Keywords)) |

## PartOf[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#partof "Permalink to this headline")

| Description: | Link to the research output of which this product is a part (e.g. a data set collection that contains it) |
| --- | --- |
| Use: | optional (0..1) |
| Representation: | XML element `PartOf` with embedded XML element `Publication` or `Patent` or `Product` |
| CERIF: | the ResultProduct\_ResultProduct linking entity ([https://w3id.org/cerif/model#ResultProduct\_ResultProduct](https://w3id.org/cerif/model#ResultProduct_ResultProduct)) with the [https://w3id.org/cerif/vocab/InterProductRelations#Part](https://w3id.org/cerif/vocab/InterProductRelations#Part) semantics (direction :1) |

## OriginatesFrom[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#originatesfrom "Permalink to this headline")

| Use: | optional, possibly multiple (0..\*) |
| --- | --- |
| Representation: | XML element `OriginatesFrom` with embedded XML element `Project` or `Funding` |
| CERIF: | the Project\_ResultProduct linking entity ([https://w3id.org/cerif/model#Project\_ResultProduct](https://w3id.org/cerif/model#Project_ResultProduct)) with the [https://w3id.org/cerif/vocab/ProjectOutputRoles#Originator](https://w3id.org/cerif/vocab/ProjectOutputRoles#Originator) semantics; the ResultProduct\_Funding linking entity ([https://w3id.org/cerif/model#ResultProduct\_Funding](https://w3id.org/cerif/model#ResultProduct_Funding)) with the [https://w3id.org/cerif/vocab/OutputFundingRoles#Originator](https://w3id.org/cerif/vocab/OutputFundingRoles#Originator) semantics |

## GeneratedBy[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#generatedby "Permalink to this headline")

| Description: | The equipment that generated this product |
| --- | --- |
| Use: | optional, possibly multiple (0..\*) |
| Representation: | XML element `GeneratedBy` with embedded XML element `Equipment` |
| CERIF: | the ResultProduct\_Equipment linking entity ([https://w3id.org/cerif/model#ResultProduct\_Equipment](https://w3id.org/cerif/model#ResultProduct_Equipment)) with the [https://w3id.org/cerif/vocab/OutputResearchInfrastructureRelations#Generation](https://w3id.org/cerif/vocab/OutputResearchInfrastructureRelations#Generation) semantics |

## PresentedAt[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#presentedat "Permalink to this headline")

| Description: | The event where this product was presented |
| --- | --- |
| Use: | optional, possibly multiple (0..\*) |
| Representation: | XML element `PresentedAt` with embedded XML element `Event` |
| CERIF: | the ResultProduct\_Event linking entity ([https://w3id.org/cerif/model#ResultProduct\_Event](https://w3id.org/cerif/model#ResultProduct_Event)) with the [https://w3id.org/cerif/vocab/EventOutputRelationships#Presented](https://w3id.org/cerif/vocab/EventOutputRelationships#Presented) semantics |

## Coverage[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#coverage "Permalink to this headline")

| Description: | The event that is covered by this product (e.g. a video or audio interview about the event) |
| --- | --- |
| Use: | optional, possibly multiple (0..\*) |
| Representation: | XML element `Coverage` with embedded XML element `Event` |
| CERIF: | the ResultProduct\_Event linking entity ([https://w3id.org/cerif/model#ResultProduct\_Event](https://w3id.org/cerif/model#ResultProduct_Event)) with the [https://w3id.org/cerif/vocab/EventOutputRelationships#Coverage](https://w3id.org/cerif/vocab/EventOutputRelationships#Coverage) semantics |

## References[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#references "Permalink to this headline")

| Description: | Result outputs that are referenced by this product |
| --- | --- |
| Use: | optional, possibly multiple (0..\*) |
| Representation: | XML element `References` with embedded XML element `Publication` or `Patent` or `Product` |
| CERIF: | the ResultPublication\_ResultProduct linking entity ([https://w3id.org/cerif/model#ResultPublication\_ResultProduct](https://w3id.org/cerif/model#ResultPublication_ResultProduct)) with the [https://w3id.org/cerif/vocab/InterOutputRelations#Reference](https://w3id.org/cerif/vocab/InterOutputRelations#Reference) semantics (direction :1); the ResultProduct\_ResultProduct linking entity ([https://w3id.org/cerif/model#ResultProduct\_ResultProduct](https://w3id.org/cerif/model#ResultProduct_ResultProduct)) with the [https://w3id.org/cerif/vocab/InterOutputRelations#Reference](https://w3id.org/cerif/vocab/InterOutputRelations#Reference) semantics (direction :1); the ResultProduct\_ResultPatent linking entity ([https://w3id.org/cerif/model#ResultProduct\_ResultPatent](https://w3id.org/cerif/model#ResultProduct_ResultPatent)) with the [https://w3id.org/cerif/vocab/InterOutputRelations#Reference](https://w3id.org/cerif/vocab/InterOutputRelations#Reference) semantics (direction :1) |

## ns4:Access[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#ns4-access "Permalink to this headline")

| Description: | The open access type of the product |
| --- | --- |
| Use: | optional (0..1) |
| Representation: | XML element `Access` from namespace [http://purl.org/coar/access\_right](http://purl.org/coar/access_right) |
| CERIF: | the ResultProduct\_Classification ([https://w3id.org/cerif/model#ResultProduct\_Classification](https://w3id.org/cerif/model#ResultProduct_Classification)) |
| Vocabulary: | - **open access** ([http://purl.org/coar/access\_right/c\_abf2](http://purl.org/coar/access_right/c_abf2)): Open access refers to a resource that is immediately and permanently online, and free for all on the Web, without financial and technical barriers.The resource is either stored in the repository or referenced to an external journal or trustworthy archive. - **embargoed access** ([http://purl.org/coar/access\_right/c\_f1cf](http://purl.org/coar/access_right/c_f1cf)): Embargoed access refers to a resource that is metadata only access until released for open access on a certain date. Embargoes can be required by publishers and funders policies, or set by the author (e.g such as in the case of theses and dissertations). - **restricted access** ([http://purl.org/coar/access\_right/c\_16ec](http://purl.org/coar/access_right/c_16ec)): Restricted access refers to a resource that is available in a system but with some type of restriction for full open access. This type of access can occur in a number of different situations. Some examples are described below: The user must log-in to the system in order to access the resource The user must send an email to the author or system administrator to access the resource Access to the resource is restricted to a specific community (e.g. limited to a university community) - **metadata only access** ([http://purl.org/coar/access\_right/c\_14cb](http://purl.org/coar/access_right/c_14cb)): Metadata only access refers to a resource in which access is limited to metadata only. The resource itself is described by the metadata, but neither is directly available through the system or platform nor can be referenced to an open access copy in an external journal or trustworthy archive. |

## Dates[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#dates "Permalink to this headline")

| Description: | Dates or date ranges to describe temporal aspects of the product. Semantically follows the dateType construct from the DataCite Metadata Schema 4.4. If an embargo period is to be expressed, its start should be expressed by the `startDate` on `Submitted` or `Accepted` (as appropriate) and end is represented by the `startDate` on `Available`. |
| --- | --- |
| Use: | optional (0..1) |
| Representation: | XML element `Dates` with embedded XML elements `Accepted` or `Available` or `Copyrighted` or `Collected` or `Created` or `Issued` or `Submitted` or `Updated` or `Valid` or `Withdrawn` from the shared structure [DatesStructure\_\_Group](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/cerif_xml_common__datesstructure__group.html#cerif-xml-common-datesstructure-group) |

## FileLocations[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#filelocations "Permalink to this headline")

| Description: | The files that this Product has as contents. |
| --- | --- |
| Use: | optional (0..1) |
| Representation: | XML element `FileLocations` with embedded XML element `Medium` |
| CERIF: | the ResultProduct\_Medium linking entity ([https://w3id.org/cerif/model#ResultProduct\_Medium](https://w3id.org/cerif/model#ResultProduct_Medium)) with the [https://w3id.org/cerif/vocab/MediaRelations#Contents](https://w3id.org/cerif/vocab/MediaRelations#Contents) semantics |
