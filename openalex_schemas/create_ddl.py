from pydantic import BaseModel


def generate_ddl(model: BaseModel, table_name: str = "works"):
    """Creates a DuckDB DDL statement to create a table based on the Pydantic model."""
    schema = model.model_json_schema()
    type_definitions = schema.get("$defs", {})
    processed_refs = set()

    def get_duckdb_type(property_schema):
        """Convert a JSON schema type to a DuckDB type"""
        if "anyOf" in property_schema:
            for type_option in property_schema["anyOf"]:
                if type_option.get("type") != "null" or "$ref" in type_option:
                    return get_duckdb_type(type_option)
            return "VARCHAR"  # Default if all options are null

        if "$ref" in property_schema:
            ref = property_schema["$ref"]
            if ref in processed_refs:
                return "JSON"  # Avoid circular references

            processed_refs.add(ref)
            ref_path = ref.split("/")
            if ref_path[0] == "#" and ref_path[1] == "$defs":
                ref_type_name = ref_path[2]
                if ref_type_name in type_definitions:
                    result = build_struct_type(type_definitions[ref_type_name])
                    processed_refs.remove(ref)
                    return result
            processed_refs.remove(ref)
            return "JSON"

        if "type" in property_schema:
            schema_type = property_schema["type"]

            if schema_type == "string":
                return "VARCHAR"
            if schema_type == "integer":
                return "INTEGER"
            if schema_type == "number":
                return "DOUBLE"
            if schema_type == "boolean":
                return "BOOLEAN"
            if schema_type == "array":
                if "items" in property_schema:
                    item_type = get_duckdb_type(property_schema["items"])
                    return f"{item_type}[]"
                return "VARCHAR[]"
            if schema_type == "object":
                return build_struct_type(property_schema)
            return "VARCHAR"

        return "JSON"  # Default for unknown types

    def build_struct_type(object_schema):
        """Build a STRUCT type from an object schema"""
        if "properties" not in object_schema:
            return "STRUCT()"

        properties = object_schema.get("properties", {})
        struct_fields = []

        for prop_name, prop_schema in properties.items():
            prop_type = get_duckdb_type(prop_schema)
            # Quote field names to handle special characters and reserve words
            struct_fields.append(f'"{prop_name}" {prop_type}')

        return f"STRUCT({', '.join(struct_fields)})"

    fields = []
    for prop_name, prop_schema in schema["properties"].items():
        field_type = get_duckdb_type(prop_schema)
        if prop_name == "id":
            fields.append(f'    "{prop_name}" {field_type} PRIMARY KEY')
        else:
            fields.append(f'    "{prop_name}" {field_type}')

    ddl = f"CREATE TABLE {table_name} (\n"
    ddl += ",\n".join(fields)
    ddl += "\n);"

    return ddl
