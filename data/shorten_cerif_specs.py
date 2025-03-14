#!/usr/bin/env python3
"""
Script to shorten CERIF specification RDF file by removing redundancy and extracting
essential elements needed for constructing CERIF files according to the specs.

The original specification contains many repetitions and verbose descriptions.
This script preserves crucial information while making it more concise.
"""

import datetime
import json
import os
import re
from pathlib import Path


def clean_text(text):
    """Clean and normalize text content."""
    if text is None:
        return ""

    # Remove excessive whitespace
    text = re.sub(r"\s+", " ", text)
    # Trim
    text = text.strip()
    return text


def extract_entities_from_text(text):
    """Extract CERIF entity identifiers from text."""
    # Match patterns like cfPerson, cfProject, cfResult, etc.
    entity_pattern = r"cf[A-Z][a-zA-Z]+"
    return sorted(set(re.findall(entity_pattern, text)))


def extract_link_tables_from_text(text):
    """Extract CERIF link tables from text."""
    # Match patterns like cfPerson_Equipment, cfProject_Facility, etc.
    link_pattern = r"cf[A-Z][a-zA-Z]+_[A-Z][a-zA-Z]+"
    return sorted(set(re.findall(link_pattern, text)))


def extract_attributes(text, entity_name=None):
    """Extract attribute names for a specific entity or all attributes if entity_name is None."""
    if entity_name:
        # Look for attributes specific to an entity
        pattern = rf"{entity_name}([A-Z][a-zA-Z]+)"
        matches = re.findall(pattern, text)
        return sorted(set(f"{entity_name}{m}" for m in matches))
    else:
        # General attribute pattern
        pattern = r"cf[A-Z][a-zA-Z]+[A-Z][a-zA-Z]+"
        # Exclude link tables (with underscore)
        matches = [m for m in re.findall(pattern, text) if "_" not in m]
        return sorted(set(matches))


def extract_relationships(link_tables):
    """Extract entity relationships from link table names."""
    relationships = {}

    for link in link_tables:
        parts = link.split("_")
        if len(parts) == 2:
            entity1, entity2 = parts

            # Add to relationships dictionary
            if entity1 not in relationships:
                relationships[entity1] = []
            if entity2 not in relationships:
                relationships[entity2] = []

            relationships[entity1].append({"related_to": entity2, "through": link})
            relationships[entity2].append({"related_to": entity1, "through": link})

    return relationships


def extract_key_descriptions(text):
    """Extract key conceptual descriptions from the text."""
    # Find explanatory paragraphs about CERIF concepts
    key_concepts = {}

    # Extract description about identifiers
    id_match = re.search(
        r"(A classification.*?uniquely identified.*?cfClassId.*?attribute.*?uuid.*?)",
        text,
    )
    if id_match:
        key_concepts["identifiers"] = clean_text(id_match.group(1))

    # Extract description about classifications
    class_match = re.search(r"(classification examples grouped by.*?scheme.*?)", text)
    if class_match:
        key_concepts["classifications"] = clean_text(class_match.group(1))

    # Extract info about entity types
    entity_types = {}
    for entity_type in [
        "Person",
        "Organisation",
        "Project",
        "Publication",
        "Patent",
        "Product",
        "Facility",
        "Equipment",
        "Service",
    ]:
        pattern = rf"cf{entity_type}\w+"
        matches = re.findall(pattern, text)
        if matches:
            entity_types[f"cf{entity_type}"] = sorted(list(set(matches)))

    key_concepts["entity_types"] = entity_types

    return key_concepts


def extract_classification_schemes(text):
    """Extract classification schemes mentioned in the specification."""
    # Look for mentions of classification schemes
    scheme_pattern = r"scheme i\.e\. ([^,\.]+)"
    schemes = re.findall(scheme_pattern, text)

    # Clean and deduplicate
    schemes = [clean_text(s) for s in schemes]
    return sorted(list(set(schemes)))


def analyze_entity_hierarchy(entities, link_tables):
    """Analyze potential hierarchy among entities based on naming conventions."""
    hierarchy = {}

    # Group similar entities (e.g., cfResult, cfResultPublication, cfResultPatent)
    for entity in entities:
        # Skip link tables
        if "_" in entity:
            continue

        # Find parent entity if this is a subtype
        parent = None
        for potential_parent in entities:
            if potential_parent != entity and entity.startswith(potential_parent):
                # This is a potential parent-child relationship
                if parent is None or len(potential_parent) > len(parent):
                    parent = potential_parent

        if parent:
            if parent not in hierarchy:
                hierarchy[parent] = []
            hierarchy[parent].append(entity)

    return hierarchy


