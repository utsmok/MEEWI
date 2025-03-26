---
title: "Project — OpenAIRE Guidelines for CRIS Managers 1.2.0 documentation"
source: "https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/cerif_xml_project_entity.html"
---
| Description: | A temporary endeavor undertaken to create a unique product, service or result. Source: the Project Management Institute, [https://www.pmi.org/about/learn-about-pmi/what-is-project-management](https://www.pmi.org/about/learn-about-pmi/what-is-project-management) In the research information domain, one typically tracks: (1) research projects, where the result is an addition to the body of knowledge of the mankind, (2) technology development projects, where the result is a particular technology or product, (3) innovation projects, where the result is an improvement of a product or process, and (4) projects that create or enhance infrastructure for research, technology development or innovation. Depending on the scope one can also track finer levels of granularity: stages, work packages, sometimes even down to individual tasks. All such activities are also modelled using the Project entity and linked using the recursive link relationship. The Project entity only captures details of the project scope and plan. Information about the resources needed to execute the project such as the funding (i.e., the grants received), the people and organisations involved, the supporting infrastructures, the outputs produced, etc. is contained in separate entities (the Funding entity, the Person entity, the OrgUnit entity, the infrastructure entities, the result entities respectively) and is linked to the Project. |
| --- | --- |
| Examples: | [openaire\_cerif\_xml\_example\_projects.xml](https://github.com/openaire/guidelines-cris-managers/blob/v1.2/samples/openaire_cerif_xml_example_projects.xml) |
| Representation: | XML element `Project`; the rest of this section documents children of this element |
| CERIF: | the Project entity ([https://w3id.org/cerif/model#Project](https://w3id.org/cerif/model#Project)) |

## Internal Identifier[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#internal-identifier "Permalink to this headline")

| Use: | mandatory (1) in top level entity. When embedded in other entities the Internal Identifier must be included only for managed information (i.e. entities that have a concrete record in the local CRIS system). See [Metadata representation in CERIF XML](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/implementation.html#metadata-representation-in-cerif-xml) |
| --- | --- |
| Representation: | XML attribute `id` |
| CERIF: | the ProjectIdentifier attribute ([https://w3id.org/cerif/model#Project.ProjectIdentifier](https://w3id.org/cerif/model#Project.ProjectIdentifier)) |

## Type[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#type "Permalink to this headline")

| Description: | The type of the project |
| --- | --- |
| Use: | optional, possibly multiple (0..\*) |
| Representation: | XML element `Type` containing the classification identifier and having a `scheme` attribute to specify the classification scheme identifier |
| CERIF: | the Project\_Classification ([https://w3id.org/cerif/model#Project\_Classification](https://w3id.org/cerif/model#Project_Classification)) |

## Acronym[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#acronym "Permalink to this headline")

| Description: | The acronym of the project |
| --- | --- |
| Use: | optional (0..1) |
| Representation: | XML element `Acronym` |
| CERIF: | the Project.Acronym attribute ([https://w3id.org/cerif/model#Project.Acronym](https://w3id.org/cerif/model#Project.Acronym)) |

## Title[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#title "Permalink to this headline")

| Description: | The title of the project |
| --- | --- |
| Use: | optional, possibly multiple (0..\*) |
| Representation: | XML element `Title` as a multilingual string |
| CERIF: | the Project.Title attribute ([https://w3id.org/cerif/model#Project.Title](https://w3id.org/cerif/model#Project.Title)) |

## Identifier[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#identifier "Permalink to this headline")

| Description: | An identifier of the project |
| --- | --- |
| Use: | optional, possibly multiple (0..\*) |
| Representation: | XML element `Identifier` with a required `type` attribute (the URI of the identifier scheme) |
| CERIF: | the FederatedIdentifier entity ([https://w3id.org/cerif/model#FederatedIdentifier](https://w3id.org/cerif/model#FederatedIdentifier)) |

## StartDate[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#startdate "Permalink to this headline")

| Description: | The start date of the project |
| --- | --- |
| Use: | optional (0..1) |
| Representation: | XML element `StartDate` |
| CERIF: | the Project.StartDate attribute ([https://w3id.org/cerif/model#Project.StartDate](https://w3id.org/cerif/model#Project.StartDate)) |
| Format: | full date (`YYYY-MM-DD`) with optional time zone indication |

## EndDate[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#enddate "Permalink to this headline")

| Description: | The end date of the project |
| --- | --- |
| Use: | optional (0..1) |
| Representation: | XML element `EndDate` |
| CERIF: | the Project.EndDate attribute ([https://w3id.org/cerif/model#Project.EndDate](https://w3id.org/cerif/model#Project.EndDate)) |
| Format: | full date (`YYYY-MM-DD`) with optional time zone indication |

## Consortium[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#consortium "Permalink to this headline")

| Description: | The consortium of the project: the organisations (persons) who are contractually bound to do the work in the project |
| --- | --- |
| Use: | optional (0..1) |
| Representation: | XML element `Consortium` with unordered embedded XML elements `Coordinator` that can contain an embedded organisation unit or person or `Partner` that can contain an embedded organisation unit or person or `Contractor` that can contain an embedded organisation unit or person or `InkindContributor` that can contain an embedded organisation unit or person or `Member` that can contain an embedded organisation unit or person |

### Coordinator[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#coordinator "Permalink to this headline")

| Description: | Project coordinator |
| --- | --- |
| Use: | optional, possibly multiple (0..\*) |
| Representation: | XML element `Coordinator` with embedded XML element `OrgUnit` or `Person`. A `DisplayName` may be specified, too. |
| CERIF: | the Project\_OrganisationUnit linking entity ([https://w3id.org/cerif/model#Project\_OrganisationUnit](https://w3id.org/cerif/model#Project_OrganisationUnit)) with the [https://w3id.org/cerif/vocab/OrganisationProjectEngagements#Coordinator](https://w3id.org/cerif/vocab/OrganisationProjectEngagements#Coordinator) semantics; the Project\_Person linking entity ([https://w3id.org/cerif/model#Project\_Person](https://w3id.org/cerif/model#Project_Person)) with the [https://w3id.org/cerif/vocab/PersonProjectEngagements#Coordinator](https://w3id.org/cerif/vocab/PersonProjectEngagements#Coordinator) semantics |

### Partner[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#partner "Permalink to this headline")

| Description: | Project partner |
| --- | --- |
| Use: | optional, possibly multiple (0..\*) |
| Representation: | XML element `Partner` with embedded XML element `OrgUnit` or `Person`. A `DisplayName` may be specified, too. |
| CERIF: | the Project\_OrganisationUnit linking entity ([https://w3id.org/cerif/model#Project\_OrganisationUnit](https://w3id.org/cerif/model#Project_OrganisationUnit)) with the [https://w3id.org/cerif/vocab/OrganisationProjectEngagements#Partner](https://w3id.org/cerif/vocab/OrganisationProjectEngagements#Partner) semantics; the Project\_Person linking entity ([https://w3id.org/cerif/model#Project\_Person](https://w3id.org/cerif/model#Project_Person)) with the [https://w3id.org/cerif/vocab/PersonProjectEngagements#Partner](https://w3id.org/cerif/vocab/PersonProjectEngagements#Partner) semantics |

### Contractor[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#contractor "Permalink to this headline")

| Description: | Project contractor |
| --- | --- |
| Use: | optional, possibly multiple (0..\*) |
| Representation: | XML element `Contractor` with embedded XML element `OrgUnit` or `Person`. A `DisplayName` may be specified, too. |
| CERIF: | the Project\_OrganisationUnit linking entity ([https://w3id.org/cerif/model#Project\_OrganisationUnit](https://w3id.org/cerif/model#Project_OrganisationUnit)) with the [https://w3id.org/cerif/vocab/OrganisationProjectEngagements#Contractor](https://w3id.org/cerif/vocab/OrganisationProjectEngagements#Contractor) semantics; the Project\_Person linking entity ([https://w3id.org/cerif/model#Project\_Person](https://w3id.org/cerif/model#Project_Person)) with the [https://w3id.org/cerif/vocab/PersonProjectEngagements#Contractor](https://w3id.org/cerif/vocab/PersonProjectEngagements#Contractor) semantics |

### InkindContributor[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#inkindcontributor "Permalink to this headline")

| Description: | Project in kind contributor |
| --- | --- |
| Use: | optional, possibly multiple (0..\*) |
| Representation: | XML element `InkindContributor` with embedded XML element `OrgUnit` or `Person`. A `DisplayName` may be specified, too. |
| CERIF: | the Project\_OrganisationUnit linking entity ([https://w3id.org/cerif/model#Project\_OrganisationUnit](https://w3id.org/cerif/model#Project_OrganisationUnit)) with the [https://w3id.org/cerif/vocab/OrganisationProjectEngagements#InkindContributor](https://w3id.org/cerif/vocab/OrganisationProjectEngagements#InkindContributor) semantics; the Project\_Person linking entity ([https://w3id.org/cerif/model#Project\_Person](https://w3id.org/cerif/model#Project_Person)) with the [https://w3id.org/cerif/vocab/PersonProjectEngagements#InkindContributor](https://w3id.org/cerif/vocab/PersonProjectEngagements#InkindContributor) semantics |

### Member[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#member "Permalink to this headline")

| Description: | A member of the project consortium |
| --- | --- |
| Use: | optional, possibly multiple (0..\*) |
| Representation: | XML element `Member` with embedded XML element `OrgUnit` or `Person`. A `DisplayName` may be specified, too. |
| CERIF: | the Project\_OrganisationUnit linking entity ([https://w3id.org/cerif/model#Project\_OrganisationUnit](https://w3id.org/cerif/model#Project_OrganisationUnit)) with the [https://w3id.org/cerif/vocab/OrganisationProjectEngagements#ConsortiumMember](https://w3id.org/cerif/vocab/OrganisationProjectEngagements#ConsortiumMember) semantics; the Project\_Person linking entity ([https://w3id.org/cerif/model#Project\_Person](https://w3id.org/cerif/model#Project_Person)) with the [https://w3id.org/cerif/vocab/PersonProjectEngagements#ConsortiumMember](https://w3id.org/cerif/vocab/PersonProjectEngagements#ConsortiumMember) semantics |

## Team[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#team "Permalink to this headline")

| Description: | The project team: the persons who carry out the work in the project, typically as a part of their job at the organisations from the consortium |
| --- | --- |
| Use: | optional (0..1) |
| Representation: | XML element `Team` with unordered embedded XML elements `PrincipalInvestigator` or `Contact` or `Member` |

### PrincipalInvestigator[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#principalinvestigator "Permalink to this headline")

| Description: | The principal investigator: the person responsible for the whole project, the head of the project team |
| --- | --- |
| Use: | optional, possibly multiple (0..\*) |
| Representation: | XML element `PrincipalInvestigator` with embedded XML element `Person` optionally followed by one or several `Affiliation` elements. A `DisplayName` may be specified, too. |
| CERIF: | the Project\_Person linking entity ([https://w3id.org/cerif/model#Project\_Person](https://w3id.org/cerif/model#Project_Person)) with the [https://w3id.org/cerif/vocab/PersonProjectEngagements#PrincipalInvestigator](https://w3id.org/cerif/vocab/PersonProjectEngagements#PrincipalInvestigator) semantics |

### Contact[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#contact "Permalink to this headline")

| Description: | A person to contact in matters connected with her/his organisations’ participation in the project |
| --- | --- |
| Use: | optional, possibly multiple (0..\*) |
| Representation: | XML element `Contact` with embedded XML element `Person` optionally followed by one or several `Affiliation` elements. A `DisplayName` may be specified, too. |
| CERIF: | the Project\_Person linking entity ([https://w3id.org/cerif/model#Project\_Person](https://w3id.org/cerif/model#Project_Person)) with the [https://w3id.org/cerif/vocab/PersonProjectEngagements#OrganisationContact](https://w3id.org/cerif/vocab/PersonProjectEngagements#OrganisationContact) semantics |

### Member[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#id12 "Permalink to this headline")

| Description: | A member of the project team |
| --- | --- |
| Use: | optional, possibly multiple (0..\*) |
| Representation: | XML element `Member` with embedded XML element `Person` optionally followed by one or several `Affiliation` elements. A `DisplayName` may be specified, too. |
| CERIF: | the Project\_Person linking entity ([https://w3id.org/cerif/model#Project\_Person](https://w3id.org/cerif/model#Project_Person)) with the [https://w3id.org/cerif/vocab/PersonProjectEngagements#TeamMember](https://w3id.org/cerif/vocab/PersonProjectEngagements#TeamMember) semantics |

## Funded[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#funded "Permalink to this headline")

| Description: | Information about funding of this project |
| --- | --- |
| Use: | optional, possibly multiple (0..\*) |
| Representation: | XML element `Funded` with unordered embedded XML elements `By` that can contain an embedded organisation unit or person or `As` |

### By[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#by "Permalink to this headline")

| Description: | The funder of the project |
| --- | --- |
| Use: | optional (0..1) |
| Representation: | XML element `By` with embedded XML element `OrgUnit` or `Person`. A `DisplayName` may be specified, too. |
| CERIF: | the Project\_OrganisationUnit linking entity ([https://w3id.org/cerif/model#Project\_OrganisationUnit](https://w3id.org/cerif/model#Project_OrganisationUnit)) with the [https://w3id.org/cerif/vocab/OrganisationProjectEngagements#Funder](https://w3id.org/cerif/vocab/OrganisationProjectEngagements#Funder) semantics |

### As[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#as "Permalink to this headline")

| Description: | The specific funding device (grant, award, contract) for the project |
| --- | --- |
| Use: | optional (0..1) |
| Representation: | XML element `As` with embedded XML element `Funding` |
| CERIF: | the Project\_Funding linking entity ([https://w3id.org/cerif/model#Project\_Funding](https://w3id.org/cerif/model#Project_Funding)) with the [https://w3id.org/cerif/vocab/ProjectFundingRelations#Support](https://w3id.org/cerif/vocab/ProjectFundingRelations#Support) semantics |

## Subject[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#subject "Permalink to this headline")

| Description: | The subject classification(s) of the project |
| --- | --- |
| Use: | optional, possibly multiple (0..\*) |
| Representation: | XML element `Subject` containing the classification identifier and having a `scheme` attribute to specify the classification scheme identifier |
| CERIF: | the Project\_Classification ([https://w3id.org/cerif/model#Project\_Classification](https://w3id.org/cerif/model#Project_Classification)) |

## Keyword[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#keyword "Permalink to this headline")

| Description: | A single keyword or key expression that characterize the project. Please repeat to serialize separate keywords or key expressions. |
| --- | --- |
| Use: | optional, possibly multiple (0..\*) |
| Representation: | XML element `Keyword` as a multilingual string |
| CERIF: | the Project.Keywords attribute ([https://w3id.org/cerif/model#Project.Keywords](https://w3id.org/cerif/model#Project.Keywords)) |

## Abstract[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#abstract "Permalink to this headline")

| Description: | The abstract of the project |
| --- | --- |
| Use: | optional, possibly multiple (0..\*) |
| Representation: | XML element `Abstract` |
| CERIF: | the Project.Abstract attribute ([https://w3id.org/cerif/model#Project.Abstract](https://w3id.org/cerif/model#Project.Abstract)) |

## Status[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#status "Permalink to this headline")

| Description: | The status of the project |
| --- | --- |
| Use: | optional, possibly multiple (0..\*) |
| Representation: | XML element `Status` containing the classification identifier and having a `scheme` attribute to specify the classification scheme identifier |
| CERIF: | the Project\_Classification ([https://w3id.org/cerif/model#Project\_Classification](https://w3id.org/cerif/model#Project_Classification)) |

## Uses[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#uses "Permalink to this headline")

| Description: | The equipment this project uses |
| --- | --- |
| Use: | optional, possibly multiple (0..\*) |
| Representation: | XML element `Uses` with embedded XML element `Equipment` |
| CERIF: | the Project\_Equipment linking entity ([https://w3id.org/cerif/model#Project\_Equipment](https://w3id.org/cerif/model#Project_Equipment)) with the [https://w3id.org/cerif/vocab/ProjectResearchInfrastructureRelations#User](https://w3id.org/cerif/vocab/ProjectResearchInfrastructureRelations#User) semantics |

## OAMandate[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#oamandate "Permalink to this headline")

| Description: | Information about the Open Access mandate that applies to this project |
| --- | --- |
| Use: | optional, possibly multiple (0..\*) |
| Representation: | XML element `OAMandate` |

### mandated[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#mandated "Permalink to this headline")

| Description: | The flag if Open Access is mandated in the project |
| --- | --- |
| Use: | required |
| Representation: | XML attribute `mandated` |
| Format: | `true` or `false` (data type `xs:boolean`) |

### uri[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#uri "Permalink to this headline")

| Description: | The Open Access policy that applies to the project |
| --- | --- |
| Use: | optional |
| Representation: | XML attribute `uri` |
| Format: | URI (data type `xs:anyURI`) |
