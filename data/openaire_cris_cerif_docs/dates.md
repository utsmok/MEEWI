---
title: "DatesStructure__Group  — OpenAIRE Guidelines for CRIS Managers 1.2.0 documentation"
source: "https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/cerif_xml_common__datesstructure__group_contents.html"
---

A `DatesStructure__Group` is a group of elements that describe the dates associated with a resource. The dates are represented as XML elements and are linked to the CERIF model.

| Description: | Use the `startDate` attribute for the date the publisher accepted the resource into their system. |
| --- | --- |
| Use: | optional (0..1) |
| Representation: | XML element `Accepted` |
| CERIF: | the ResultProduct\_Classification linking entity ([https://w3id.org/cerif/model#ResultProduct\_Classification](https://w3id.org/cerif/model#ResultProduct_Classification)) with the [https://w3id.org/cerif/vocab/DataCiteMetadataSchema\_DateType#Accepted](https://w3id.org/cerif/vocab/DataCiteMetadataSchema_DateType#Accepted) semantics |

# Available[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#available "Permalink to this headline")

| Description: | Use the `startDate` and possibly also `endDate` attributes for the dates the resource is or was publicly available. |
| --- | --- |
| Use: | optional (0..1) |
| Representation: | XML element `Available` |
| CERIF: | the ResultProduct\_Classification linking entity ([https://w3id.org/cerif/model#ResultProduct\_Classification](https://w3id.org/cerif/model#ResultProduct_Classification)) with the [https://w3id.org/cerif/vocab/DataCiteMetadataSchema\_DateType#Available](https://w3id.org/cerif/vocab/DataCiteMetadataSchema_DateType#Available) semantics |

# Copyrighted[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#copyrighted "Permalink to this headline")

| Description: | Use the `startDate` attribute to give the specific, documented date at which the resource receives a copyrighted status, if applicable |
| --- | --- |
| Use: | optional (0..1) |
| Representation: | XML element `Copyrighted` |
| CERIF: | the ResultProduct\_Classification linking entity ([https://w3id.org/cerif/model#ResultProduct\_Classification](https://w3id.org/cerif/model#ResultProduct_Classification)) with the [https://w3id.org/cerif/vocab/DataCiteMetadataSchema\_DateType#Copyrighted](https://w3id.org/cerif/vocab/DataCiteMetadataSchema_DateType#Copyrighted) semantics |

# Collected[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#collected "Permalink to this headline")

| Description: | Use the `startDate` and `endDate` attributes to describe the date range in which the resource content was collected. To indicate precise or particular timeframes in which research was conducted. |
| --- | --- |
| Use: | optional (0..1) |
| Representation: | XML element `Collected` |
| CERIF: | the ResultProduct\_Classification linking entity ([https://w3id.org/cerif/model#ResultProduct\_Classification](https://w3id.org/cerif/model#ResultProduct_Classification)) with the [https://w3id.org/cerif/vocab/DataCiteMetadataSchema\_DateType#Collected](https://w3id.org/cerif/vocab/DataCiteMetadataSchema_DateType#Collected) semantics |

# Created[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#created "Permalink to this headline")

| Description: | Use the `startDate` and `endDate` attributes to describe the date range in which the resource itself was put together. |
| --- | --- |
| Use: | optional (0..1) |
| Representation: | XML element `Created` |
| CERIF: | the ResultProduct\_Classification linking entity ([https://w3id.org/cerif/model#ResultProduct\_Classification](https://w3id.org/cerif/model#ResultProduct_Classification)) with the [https://w3id.org/cerif/vocab/DataCiteMetadataSchema\_DateType#Created](https://w3id.org/cerif/vocab/DataCiteMetadataSchema_DateType#Created) semantics |

# Issued[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#issued "Permalink to this headline")

| Description: | Use the `startDate` attribute for the date the resource was published or distributed, e.g. to a data centre. |
| --- | --- |
| Use: | optional (0..1) |
| Representation: | XML element `Issued` |
| CERIF: | the ResultProduct\_Classification linking entity ([https://w3id.org/cerif/model#ResultProduct\_Classification](https://w3id.org/cerif/model#ResultProduct_Classification)) with the [https://w3id.org/cerif/vocab/DataCiteMetadataSchema\_DateType#Issued](https://w3id.org/cerif/vocab/DataCiteMetadataSchema_DateType#Issued) semantics |

# Submitted[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#submitted "Permalink to this headline")

| Description: | Use the `startDate` attribute for the date the creator submits the resource to the publisher. This could be different from Accepted if the publisher then applies a selection process. |
| --- | --- |
| Use: | optional (0..1) |
| Representation: | XML element `Submitted` |
| CERIF: | the ResultProduct\_Classification linking entity ([https://w3id.org/cerif/model#ResultProduct\_Classification](https://w3id.org/cerif/model#ResultProduct_Classification)) with the [https://w3id.org/cerif/vocab/DataCiteMetadataSchema\_DateType#Submitted](https://w3id.org/cerif/vocab/DataCiteMetadataSchema_DateType#Submitted) semantics |

# Updated[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#updated "Permalink to this headline")

| Description: | Use the `startDate` and `endDate` attributes to describe the date range of the last update to the resource, when the resource is being added to. |
| --- | --- |
| Use: | optional (0..1) |
| Representation: | XML element `Updated` |
| CERIF: | the ResultProduct\_Classification linking entity ([https://w3id.org/cerif/model#ResultProduct\_Classification](https://w3id.org/cerif/model#ResultProduct_Classification)) with the [https://w3id.org/cerif/vocab/DataCiteMetadataSchema\_DateType#Updated](https://w3id.org/cerif/vocab/DataCiteMetadataSchema_DateType#Updated) semantics |

# Valid[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#valid "Permalink to this headline")

| Description: | Use the `startDate` and `endDate` attributes to indicate the period in which the dataset or resource is accurate. |
| --- | --- |
| Use: | optional (0..1) |
| Representation: | XML element `Valid` |
| CERIF: | the ResultProduct\_Classification linking entity ([https://w3id.org/cerif/model#ResultProduct\_Classification](https://w3id.org/cerif/model#ResultProduct_Classification)) with the [https://w3id.org/cerif/vocab/DataCiteMetadataSchema\_DateType#Valid](https://w3id.org/cerif/vocab/DataCiteMetadataSchema_DateType#Valid) semantics |

# Withdrawn[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#withdrawn "Permalink to this headline")

| Description: | Use the `startDate` attribute for the date the resource is removed. |
| --- | --- |
| Use: | optional (0..1) |
| Representation: | XML element `Withdrawn` |
| CERIF: | the ResultProduct\_Classification linking entity ([https://w3id.org/cerif/model#ResultProduct\_Classification](https://w3id.org/cerif/model#ResultProduct_Classification)) with the [https://w3id.org/cerif/vocab/DataCiteMetadataSchema\_DateType#Withdrawn](https://w3id.org/cerif/vocab/DataCiteMetadataSchema_DateType#Withdrawn) semantics |