def shorten_specification(input_file, output_file):
    """Main function to shorten the CERIF specification."""
    try:
        # Read the content of the XML file
        with open(input_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Extract all text content (simplified approach)
        # Note: This isn't perfect XML parsing but helps avoid namespace issues
        text_content = re.sub(r"<.*?>", " ", content)

        # Remove duplicate paragraphs to clean up the text
        clean_content = remove_duplicates(text_content)

        # Extract entities, link tables and attributes
        entities = extract_entities_from_text(clean_content)
        link_tables = extract_link_tables_from_text(clean_content)
        all_attributes = extract_attributes(clean_content)

        # Group attributes by entity
        entity_attributes = {}
        for entity in entities:
            entity_attributes[entity] = extract_attributes(clean_content, entity)

        # Extract relationships from link tables
        relationships = extract_relationships(link_tables)

        # Extract key conceptual descriptions
        key_descriptions = extract_key_descriptions(clean_content)

        # Extract classification schemes
        classification_schemes = extract_classification_schemes(clean_content)

        # Analyze entity hierarchy
        hierarchy = analyze_entity_hierarchy(entities, link_tables)

        # Build the shortened specification
        shortened_spec = {
            "metadata": {
                "original_file": os.path.basename(input_file),
                "creation_date": datetime.datetime.now().isoformat(),
                "description": "Shortened CERIF specification with essential elements for schema construction",
            },
            "entities": {
                entity: {
                    "attributes": entity_attributes.get(entity, []),
                    "relationships": relationships.get(entity, []),
                }
                for entity in entities
                if "_" not in entity
            },
            "link_tables": {
                link: {"connects": link.split("_") if "_" in link else []}
                for link in link_tables
            },
            "classification_schemes": classification_schemes,
            "entity_hierarchy": hierarchy,
            "key_concepts": key_descriptions,
            "summary": {
                "entity_count": len([e for e in entities if "_" not in e]),
                "link_table_count": len(link_tables),
                "attribute_count": len(all_attributes),
            },
        }

        # Save the shortened specification
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(shortened_spec, f, indent=2)

        # Calculate compression
        original_size = len(content)
        shortened_size = os.path.getsize(output_file)
        compression_ratio = original_size / shortened_size if shortened_size > 0 else 0

        print(f"Shortened CERIF specification saved to {output_file}")
        print(
            f"Reduced from approximately {original_size:,} characters to {shortened_size:,} bytes"
        )
        print(f"Compression ratio: {compression_ratio:.2f}x")
        print(
            f"Found {shortened_spec['summary']['entity_count']} entities, {shortened_spec['summary']['link_table_count']} link tables, and {shortened_spec['summary']['attribute_count']} attributes"
        )

        # Return statistics for verification
        return {
            "original_size": original_size,
            "shortened_size": shortened_size,
            "compression_ratio": compression_ratio,
        }

    except Exception as e:
        print(f"Error processing CERIF specification: {str(e)}")
        import traceback

        traceback.print_exc()
        return {"error": str(e)}


def remove_duplicates(text):
    """Remove duplicate paragraphs from text."""
    if not text:
        return ""

    # Split into paragraphs
    paragraphs = re.split(r"\n{2,}", text)

    # Remove duplicates while preserving order
    seen = set()
    unique_paragraphs = []

    for para in paragraphs:
        clean_para = clean_text(para)
        if clean_para and clean_para not in seen and len(clean_para) > 5:
            seen.add(clean_para)
            unique_paragraphs.append(para)

    return "\n\n".join(unique_paragraphs)


def analyze_common_patterns(text):
    """Analyze common patterns in the specification text."""
    # This function could be expanded to identify frequent patterns
    # or structures in the CERIF specification that could help with generating
    # the schema automatically

    # Example patterns to look for
    patterns = {
        "identifiers": r"cf\w+Id\b",
        "names": r"cf\w+Name\b",
        "descriptions": r"cf\w+Description\b",
    }

    results = {}
    for pattern_name, pattern in patterns.items():
        matches = re.findall(pattern, text)
        results[pattern_name] = sorted(list(set(matches)))

    return results


if __name__ == "__main__":
    # Determine script directory for relative paths
    script_dir = Path(__file__).parent.absolute()

    # Input and output file paths
    input_file = script_dir / "cerif_specification.rdf"
    output_file = script_dir / "cerif_specification_shortened.json"

    stats = shorten_specification(input_file, output_file)

    if "error" not in stats:
        print("Done! Specification successfully shortened.")
    else:
        print(f"Error occurred during processing: {stats['error']}")
