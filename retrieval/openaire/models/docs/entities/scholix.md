# "Scholix Schema 3.0 | OpenAIRE Graph Documentation"
(Source)[https://graph.openaire.eu/docs/apis/scholexplorer/v3/response_schema]

Here is a table describing each field in the schema:

| **Field** | **Type** | **Description** |
| --- | --- | --- |
| `LinkPublicationDate` | `string` (date) | Date of the linking publication. |
| `LinkProvider[]` | `array` (object) | Information about the provider of the link. |
| `LinkProvider[].name` | `string` | Name of the Datasource provides links. |
| `LinkProvider[].identifier[]` | `array` (object) | Identifiers associated with the link provider. |
| `LinkProvider[].identifier[].ID` | `string` | Identifier value. |
| `LinkProvider[].identifier[].IDScheme` | `string` | Identifier scheme. |
| `LinkProvider[].identifier[].IDURL` | `string` (URI) | URL associated with the identifier. |
| `RelationshipType` | `object` | Semantic of relationship between scholarly objects. |
| `RelationshipType.Name` | `string` | Name of the relationship semantic should be one of the following values `("IsSupplementTo","IsSupplementedBy", "References", "IsReferencedBy", "IsRelatedTo")` |
| `RelationshipType.SubType` | `string` | Specific subtype of the relationship described [here](https://graph.openaire.eu/docs/data-model/relationships/relationship-types). |
| `RelationshipType.SubTypeSchema` | `string` (URI) | URL of the schema defining the relationship subtype. |
| `LicenseURL` | `string` (URI) | URL of the license associated with the data. |
| `Source` | `object` | Metadata of the source entity. |
| `Source.Identifier` | `array` (object) | Identifiers of the source entity. |
| `Source.Identifier[].ID` | `string` | Persistent Identifier value. |
| `Source.Identifier[].IDScheme` | `string` | Persistent Identifier scheme. |
| `Source.Identifier[].IDURL` | `string` (URI) | URL associated with the Persistent identifier. |
| `Source.Type` | `string` | entity type (publication, dataset, software, other). |
| `Source.SubType` | `string` | Specific subtype of entity (e.g., Article, Dataset). |
| `Source.Title` | `string` | Title of the entity. |
| `Source.Creator[]` | `array` (object) | Creators of the entity. |
| `Source.Creator[].Name` | `string` | Name of the creator. |
| `Source.Creator[].Identifier` | `object` | Persistent Identifier of the creator. |
| `Source.Creator[].Identifier.ID` | `string` | Persistent Identifier value. |
| `Source.Creator[].Identifier.IDScheme` | `string` | Identifier scheme. |
| `Source.Creator[].Identifier.IDURL` | `string` (URI) | URL associated with the Persistent identifier. |
| `Source.PublicationDate` | `string` (date) | Date of publication. |
| `Source.Publisher[]` | `array` (object) | Publishers of the Entity. |
| `Source.Publisher[].name` | `string` | Name of the publisher. |
| `Source.Publisher[].Identifier[]` | `object` | Persistent Identifier of the publisher. |
| `Source.Publisher[].Identifier[].ID` | `string` | Persistent Identifier value. |
| `Source.Publisher[].Identifier[].IDScheme` | `string` | Identifier scheme. |
| `Source.Publisher[].Identifier[].IDURL` | `string` (URI) | URL associated with the identifier. |
| `Target` | `object` | Metadata of the target entity |
| `Target.Identifier` | `array` (object) | Identifiers of the target entity. |
| `Target.Identifier[].ID` | `string` | Persistent Identifier value. |
| `Target.Identifier[].IDScheme` | `string` | Persistent Identifier scheme. |
| `Target.Identifier[].IDURL` | `string` (URI) | URL associated with the Persistent identifier. |
| `Target.Type` | `string` | entity type (publication, dataset, software, other). |
| `Target.SubType` | `string` | Specific subtype of entity (e.g., Article, Dataset). |
| `Target.Title` | `string` | Title of the entity. |
| `Target.Creator[]` | `array` (object) | Creators of the entity. |
| `Target.Creator[].Name` | `string` | Name of the creator. |
| `Target.Creator[].Identifier` | `object` | Persistent Identifier of the creator. |
| `Target.Creator[].Identifier.ID` | `string` | Persistent Identifier value. |
| `Target.Creator[].Identifier.IDScheme` | `string` | Identifier scheme. |
| `Target.Creator[].Identifier.IDURL` | `string` (URI) | URL associated with the Persistent identifier. |
| `Target.PublicationDate` | `string` (date) | Date of publication. |
| `Target.Publisher[]` | `array` (object) | Publishers of the Entity. |
| `Target.Publisher[].name` | `string` | Name of the publisher. |
| `Target.Publisher[].Identifier[]` | `object` | Persistent Identifier of the publisher. |
| `Target.Publisher[].Identifier[].ID` | `string` | Persistent Identifier value. |
| `Target.Publisher[].Identifier[].IDScheme` | `string` | Identifier scheme. |
| `Target.Publisher[].Identifier[].IDURL` | `string` (URI) | URL associated with the identifier. |

