---
title: "Publication — OpenAIRE Guidelines for CRIS Managers 1.2.0 documentation"
source: "https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/cerif_xml_publication_entity.html"
---

| Description: | A text based scholarly publication or publishing channel that contains results of research. CRISs typically record metadata about scholarly publications from the scope of the CRIS (institutional CRIS for the institution, funder CRIS for the funding it distributed, etc.) in the context of the research projects, infrastructure, funding, organization units and authors/contributors. This entity typically represents the granularity level of a single published item for which attribution information is attached (usually in the form of a list of authors and contributors). This entity is also used to represent publishing channels and sources: journals and book series (incl. continuing conference proceedings series). (Taken from [https://doi.org/10.1016/j.procs.2014.06.008](https://doi.org/10.1016/j.procs.2014.06.008)) |
| --- | --- |
| Examples: | [openaire\_cerif\_xml\_example\_publications.xml](https://github.com/openaire/guidelines-cris-managers/blob/v1.2/samples/openaire_cerif_xml_example_publications.xml) |
| Representation: | XML element `Publication`; the rest of this section documents children of this element |
| CERIF: | the ResultPublication entity ([https://w3id.org/cerif/model#ResultPublication](https://w3id.org/cerif/model#ResultPublication)) |

## Internal Identifier[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#internal-identifier "Permalink to this headline")

| Use: | mandatory (1) in top level entity. When embedded in other entities the Internal Identifier must be included only for managed information (i.e. entities that have a concrete record in the local CRIS system). See [Metadata representation in CERIF XML](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/implementation.html#metadata-representation-in-cerif-xml) |
| --- | --- |
| Representation: | XML attribute `id` |
| CERIF: | the ResultPublicationIdentifier attribute ([https://w3id.org/cerif/model#ResultPublication.ResultPublicationIdentifier](https://w3id.org/cerif/model#ResultPublication.ResultPublicationIdentifier)) |

## Type[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#type "Permalink to this headline")

| Description: | The type of the publication |
| --- | --- |
| Use: | mandatory (1) |
| Representation: | XML element `Type` from namespace [https://www.openaire.eu/cerif-profile/vocab/COAR\_Publication\_Types](https://www.openaire.eu/cerif-profile/vocab/COAR_Publication_Types) |
| CERIF: | the ResultPublication\_Classification ([https://w3id.org/cerif/model#ResultPublication\_Classification](https://w3id.org/cerif/model#ResultPublication_Classification)) |
| Vocabulary: | Publication types extracted from the COAR Resource Types concept scheme: Types of publications as extracted from the COAR Resource Types concept scheme ([https://vocabularies.coar-repositories.org/resource\_types/](https://vocabularies.coar-repositories.org/resource_types/), the term ‘text’ and its descendants in the hierarchy except ‘patent’). Some terms are marked as deprecated; they can be removed in the next release of these Guidelines.  - **text** ([http://purl.org/coar/resource\_type/c\_18cf](http://purl.org/coar/resource_type/c_18cf)): A resource consisting primarily of words for reading. Examples include books, letters, dissertations, poems, newspapers, articles, archives of mailing lists. Note that facsimiles or images of texts are still of the genre Text. \[Source: [http://purl.org/dc/dcmitype/Text](http://purl.org/dc/dcmitype/Text)\] 	- **annotation** ([http://purl.org/coar/resource\_type/c\_1162](http://purl.org/coar/resource_type/c_1162)): An annotation in the sense of a legal note is a legally explanatory comment on a decision handed down by a court or arbitral tribunal. \[Source: DRIVER [info:eu-repo](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/) definition\] 	- **bibliography** ([http://purl.org/coar/resource\_type/c\_86bc](http://purl.org/coar/resource_type/c_86bc)): A list of the books and articles that have been used by someone when writing a particular book or article \[Source: [https://dictionary.cambridge.org/dictionary/english/bibliography](https://dictionary.cambridge.org/dictionary/english/bibliography)\] 	- **blog post** ([http://purl.org/coar/resource\_type/c\_6947](http://purl.org/coar/resource_type/c_6947)): A piece of writing or other item of content published on a blog. \[Source: [https://www.lexico.com/definition/blog\_post](https://www.lexico.com/definition/blog_post)\] 	- **book** ([http://purl.org/coar/resource\_type/c\_2f33](http://purl.org/coar/resource_type/c_2f33)): A non-serial publication that is complete in one volume or a designated finite number of volumes. \[Source: Adapted from [http://purl.org/eprint/type/Book](http://purl.org/eprint/type/Book)\] 		- **book part** ([http://purl.org/coar/resource\_type/c\_3248](http://purl.org/coar/resource_type/c_3248)): A defined chapter or section of a book, usually with a separate title or number. \[Source: [http://purl.org/spar/fabio/BookChapter](http://purl.org/spar/fabio/BookChapter)\] 	- **conference output** ([http://purl.org/coar/resource\_type/c\_c94f](http://purl.org/coar/resource_type/c_c94f)): All kind of digital resources contributed to a conference, like conference presentation (slides), conference report, conference lecture, abstracts, demonstrations. For conference papers, posters or proceedings the specific sub-concepts should be used. \[COAR definition\] 		- **conference paper not in proceedings** ([http://purl.org/coar/resource\_type/c\_18cp](http://purl.org/coar/resource_type/c_18cp)): A paper, typically the realization of a research paper reporting original research findings. Use this label when the paper is not published in a proceeding. \[Source: Adapted from [http://purl.org/spar/fabio/ConferencePaper](http://purl.org/spar/fabio/ConferencePaper)\] 		- **conference poster not in proceedings** ([http://purl.org/coar/resource\_type/c\_18co](http://purl.org/coar/resource_type/c_18co)): A display poster, typically containing text with illustrative figures and/or tables, usually reporting research results or proposing hypotheses, submitted for acceptance to and/or presented at a conference, seminar, symposium, workshop or similar event. Use this label when the poster is not published in a proceeding. \[Source: [http://purl.org/spar/fabio/ConferencePoster](http://purl.org/spar/fabio/ConferencePoster)\] 		- **conference presentation** ([http://purl.org/coar/resource\_type/R60J-J5BD](http://purl.org/coar/resource_type/R60J-J5BD)): A set of slides containing text, tables or figures, designed to communicate ideas or research results, for projection and viewing by an audience at a conference, symposium, seminar, lecture, workshop or other gatherings. \[Source: Adapted from [http://purl.org/spar/fabio/Presentation](http://purl.org/spar/fabio/Presentation)\] 		- **conference proceedings** ([http://purl.org/coar/resource\_type/c\_f744](http://purl.org/coar/resource_type/c_f744)): Conference proceedings is the official record of a conference meeting. It is a collection of documents which corresponds to the presentations given at the conference. It may include additional content. \[Source: [http://www.ieee.org/documents/confprocdefined.pdf](http://www.ieee.org/documents/confprocdefined.pdf) \] 			- **conference paper** ([http://purl.org/coar/resource\_type/c\_5794](http://purl.org/coar/resource_type/c_5794)): A paper, published within a conference proceeding, typically the realization of a research paper reporting original research findings. \[Source: Adapted from [http://purl.org/spar/fabio/ConferencePaper](http://purl.org/spar/fabio/ConferencePaper)\] 			- **conference poster** ([http://purl.org/coar/resource\_type/c\_6670](http://purl.org/coar/resource_type/c_6670)): A display poster, published within a conference proceeding, typically containing text with illustrative figures and/or tables, usually reporting research results or proposing hypotheses, submitted for acceptance to and/or presented at a conference, seminar, symposium, workshop or similar event. \[Source: Adapted [http://purl.org/spar/fabio/ConferencePoster](http://purl.org/spar/fabio/ConferencePoster)\] 	- **lecture** ([http://purl.org/coar/resource\_type/c\_8544](http://purl.org/coar/resource_type/c_8544)): Transcription of an oral presentation/talk intended to present information or teach people about a particular subject, for example by a university or college teacher. \[Source: Adopted from [https://en.wikipedia.org/wiki/Lecture](https://en.wikipedia.org/wiki/Lecture)\] 	- **letter** ([http://purl.org/coar/resource\_type/c\_0857](http://purl.org/coar/resource_type/c_0857)): A brief description of important new research, also known as “communication”. \[Source: [https://cerif.eurocris.org/vocab/html/OutputTypes.html#Letter](https://cerif.eurocris.org/vocab/html/OutputTypes.html#Letter)\] 	- **magazine** ([http://purl.org/coar/resource\_type/c\_2cd9](http://purl.org/coar/resource_type/c_2cd9)): A popular interest periodical usually containing articles on a variety of topics, written by various authors in a nonscholarly style or a trade publication, unlike a consumer publication, covers a specific topic for people who work in that particular field or industry. \[Source: Adapted from [https://www.thebalance.com/what-is-a-trade-publication-exactly-2316039](https://www.thebalance.com/what-is-a-trade-publication-exactly-2316039) and [http://www.abc-clio.com/ODLIS/odlis\_m.aspx](http://www.abc-clio.com/ODLIS/odlis_m.aspx)\] 	- **manuscript** ([http://purl.org/coar/resource\_type/c\_0040](http://purl.org/coar/resource_type/c_0040)): A manuscript is a work of any kind (text, inscription, music score, map, etc.) written entirely by hand. \[Source: [https://products.abc-clio.com/ODLIS/odlis\_m.aspx](https://products.abc-clio.com/ODLIS/odlis_m.aspx)\] 	- **musical notation** ([http://purl.org/coar/resource\_type/c\_18cw](http://purl.org/coar/resource_type/c_18cw)): Symbols used to write music, as in a music score, and to express mathematical concepts. \[Source: Adapted from [https://products.abc-clio.com/ODLIS/odlis\_n.aspx](https://products.abc-clio.com/ODLIS/odlis_n.aspx)\] 	- **newspaper** ([http://purl.org/coar/resource\_type/c\_2fe3](http://purl.org/coar/resource_type/c_2fe3)): A non-peer reviewed periodical, usually published daily or weekly, consisting primarily of editorials and news items concerning current or recent events and matters of public interest. \[Source: [http://purl.org/spar/fabio/Newspaper](http://purl.org/spar/fabio/Newspaper)\] 		- **newspaper article** ([http://purl.org/coar/resource\_type/c\_998f](http://purl.org/coar/resource_type/c_998f)): Work consisting of a news item appearing in a general-interest newspaper or other general news periodical, containing information of current and timely interest in a field. (Adapted from [http://www.reference.md/files/D018/mD018431.html](http://www.reference.md/files/D018/mD018431.html) ) 	- **other periodical** ([http://purl.org/coar/resource\_type/QX5C-AR31](http://purl.org/coar/resource_type/QX5C-AR31)): A resource type that is not included in existing terms under the top concept “Text”. \[COAR definition\] 	- **periodical (deprecated)** ([http://purl.org/coar/resource\_type/c\_2659](http://purl.org/coar/resource_type/c_2659)): A periodical is a serial publication with its own distinctive title, characterized by a variety of contents and contributors, and issued at regular intervals. (Adapted from ODLIS) \[Source: [http://www.abc-clio.com/ODLIS/odlis\_p.aspx](http://www.abc-clio.com/ODLIS/odlis_p.aspx)\] 		- **journal** ([http://purl.org/coar/resource\_type/c\_0640](http://purl.org/coar/resource_type/c_0640)): A journal is a serial publication devoted to disseminating original research and current developments on a subject. (Adapted from ODLIS) \[Source: [http://dspacecris.eurocris.org/cris/classcerif/classcerif00422](http://dspacecris.eurocris.org/cris/classcerif/classcerif00422)\] 			- **contribution to journal (deprecated)** ([http://purl.org/coar/resource\_type/c\_3e5a](http://purl.org/coar/resource_type/c_3e5a)): A contribution to a journal denotes a work published in a journal. If applicable sub-terms should be chosen. 				- **editorial** ([http://purl.org/coar/resource\_type/c\_b239](http://purl.org/coar/resource_type/c_b239)): A brief essay expressing the opinion or position of the chief editor(s) of a (academic) journal with respect to a current political, social, cultural, or professional issue. \[Source: Adapted from ODLIS \[Source: [http://www.abc-clio.com/ODLIS/odlis\_e.aspx](http://www.abc-clio.com/ODLIS/odlis_e.aspx) \] 				- **journal article** ([http://purl.org/coar/resource\_type/c\_6501](http://purl.org/coar/resource_type/c_6501)): An article, typically the realization of a research paper reporting original research findings, published in a journal issue. \[Source: [http://purl.org/spar/fabio/JournalArticle](http://purl.org/spar/fabio/JournalArticle)\] 					- **corrigendum** ([http://purl.org/coar/resource\_type/c\_7acd](http://purl.org/coar/resource_type/c_7acd)): A formal correction to an error introduced by the author into a previously published document. (adapted from [https://sparontologies.github.io/fabio/current/fabio.html#d4e2712](https://sparontologies.github.io/fabio/current/fabio.html#d4e2712)) 					- **data paper** ([http://purl.org/coar/resource\_type/c\_beb9](http://purl.org/coar/resource_type/c_beb9)): A data paper is a scholarly publication describing a particular dataset or group of dataset, published in the form of a peer-reviewed article in a scholarly journal. The main purpose of a data paper is to describe data, the circumstances of their collection, and information related to data features, access and potential reuse. Adapted from [https://en.wikipedia.org/wiki/Data\_paper](https://en.wikipedia.org/wiki/Data_paper) and [http://www.gbif.org/publishing-data/data-papers](http://www.gbif.org/publishing-data/data-papers) 					- **research article** ([http://purl.org/coar/resource\_type/c\_2df8fbb1](http://purl.org/coar/resource_type/c_2df8fbb1)): A research article is a primary source, that is, it reports the methods and results of an original study performed by the authors. (adapted from [http://apus.libanswers.com/faq/2324](http://apus.libanswers.com/faq/2324)) 					- **review article** ([http://purl.org/coar/resource\_type/c\_dcae04bc](http://purl.org/coar/resource_type/c_dcae04bc)): A review article is a secondary source, that is, it is written about other articles, and does not report original research of its own. \[Source: Adapted from [http://apus.libanswers.com/faq/2324](http://apus.libanswers.com/faq/2324)\] 					- **software paper** ([http://purl.org/coar/resource\_type/c\_7bab](http://purl.org/coar/resource_type/c_7bab)): A software paper should include the rationale for the development of the tool and details of the code used for its construction. \[Source: Adapted from [https://f1000research.com/for-authors/article-guidelines/software-tool-articles](https://f1000research.com/for-authors/article-guidelines/software-tool-articles) \] 				- **letter to the editor** ([http://purl.org/coar/resource\_type/c\_545b](http://purl.org/coar/resource_type/c_545b)): A letter addressed to the editor and comments on or discussed an item previously published by that periodical, or of interest to its readership. \[Source: Adapted from [http://purl.org/spar/fabio/Letter](http://purl.org/spar/fabio/Letter)\] 	- **preprint (deprecated)** ([http://purl.org/coar/resource\_type/c\_816b](http://purl.org/coar/resource_type/c_816b)): A preprint is a scientific manuscript without peer-review and has not yet been accepted by a journal, typicaly submitted to a public server/ repository by the author. \[Source: Adapted from [https://asapbio.org/preprint-info/preprint-faq#qaef-637](https://asapbio.org/preprint-info/preprint-faq#qaef-637)\] 	- **report** ([http://purl.org/coar/resource\_type/c\_93fc](http://purl.org/coar/resource_type/c_93fc)): A report is a separately published record of research findings, research still in progress, policy developments and events, or other technical findings, usually bearing a report number and sometimes a grant number assigned by the funding agency. Also, an official record of the activities of a committee or corporate entity, the proceedings of a government body, or an investigation by an agency, whether published or private, usually archived or submitted to a higher authority, voluntarily or under mandate. In a more general sense, any formal account of facts or information related to a specific event or phenomenon, sometimes given at regular intervals. \[Source: [http://lu.com/odlis/odlis\_R.cfm#report](http://lu.com/odlis/odlis_R.cfm#report) \] 		- **clinical study** ([http://purl.org/coar/resource\_type/c\_7877](http://purl.org/coar/resource_type/c_7877)): A work that reports on the results of a research study to evaluate interventions or exposures on biomedical or health-related outcomes. The two main types of clinical studies are interventional studies (clinical trials) and observational studies. While most clinical studies concern humans, this publication type may be used for clinical veterinary articles meeting the requisites for humans. \[Source: [https://www.ncbi.nlm.nih.gov/mesh/2009830](https://www.ncbi.nlm.nih.gov/mesh/2009830)\] 		- **data management plan** ([http://purl.org/coar/resource\_type/c\_ab20](http://purl.org/coar/resource_type/c_ab20)): A formal statement describing how research data will be managed and documented throughout a research project and the terms regarding the subsequent deposit of the data with a data repository for long-term management and preservation. \[Source: [https://casrai.org/rdm-glossary](https://casrai.org/rdm-glossary)\] 		- **internal report (deprecated)** ([http://purl.org/coar/resource\_type/c\_18ww](http://purl.org/coar/resource_type/c_18ww)): An internal report is a record of findings collected for internal use. It is not designed to be made public and may include confidential or proprietary information. 		- **memorandum** ([http://purl.org/coar/resource\_type/c\_18wz](http://purl.org/coar/resource_type/c_18wz)): A formal note distributed internally to one or more persons in a company, agency, organization, or institution, with a header indicating the date it was sent and stating to whom it is addressed (To:), from whom it is sent (From:), and the subject of the text (Re:). Unlike a letter, a memo does not require a full salutation or signature at the end of the text–the sender may simply initial his or her name in the header. \[Source: [https://products.abc-clio.com/ODLIS/odlis\_m.aspx#memorandum](https://products.abc-clio.com/ODLIS/odlis_m.aspx#memorandum)\] 		- **other type of report (deprecated)** ([http://purl.org/coar/resource\_type/c\_18wq](http://purl.org/coar/resource_type/c_18wq)): Other types of report may include Business Plans Technical Specifications, data management plans, recommendation reports, white papers, annual reports, auditor’s reports, workplace reports, census reports, trip reports, progress reports, investigative reports, budget reports, policy reports, demographic reports, credit reports, appraisal reports, inspection reports, military reports, bound reports, etc. \[Source: [https://en.wikipedia.org/wiki/Report](https://en.wikipedia.org/wiki/Report)\] 		- **policy report (deprecated)** ([http://purl.org/coar/resource\_type/c\_186u](http://purl.org/coar/resource_type/c_186u)): A policy report presents what is known about a particular issue or problem. It assembles facts and evidence to help readers understand complex issues and form a response. It might aim to be neutral, or it might aim to persuade readers in a particular direction. \[Source: [https://www.uow.edu.au/student/learning-co-op/assessments/policy-report](https://www.uow.edu.au/student/learning-co-op/assessments/policy-report)/#\] 		- **project deliverable** ([http://purl.org/coar/resource\_type/c\_18op](http://purl.org/coar/resource_type/c_18op)): A document containing a project report, intended to be delivered to a customer or funding agency describing the results achieved within a specific project. \[Source: [http://purl.org/spar/fabio/ProjectReportDocument](http://purl.org/spar/fabio/ProjectReportDocument)\] 		- **report part (deprecated)** ([http://purl.org/coar/resource\_type/c\_ba1f](http://purl.org/coar/resource_type/c_ba1f)): part of a report 		- **report to funding agency (deprecated)** ([http://purl.org/coar/resource\_type/c\_18hj](http://purl.org/coar/resource_type/c_18hj)): A report to a funding agency is a document written by beneficiaries of project grants. The reporting documents can be e.g. periodic reports about progress of scientific and technical work and final report. For deliverables use ‘Project deliverable’. \[Source: [http://ec.europa.eu/research/participants/fp7documents/funding-guide/6\_projects/reports/reports\_en.htm](http://ec.europa.eu/research/participants/fp7documents/funding-guide/6_projects/reports/reports_en.htm) \] 		- **research protocol** ([http://purl.org/coar/resource\_type/YZ1N-ZFT9](http://purl.org/coar/resource_type/YZ1N-ZFT9)): The protocol is a detailed plan of the research study including a project summary, project description covering the rationale, objectives, methodology, data management and analysis, ethical considerations, gender issues and references. \[Source: Adapted from [https://www.who.int/publications/i/item/a-practical-guide-for-health-researchers](https://www.who.int/publications/i/item/a-practical-guide-for-health-researchers)\] 		- **research report** ([http://purl.org/coar/resource\_type/c\_18ws](http://purl.org/coar/resource_type/c_18ws)): It is publication that reports on the findings of a research project or alternatively scientific observations on or about a subject. \[Source: Adapted from [https://en.wikipedia.org/wiki/Research\_report](https://en.wikipedia.org/wiki/Research_report)\] 		- **technical report** ([http://purl.org/coar/resource\_type/c\_18gh](http://purl.org/coar/resource_type/c_18gh)): A document that describes the process, progress, or results of technical or scientific research or the state of a technical or scientific research problem. It might also include recommendations and conclusions of the research. \[Source: [http://guides.library.cornell.edu/ecommons/types](http://guides.library.cornell.edu/ecommons/types)\] 	- **research proposal** ([http://purl.org/coar/resource\_type/c\_baaf](http://purl.org/coar/resource_type/c_baaf)): A research proposal is a document proposing a research project, generally in the sciences or academia, and generally constitutes a request for sponsorship of that research. \[Source: [https://en.wikipedia.org/wiki/Research\_proposal](https://en.wikipedia.org/wiki/Research_proposal)\] 	- **review** ([http://purl.org/coar/resource\_type/c\_efa0](http://purl.org/coar/resource_type/c_efa0)): A review of others’ published work. \[Source: Adapted from [http://purl.org/spar/fabio/Review](http://purl.org/spar/fabio/Review)\] 		- **book review** ([http://purl.org/coar/resource\_type/c\_ba08](http://purl.org/coar/resource_type/c_ba08)): A written review and critical analysis of the content, scope and quality of a book or other monographic work. \[Source: [http://purl.org/spar/fabio/BookReview](http://purl.org/spar/fabio/BookReview)\] 		- **commentary** ([http://purl.org/coar/resource\_type/D97F-VB57](http://purl.org/coar/resource_type/D97F-VB57)): A commentary is a more in-depth analysis written to draw attention to a work already published. Commentaries are somewhat like “reviews” in that the author presents his or her analysis of a work and why it would be of interest to a specific audience. \[Source: [https://www.enago.com/academy/perspective-opinion-and-commentary-pieces](https://www.enago.com/academy/perspective-opinion-and-commentary-pieces)\] 		- **peer review** ([http://purl.org/coar/resource\_type/H9BQ-739P](http://purl.org/coar/resource_type/H9BQ-739P)): An evaluation of scientific, academic, or professional work by others working in the same field. \[Source: Adopted from [https://schema.datacite.org/meta/kernel-4.4/doc/DataCite-MetadataKernel\_v4.4.pdf](https://schema.datacite.org/meta/kernel-4.4/doc/DataCite-MetadataKernel_v4.4.pdf)\] 	- **technical documentation** ([http://purl.org/coar/resource\_type/c\_71bd](http://purl.org/coar/resource_type/c_71bd)): Technical documentation refers to any type of documentation that describes handling, functionality and architecture of a technical product or a product under development or use. \[Source: [https://en.wikipedia.org/wiki/Technical\_documentation](https://en.wikipedia.org/wiki/Technical_documentation)\] 	- **thesis** ([http://purl.org/coar/resource\_type/c\_46ec](http://purl.org/coar/resource_type/c_46ec)): A book authored by a student containing a formal presentations of research outputs submitted for examination in completion of a course of study at an institution of higher education, to fulfil the requirements for an academic degree. Also know as a dissertation. \[Source: [http://purl.org/spar/fabio/Thesis](http://purl.org/spar/fabio/Thesis)\] 		- **bachelor thesis** ([http://purl.org/coar/resource\_type/c\_7a1f](http://purl.org/coar/resource_type/c_7a1f)): A thesis reporting a research project undertaken as part of an undergraduate course of education leading to a bachelor’s degree. \[Source: [http://purl.org/spar/fabio/BachelorsThesis](http://purl.org/spar/fabio/BachelorsThesis)\] 		- **doctoral thesis** ([http://purl.org/coar/resource\_type/c\_db06](http://purl.org/coar/resource_type/c_db06)): A thesis reporting the research undertaken during a period of graduate study leading to a doctoral degree. \[Source: [http://purl.org/spar/fabio/DoctoralThesis](http://purl.org/spar/fabio/DoctoralThesis)\] 		- **master thesis** ([http://purl.org/coar/resource\_type/c\_bdcc](http://purl.org/coar/resource_type/c_bdcc)): A thesis reporting a research project undertaken as part of a graduate course of education leading to a master’s degree. \[Source: [http://purl.org/spar/fabio/MastersThesis](http://purl.org/spar/fabio/MastersThesis)\] 	- **transcription** ([http://purl.org/coar/resource\_type/6NC7-GK9S](http://purl.org/coar/resource_type/6NC7-GK9S)): A written record of words spoken in court proceedings or in a speech, interview, broadcast, or sound recording. \[Source: Adapted from [https://products.abc-clio.com/ODLIS/odlis\_t.aspx](https://products.abc-clio.com/ODLIS/odlis_t.aspx)\] 	- **working paper** ([http://purl.org/coar/resource\_type/c\_8042](http://purl.org/coar/resource_type/c_8042)): A working or discussion paper circulated publicly or among a group of peers. Certain disciplines, for example economics, issue working papers in series. \[Source: [http://www.ukoln.ac.uk/repositories/digirep/index/Eprints\_Type\_Vocabulary\_Encoding\_Scheme#:~:text=http%3A//purl.org/eprint/type/WorkingPaper](http://www.ukoln.ac.uk/repositories/digirep/index/Eprints_Type_Vocabulary_Encoding_Scheme#:~:text=http%3A//purl.org/eprint/type/WorkingPaper)\] |

## Language[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#language "Permalink to this headline")

| Description: | The language of the publication. Please use the IETF language tags as described in the IETF BCP 47 document. |
| --- | --- |
| Use: | optional (0..1) |
| Representation: | XML element `Language` |
| CERIF: | the ResultPublication\_Classification linking entity ([https://w3id.org/cerif/model#ResultPublication\_Classification](https://w3id.org/cerif/model#ResultPublication_Classification)) with the [http://publications.europa.eu/resource/authority/language](http://publications.europa.eu/resource/authority/language) semantics |

## Title[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#title "Permalink to this headline")

| Description: | The title of the publication |
| --- | --- |
| Use: | optional, possibly multiple (0..\*) |
| Representation: | XML element `Title` as a multilingual string |
| CERIF: | the ResultPublication.Title attribute ([https://w3id.org/cerif/model#ResultPublication.Title](https://w3id.org/cerif/model#ResultPublication.Title)) |

## Subtitle[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#subtitle "Permalink to this headline")

| Description: | The subtitle of the publication |
| --- | --- |
| Use: | optional, possibly multiple (0..\*) |
| Representation: | XML element `Subtitle` as a multilingual string |
| CERIF: | the ResultPublication.Subtitle attribute ([https://w3id.org/cerif/model#ResultPublication.Subtitle](https://w3id.org/cerif/model#ResultPublication.Subtitle)) |

## NameAbbreviation[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#nameabbreviation "Permalink to this headline")

| Description: | The abbreviation of the title of the publication. E.g. the acronym of a journal. |
| --- | --- |
| Use: | optional, possibly multiple (0..\*) |
| Representation: | XML element `NameAbbreviation` as a multilingual string |
| CERIF: | the ResultPublication.NameAbbreviation attribute ([https://w3id.org/cerif/model#ResultPublication.NameAbbreviation](https://w3id.org/cerif/model#ResultPublication.NameAbbreviation)) |

## PublishedIn[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#publishedin "Permalink to this headline")

| Description: | The source (another Publication) where this publication appeared. E.g. a journal article lists here the journal where it appeared. To be used for a publishing channel. |
| --- | --- |
| Use: | optional (0..1) |
| Representation: | XML element `PublishedIn` with embedded XML element `Publication` |
| CERIF: | the ResultPublication\_ResultPublication linking entity ([https://w3id.org/cerif/model#ResultPublication\_ResultPublication](https://w3id.org/cerif/model#ResultPublication_ResultPublication)) with the [https://w3id.org/cerif/vocab/InterPublicationRelations#Publication](https://w3id.org/cerif/vocab/InterPublicationRelations#Publication) semantics (direction :1) |

## PartOf[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#partof "Permalink to this headline")

| Description: | The Publication of which this publication is a part. E.g. a book chapter lists here the book that contains it. To be used for a containing publication. |
| --- | --- |
| Use: | optional (0..1) |
| Representation: | XML element `PartOf` with embedded XML element `Publication` |
| CERIF: | the ResultPublication\_ResultPublication linking entity ([https://w3id.org/cerif/model#ResultPublication\_ResultPublication](https://w3id.org/cerif/model#ResultPublication_ResultPublication)) with the [https://w3id.org/cerif/vocab/InterPublicationRelations#Part](https://w3id.org/cerif/vocab/InterPublicationRelations#Part) semantics (direction :1) |

## PublicationDate[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#publicationdate "Permalink to this headline")

| Description: | The date the publication appeared |
| --- | --- |
| Use: | optional (0..1) |
| Representation: | XML element `PublicationDate` |
| CERIF: | the ResultPublication.ResultPublicationDate attribute ([https://w3id.org/cerif/model#ResultPublication.ResultPublicationDate](https://w3id.org/cerif/model#ResultPublication.ResultPublicationDate)) |
| Format: | any of:  - year (`YYYY`) with optional time zone indication - year and month (`YYYY-MM`) with optional time zone indication - full date (`YYYY-MM-DD`) with optional time zone indication - date and time (`YYYY-MM-DD'T'hh:mm:ss(.SSS)`) with optional time zone indication |

## Number[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#number "Permalink to this headline")

| Description: | The number of the publication (e.g. Article Number) |
| --- | --- |
| Use: | optional (0..1) |
| Representation: | XML element `Number` |
| CERIF: | the ResultPublication.Number attribute ([https://w3id.org/cerif/model#ResultPublication.Number](https://w3id.org/cerif/model#ResultPublication.Number)) |

## Volume[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#volume "Permalink to this headline")

| Description: | The volume of the publishing channel where this publication appeared |
| --- | --- |
| Use: | optional (0..1) |
| Representation: | XML element `Volume` |
| CERIF: | the ResultPublication.Volume attribute ([https://w3id.org/cerif/model#ResultPublication.Volume](https://w3id.org/cerif/model#ResultPublication.Volume)) |

## Issue[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#issue "Permalink to this headline")

| Description: | The issue of the publishing channel where this publication appeared |
| --- | --- |
| Use: | optional (0..1) |
| Representation: | XML element `Issue` |
| CERIF: | the ResultPublication.Issue attribute ([https://w3id.org/cerif/model#ResultPublication.Issue](https://w3id.org/cerif/model#ResultPublication.Issue)) |

## Edition[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#edition "Permalink to this headline")

| Description: | The edition of the publication |
| --- | --- |
| Use: | optional (0..1) |
| Representation: | XML element `Edition` |
| CERIF: | the ResultPublication.Edition attribute ([https://w3id.org/cerif/model#ResultPublication.Edition](https://w3id.org/cerif/model#ResultPublication.Edition)) |

## StartPage[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#startpage "Permalink to this headline")

| Description: | The page where this publication starts, in case the publishing channel or containing publication has numbered pages |
| --- | --- |
| Use: | optional (0..1) |
| Representation: | XML element `StartPage` |
| CERIF: | the ResultPublication.StartPage attribute ([https://w3id.org/cerif/model#ResultPublication.StartPage](https://w3id.org/cerif/model#ResultPublication.StartPage)) |

## EndPage[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#endpage "Permalink to this headline")

| Description: | The page where this publication ends, in case the publishing channel or containing publication has numbered pages |
| --- | --- |
| Use: | optional (0..1) |
| Representation: | XML element `EndPage` |
| CERIF: | the ResultPublication.EndPage attribute ([https://w3id.org/cerif/model#ResultPublication.EndPage](https://w3id.org/cerif/model#ResultPublication.EndPage)) |

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

## PMCID[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#pmcid "Permalink to this headline")

| Use: | optional (0..1) |
| --- | --- |
| Representation: | XML element `PMCID` |
| CERIF: | the FederatedIdentifier entity ([https://w3id.org/cerif/model#FederatedIdentifier](https://w3id.org/cerif/model#FederatedIdentifier)) |

## ISI-Number[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#isi-number "Permalink to this headline")

| Use: | optional (0..1) |
| --- | --- |
| Representation: | XML element `ISI-Number` |
| CERIF: | the FederatedIdentifier entity ([https://w3id.org/cerif/model#FederatedIdentifier](https://w3id.org/cerif/model#FederatedIdentifier)) |

## SCP-Number[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#scp-number "Permalink to this headline")

| Use: | optional (0..1) |
| --- | --- |
| Representation: | XML element `SCP-Number` |
| CERIF: | the FederatedIdentifier entity ([https://w3id.org/cerif/model#FederatedIdentifier](https://w3id.org/cerif/model#FederatedIdentifier)) |

## ISSN[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#issn "Permalink to this headline")

| Description: | The International Standard Serial Number |
| --- | --- |
| Use: | optional, possibly multiple (0..\*) |
| Representation: | XML element `ISSN` |
| CERIF: | the FederatedIdentifier entity ([https://w3id.org/cerif/model#FederatedIdentifier](https://w3id.org/cerif/model#FederatedIdentifier)) |
| Format: | regular expression `\d{4}-?\d{3}[\dX]` and length between 8 and 9 characters (as per [https://data.crossref.org/reports/help/schema\_doc/4.4.1/schema\_4\_4\_1.html#issn\_t](https://data.crossref.org/reports/help/schema_doc/4.4.1/schema_4_4_1.html#issn_t)) |

### medium[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#medium "Permalink to this headline")

| Use: | optional |
| --- | --- |
| Representation: | XML attribute `medium` |
| Vocabulary: | ISSN Media List  - **Print** ([http://issn.org/vocabularies/Medium#Print](http://issn.org/vocabularies/Medium#Print)): Print (paper) - **Online** ([http://issn.org/vocabularies/Medium#Online](http://issn.org/vocabularies/Medium#Online)): Online (online publication) - **Digital carrier** ([http://issn.org/vocabularies/Medium#DigitalCarrier](http://issn.org/vocabularies/Medium#DigitalCarrier)): Digital carrier (CD-ROM, USB keys) - **Other** ([http://issn.org/vocabularies/Medium#Other](http://issn.org/vocabularies/Medium#Other)): Other (Loose-leaf publications, braille, etc.) |

## ISBN[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#isbn "Permalink to this headline")

| Description: | The International Standard Book Number |
| --- | --- |
| Use: | optional, possibly multiple (0..\*) |
| Representation: | XML element `ISBN` |
| CERIF: | the FederatedIdentifier entity ([https://w3id.org/cerif/model#FederatedIdentifier](https://w3id.org/cerif/model#FederatedIdentifier)) |
| Format: | any of:  - regular expression `978-\d+-\d+-\d+-\d` and length of exactly 17 characters (ISBN-13, human readable form) - regular expression `978 \d+ \d+ \d+ \d` and length of exactly 17 characters (ISBN-13, human readable form) - regular expression `979-[1-9]\d*-\d+-\d+-\d` and length of exactly 17 characters (ISBN-13, human readable form) - regular expression `979 [1-9]\d* \d+ \d+ \d` and length of exactly 17 characters (ISBN-13, human readable form) - regular expression `978\d{10}` and length of exactly 13 characters (ISBN-13, concise form) - regular expression `979[1-9]\d{9}` and length of exactly 13 characters (ISBN-13, concise form) - regular expression `\d+-\d+-\d+-[\dX]` and length of exactly 13 characters (ISBN-10, human readable form) - regular expression `\d+ \d+ \d+ [\dX]` and length of exactly 13 characters (ISBN-10, human readable form) - regular expression `\d{9}[\dX]` and length of exactly 10 characters (ISBN-10, concise form) |

### medium[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#id10 "Permalink to this headline")

| Use: | optional |
| --- | --- |
| Representation: | XML attribute `medium` |
| Vocabulary: | ISSN Media List  - **Print** ([http://issn.org/vocabularies/Medium#Print](http://issn.org/vocabularies/Medium#Print)): Print (paper) - **Online** ([http://issn.org/vocabularies/Medium#Online](http://issn.org/vocabularies/Medium#Online)): Online (online publication) - **Digital carrier** ([http://issn.org/vocabularies/Medium#DigitalCarrier](http://issn.org/vocabularies/Medium#DigitalCarrier)): Digital carrier (CD-ROM, USB keys) - **Other** ([http://issn.org/vocabularies/Medium#Other](http://issn.org/vocabularies/Medium#Other)): Other (Loose-leaf publications, braille, etc.) |

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

## ZDB-ID[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#zdb-id "Permalink to this headline")

| Use: | optional (0..1) |
| --- | --- |
| Representation: | XML element `ZDB-ID` |
| CERIF: | the FederatedIdentifier entity ([https://w3id.org/cerif/model#FederatedIdentifier](https://w3id.org/cerif/model#FederatedIdentifier)) |
| Format: | regular expression `\d{1,7}-[Xx\d]` (as per [https://www.wikidata.org/wiki/Property:P1042](https://www.wikidata.org/wiki/Property:P1042)) |

## Authors[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#authors "Permalink to this headline")

| Description: | The authors of this publication |
| --- | --- |
| Use: | optional (0..1) |
| Representation: | XML element `Authors` with ordered embedded XML elements `Author` that can contain an embedded person with affiliations or organisation unit |

### Author[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#author "Permalink to this headline")

| Use: | optional, possibly multiple (0..\*) |
| --- | --- |
| Representation: | XML element `Author` with embedded XML element `Person` optionally followed by one or several `Affiliation` elements, or `OrgUnit`. A `DisplayName` may be specified, too. |
| CERIF: | the Person\_ResultPublication linking entity ([https://w3id.org/cerif/model#Person\_ResultPublication](https://w3id.org/cerif/model#Person_ResultPublication)) with the [https://w3id.org/cerif/vocab/PersonOutputContributions#Author](https://w3id.org/cerif/vocab/PersonOutputContributions#Author) semantics; the OrganisationUnit\_ResultPublication linking entity ([https://w3id.org/cerif/model#OrganisationUnit\_ResultPublication](https://w3id.org/cerif/model#OrganisationUnit_ResultPublication)) with the [https://w3id.org/cerif/vocab/OrganisationOutputContributions#Author](https://w3id.org/cerif/vocab/OrganisationOutputContributions#Author) semantics |

## Editors[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#editors "Permalink to this headline")

| Description: | The editors of this publication |
| --- | --- |
| Use: | optional (0..1) |
| Representation: | XML element `Editors` with ordered embedded XML elements `Editor` that can contain an embedded person with affiliations or organisation unit |

### Editor[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#editor "Permalink to this headline")

| Use: | optional, possibly multiple (0..\*) |
| --- | --- |
| Representation: | XML element `Editor` with embedded XML element `Person` optionally followed by one or several `Affiliation` elements, or `OrgUnit`. A `DisplayName` may be specified, too. |
| CERIF: | the Person\_ResultPublication linking entity ([https://w3id.org/cerif/model#Person\_ResultPublication](https://w3id.org/cerif/model#Person_ResultPublication)) with the [https://w3id.org/cerif/vocab/PersonOutputContributions#Editor](https://w3id.org/cerif/vocab/PersonOutputContributions#Editor) semantics; the OrganisationUnit\_ResultPublication linking entity ([https://w3id.org/cerif/model#OrganisationUnit\_ResultPublication](https://w3id.org/cerif/model#OrganisationUnit_ResultPublication)) with the [https://w3id.org/cerif/vocab/OrganisationOutputContributions#Editor](https://w3id.org/cerif/vocab/OrganisationOutputContributions#Editor) semantics |

## Publishers[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#publishers "Permalink to this headline")

| Description: | The publishers of this publication |
| --- | --- |
| Use: | optional (0..1) |
| Representation: | XML element `Publishers` with ordered embedded XML elements `Publisher` that can contain an embedded organisation unit or person |

### Publisher[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#publisher "Permalink to this headline")

| Use: | optional, possibly multiple (0..\*) |
| --- | --- |
| Representation: | XML element `Publisher` with embedded XML element `OrgUnit` or `Person`. A `DisplayName` may be specified, too. |
| CERIF: | the OrganisationUnit\_ResultPublication linking entity ([https://w3id.org/cerif/model#OrganisationUnit\_ResultPublication](https://w3id.org/cerif/model#OrganisationUnit_ResultPublication)) with the [https://w3id.org/cerif/vocab/OrganisationOutputContributions#Publisher](https://w3id.org/cerif/vocab/OrganisationOutputContributions#Publisher) semantics; the Person\_ResultPublication linking entity ([https://w3id.org/cerif/model#Person\_ResultPublication](https://w3id.org/cerif/model#Person_ResultPublication)) with the [https://w3id.org/cerif/vocab/PersonOutputContributions#Publisher](https://w3id.org/cerif/vocab/PersonOutputContributions#Publisher) semantics |

## License[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#license "Permalink to this headline")

| Description: | The license of the publication. We recommend using URIs from the SPDX License List ([https://spdx.org/licenses/](https://spdx.org/licenses/)), which includes the Creative Commons licenses. |
| --- | --- |
| Use: | optional, possibly multiple (0..\*) |
| Representation: | XML element `License` containing the classification identifier and having a `scheme` attribute to specify the classification scheme identifier |
| CERIF: | the ResultPublication\_Classification ([https://w3id.org/cerif/model#ResultPublication\_Classification](https://w3id.org/cerif/model#ResultPublication_Classification)) |

## Subject[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#subject "Permalink to this headline")

| Description: | The subject of the publication from a classification |
| --- | --- |
| Use: | optional, possibly multiple (0..\*) |
| Representation: | XML element `Subject` containing the classification identifier and having a `scheme` attribute to specify the classification scheme identifier |
| CERIF: | the ResultPublication\_Classification ([https://w3id.org/cerif/model#ResultPublication\_Classification](https://w3id.org/cerif/model#ResultPublication_Classification)) |

## Keyword[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#keyword "Permalink to this headline")

| Description: | A single keyword or key expression. Please repeat to serialize separate keywords or key expressions. |
| --- | --- |
| Use: | optional, possibly multiple (0..\*) |
| Representation: | XML element `Keyword` as a multilingual string |
| CERIF: | the ResultPublication.Keywords attribute ([https://w3id.org/cerif/model#ResultPublication.Keywords](https://w3id.org/cerif/model#ResultPublication.Keywords)) |

## Abstract[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#abstract "Permalink to this headline")

| Use: | optional, possibly multiple (0..\*) |
| --- | --- |
| Representation: | XML element `Abstract` as a multilingual string |
| CERIF: | the ResultPublication.Abstract attribute ([https://w3id.org/cerif/model#ResultPublication.Abstract](https://w3id.org/cerif/model#ResultPublication.Abstract)) |

## Status[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#status "Permalink to this headline")

| Use: | optional, possibly multiple (0..\*) |
| --- | --- |
| Representation: | XML element `Status` containing the classification identifier and having a `scheme` attribute to specify the classification scheme identifier |
| CERIF: | the ResultPublication\_Classification ([https://w3id.org/cerif/model#ResultPublication\_Classification](https://w3id.org/cerif/model#ResultPublication_Classification)) |

## OriginatesFrom[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#originatesfrom "Permalink to this headline")

| Use: | optional, possibly multiple (0..\*) |
| --- | --- |
| Representation: | XML element `OriginatesFrom` with embedded XML element `Project` or `Funding` |
| CERIF: | the Project\_ResultPublication linking entity ([https://w3id.org/cerif/model#Project\_ResultPublication](https://w3id.org/cerif/model#Project_ResultPublication)) with the [https://w3id.org/cerif/vocab/ProjectOutputRoles#Originator](https://w3id.org/cerif/vocab/ProjectOutputRoles#Originator) semantics; the ResultPublication\_Funding linking entity ([https://w3id.org/cerif/model#ResultPublication\_Funding](https://w3id.org/cerif/model#ResultPublication_Funding)) with the [https://w3id.org/cerif/vocab/OutputFundingRoles#Originator](https://w3id.org/cerif/vocab/OutputFundingRoles#Originator) semantics |

## PresentedAt[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#presentedat "Permalink to this headline")

| Description: | The event where this publication was presented. [\[1\]](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#id26) |
| --- | --- |
| Use: | optional, possibly multiple (0..\*) |
| Representation: | XML element `PresentedAt` with embedded XML element `Event` |
| CERIF: | the ResultPublication\_Event linking entity ([https://w3id.org/cerif/model#ResultPublication\_Event](https://w3id.org/cerif/model#ResultPublication_Event)) with the [https://w3id.org/cerif/vocab/EventOutputRelationships#Presented](https://w3id.org/cerif/vocab/EventOutputRelationships#Presented) semantics |

| [\[1\]](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#id25) | Note: Video recordings of conference presentations are stored as alternative representations of the primary object: the conference paper. It would be unneccessarily complex to represent them as separate, linked Products. |
| --- | --- |

## OutputFrom[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#outputfrom "Permalink to this headline")

| Description: | This publication contains the proceedings from the linked event |
| --- | --- |
| Use: | optional, possibly multiple (0..\*) |
| Representation: | XML element `OutputFrom` with embedded XML element `Event` |
| CERIF: | the ResultPublication\_Event linking entity ([https://w3id.org/cerif/model#ResultPublication\_Event](https://w3id.org/cerif/model#ResultPublication_Event)) with the [https://w3id.org/cerif/vocab/EventOutputRelationships#Output](https://w3id.org/cerif/vocab/EventOutputRelationships#Output) semantics |

## Coverage[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#coverage "Permalink to this headline")

| Description: | The event that is covered by this publication (e.g. a report about the event) |
| --- | --- |
| Use: | optional, possibly multiple (0..\*) |
| Representation: | XML element `Coverage` with embedded XML element `Event` |
| CERIF: | the ResultPublication\_Event linking entity ([https://w3id.org/cerif/model#ResultPublication\_Event](https://w3id.org/cerif/model#ResultPublication_Event)) with the [https://w3id.org/cerif/vocab/EventOutputRelationships#Coverage](https://w3id.org/cerif/vocab/EventOutputRelationships#Coverage) semantics |

## References[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#references "Permalink to this headline")

| Description: | Result outputs that are referenced by this publication |
| --- | --- |
| Use: | optional, possibly multiple (0..\*) |
| Representation: | XML element `References` with embedded XML element `Publication` or `Patent` or `Product` |
| CERIF: | the ResultPublication\_ResultPublication linking entity ([https://w3id.org/cerif/model#ResultPublication\_ResultPublication](https://w3id.org/cerif/model#ResultPublication_ResultPublication)) with the [https://w3id.org/cerif/vocab/InterOutputRelations#Reference](https://w3id.org/cerif/vocab/InterOutputRelations#Reference) semantics (direction :1); the ResultPublication\_ResultProduct linking entity ([https://w3id.org/cerif/model#ResultPublication\_ResultProduct](https://w3id.org/cerif/model#ResultPublication_ResultProduct)) with the [https://w3id.org/cerif/vocab/InterOutputRelations#Reference](https://w3id.org/cerif/vocab/InterOutputRelations#Reference) semantics (direction :1); the ResultPublication\_ResultPatent linking entity ([https://w3id.org/cerif/model#ResultPublication\_ResultPatent](https://w3id.org/cerif/model#ResultPublication_ResultPatent)) with the [https://w3id.org/cerif/vocab/InterOutputRelations#Reference](https://w3id.org/cerif/vocab/InterOutputRelations#Reference) semantics (direction :1) |

## ns4:Access[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#ns4-access "Permalink to this headline")

| Description: | The open access type of the publication |
| --- | --- |
| Use: | optional (0..1) |
| Representation: | XML element `Access` from namespace [http://purl.org/coar/access\_right](http://purl.org/coar/access_right) |
| CERIF: | the ResultPublication\_Classification ([https://w3id.org/cerif/model#ResultPublication\_Classification](https://w3id.org/cerif/model#ResultPublication_Classification)) |
| Vocabulary: | - **open access** ([http://purl.org/coar/access\_right/c\_abf2](http://purl.org/coar/access_right/c_abf2)): Open access refers to a resource that is immediately and permanently online, and free for all on the Web, without financial and technical barriers.The resource is either stored in the repository or referenced to an external journal or trustworthy archive. - **embargoed access** ([http://purl.org/coar/access\_right/c\_f1cf](http://purl.org/coar/access_right/c_f1cf)): Embargoed access refers to a resource that is metadata only access until released for open access on a certain date. Embargoes can be required by publishers and funders policies, or set by the author (e.g such as in the case of theses and dissertations). - **restricted access** ([http://purl.org/coar/access\_right/c\_16ec](http://purl.org/coar/access_right/c_16ec)): Restricted access refers to a resource that is available in a system but with some type of restriction for full open access. This type of access can occur in a number of different situations. Some examples are described below: The user must log-in to the system in order to access the resource The user must send an email to the author or system administrator to access the resource Access to the resource is restricted to a specific community (e.g. limited to a university community) - **metadata only access** ([http://purl.org/coar/access\_right/c\_14cb](http://purl.org/coar/access_right/c_14cb)): Metadata only access refers to a resource in which access is limited to metadata only. The resource itself is described by the metadata, but neither is directly available through the system or platform nor can be referenced to an open access copy in an external journal or trustworthy archive. |

## FileLocations[¶](https://openaire-guidelines-for-cris-managers.readthedocs.io/en/v1.2.0/#filelocations "Permalink to this headline")

| Description: | The files that this Publication has as contents. |
| --- | --- |
| Use: | optional (0..1) |
| Representation: | XML element `FileLocations` with embedded XML element `Medium` |
| CERIF: | the ResultPublication\_Medium linking entity ([https://w3id.org/cerif/model#ResultPublication\_Medium](https://w3id.org/cerif/model#ResultPublication_Medium)) with the [https://w3id.org/cerif/vocab/MediaRelations#Contents](https://w3id.org/cerif/vocab/MediaRelations#Contents) semantics |
