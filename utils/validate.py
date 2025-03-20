"""
functions to parse, normalize, standardize, and validate identifiers

use function get_validator to retrieve the function from a str representation of the identifier,
or use the specific function directly.
"""

import re
import uuid
from collections.abc import Callable

# Regular expressions for various identifier formats

DOI_REGEX = re.compile(r"^10\.\d{4,9}/[-._;()/:A-Z0-9]+$", re.IGNORECASE)
ORCID_REGEX = re.compile(r"^(\d{4}-\d{4}-\d{4}-\d{3}[X0-9])$")
ISBN10_REGEX = re.compile(r"^(?:\d[- ]?){9}[\dxX]$")
ISBN13_REGEX = re.compile(r"^(?:97(?:8|9)[- ]?)?(?:\d[- ]?){9}[\dxX]$")
SCOPUS_REGEX = re.compile(r"^\d{5,12}$")
PMID_REGEX = re.compile(r"^\d{1,8}$")
EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
URL_REGEX = re.compile(
    r"^(https?:\/\/)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)$"
)
ARXIV_OLD_REGEX = re.compile(r"^(\d{4}\.\d{4})(v\d+)?$")
ARXIV_NEW_REGEX = re.compile(r"^(\d{2})(\d{2})\.(\d{4,5})(v\d+)?$")
UUID_REGEX = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$",
    re.IGNORECASE,
)
MD5_REGEX = re.compile(r"^[0-9a-f]{32}$")
OPENALEX_ID_REGEX = re.compile(r"([WAICFVPST]\d{2,})")


def is_valid_input(input_value: any) -> bool:
    """
    Check if input is valid (not empty, None, or an exception)

    Args:
        input_value: The input value to check
    Returns:
        bool: True if input is valid, False otherwise
    """
    if isinstance(input_value, Exception):
        return False
    return not (
        input_value is None or isinstance(input_value, str) and not input_value.strip()
    )


def validate_input(input_value: any) -> str:
    """
    Validate that input is not empty, None, or an exception

    Args:
        input_value: The input value to validate
    Returns:
        str: The input as a string if valid
    Raises:
        ValueError: If the input is empty, None, or an exception
    """
    if isinstance(input_value, Exception):
        return input_value
    if input_value is None:
        raise ValueError("Input is None")
    if isinstance(input_value, str) and not input_value.strip():
        raise ValueError("Input is empty")
    return str(input_value).strip()


def clean_prefix(input_str: str, prefixes: dict[str, str]) -> str:
    """
    Remove common prefixes from a string and normalize it

    Args:
        input_str (str): The string to normalize
        prefixes (dict): Dictionary mapping prefixes to their replacements
    Returns:
        str: The normalized string with prefixes removed
    """
    input_str = input_str.lower().strip()
    for prefix, replacement in prefixes.items():
        if input_str.startswith(prefix):
            return input_str.replace(prefix, replacement).strip()
    return input_str


def validate_doi(doi: str) -> str:
    """
    Validate a DOI (Digital Object Identifier) string.
    The function normalizes the DOI by removing common prefixes and ensuring it starts with "10.".
    If the DOI does not match the required format, a ValueError is raised.

    Args:
        doi (str): The DOI string to validate and normalize.
    Returns:
        str: The normalized DOI string.
    Raises:
        ValueError: If the DOI is empty, None, or does not match the expected format.
    """
    try:
        doi = validate_input(doi)
    except ValueError as e:
        raise ValueError(f"Invalid DOI: {e}") from None

    prefixes = {
        "https://doi.org/": "",
        "http://dx.doi.org/": "",
        "https://dx.doi.org/": "",
        "doi:": "",
        "doi.org/": "",
    }

    stripped_doi = clean_prefix(doi, prefixes)

    # Special case handling
    if stripped_doi.startswith("/"):
        stripped_doi = stripped_doi.replace("/", "")
    elif stripped_doi.startswith("0."):
        stripped_doi = stripped_doi.replace("0.", "10.")
    elif not stripped_doi.startswith("10"):
        try:
            stripped_doi = "10." + doi.split(sep="10.")[-1].strip()
        except Exception as e:
            error_str = f"Input not recognized as a DOI: {doi}. Error: {e}"
            raise ValueError(error_str) from None

    if not stripped_doi:
        error_str = f"Input not recognized as a DOI: {doi}"
        raise ValueError(error_str)

    if DOI_REGEX.match(stripped_doi) is None:
        error_str = f"Cannot parse input to DOI. Input: {doi} - Parsed: {stripped_doi}"
        raise ValueError(error_str)

    return stripped_doi


def validate_isbn(input: str) -> str:
    """
    Validate and normalize ISBN-10 or ISBN-13 format.

    Args:
        input (str): The ISBN string to validate
    Returns:
        str: The normalized ISBN
    Raises:
        ValueError: If the input is not a valid ISBN
    """
    try:
        isbn = validate_input(input)
    except ValueError as e:
        raise ValueError(f"Invalid ISBN: {e}") from None

    prefixes = {
        "isbn:": "",
        "isbn-10:": "",
        "isbn-13:": "",
        "isbn10:": "",
        "isbn13:": "",
    }

    clean_isbn = clean_prefix(isbn, prefixes)
    clean_isbn = re.sub(r"[- ]", "", clean_isbn)

    ISBN10_LEN = 10
    ISBN13_LEN = 13
    # Validate ISBN-10
    if len(clean_isbn) == ISBN10_LEN:
        if not ISBN10_REGEX.match(clean_isbn):
            raise ValueError(f"Invalid ISBN-10 format: {input}")

        checksum = 0
        for i in range(ISBN10_LEN - 1):
            checksum += int(clean_isbn[i]) * (10 - i)

        check_digit = clean_isbn[ISBN10_LEN - 1].upper()
        check_digit = 10 if check_digit == "X" else int(check_digit)

        if (checksum + check_digit) % 11 != 0:
            raise ValueError(f"Invalid ISBN-10 checksum: {input}")

        return f"{clean_isbn[0]}-{clean_isbn[1:4]}-{clean_isbn[4:9]}-{clean_isbn[9]}"

    # Validate ISBN-13
    if len(clean_isbn) == ISBN13_LEN:
        if not clean_isbn.isdigit():
            raise ValueError(f"Invalid ISBN-13 format: {input}")

        checksum = 0
        for i in range(ISBN13_LEN - 1):
            checksum += int(clean_isbn[i]) * (3 if i % 2 else 1)

        check_digit = (10 - (checksum % 10)) % 10

        if int(clean_isbn[ISBN13_LEN - 1]) != check_digit:
            raise ValueError(f"Invalid ISBN-13 checksum: {input}")

        return f"{clean_isbn[0:3]}-{clean_isbn[3]}-{clean_isbn[4:9]}-{clean_isbn[9:12]}-{clean_isbn[12]}"

    raise ValueError(f"Invalid ISBN length ({len(clean_isbn)} digits): {input}")


def validate_scopus_id(input: str) -> str:
    """
    Validate Scopus ID format.
    Scopus IDs are unique identifiers for authors in the Scopus database.
    They are typically in the format of a 7-digit number, such as "1234567".

    Args:
        input (str): The Scopus ID to validate
    Returns:
        str: The normalized Scopus ID
    Raises:
        ValueError: If the input is not a valid Scopus ID
    """
    try:
        scopus_id = validate_input(input)
    except ValueError as e:
        raise ValueError(f"Invalid Scopus ID: {e}") from None

    prefixes = {
        "scopus:": "",
        "scopusid:": "",
        "scopus-id:": "",
        "scopus_id:": "",
    }

    clean_id = clean_prefix(scopus_id, prefixes)

    if not SCOPUS_REGEX.match(clean_id):
        raise ValueError(
            f"Invalid Scopus ID format. Expected 5-12 digits but got: {input}"
        )

    return clean_id


def validate_openaire_id(input: str) -> str:
    """
    Validate OpenAIRE ID format.

    OpenAIRE assigns internal identifiers for each object it collects. By default, the internal identifier is generated as
        sourcePrefix::md5(localId)
    with:
        sourcePrefix
            namespace prefix of 12 chars assigned to the data source at registration time
        localId
            identifier assigned to the object by the data source

    Args:
        input (str): The OpenAIRE ID to validate
    Returns:
        str: The normalized OpenAIRE ID
    Raises:
        ValueError: If the input is not a valid OpenAIRE ID
    """
    try:
        openaire_id = validate_input(input)
    except ValueError as e:
        raise ValueError(f"Invalid OpenAIRE ID: {e}") from None

    parts = openaire_id.split("::")

    if len(parts) != 2:  # noqa: PLR2004
        raise ValueError(
            f"Invalid OpenAIRE ID format. Expected 'sourcePrefix::md5hash' but got: {input}"
        )

    source_prefix, md5_hash = parts
    OPENAIRE_PREFIX_LEN = 12
    if len(source_prefix) != OPENAIRE_PREFIX_LEN:
        raise ValueError(
            f"Invalid source prefix length. Expected 12 characters but got {len(source_prefix)}: {input}"
        )

    if not re.match(MD5_REGEX, md5_hash.lower()):
        raise ValueError(f"Invalid MD5 hash in OpenAIRE ID: {input}")

    return f"{source_prefix}::{md5_hash.lower()}"


def validate_pmid(input: str) -> str:
    """
    Validate PubMed ID (PMID) format.
    PMIDs are integers between 1 and 99999999.

    Args:
        input (str): The PMID to validate
    Returns:
        str: The normalized PMID
    Raises:
        ValueError: If the input is not a valid PMID
    """
    try:
        pmid = validate_input(input)
    except ValueError as e:
        raise ValueError(f"Invalid PMID: {e}") from None

    prefixes = {
        "pmid:": "",
        "pubmed:": "",
        "pubmed id:": "",
        "pubmedid:": "",
    }

    clean_pmid = clean_prefix(pmid, prefixes)

    if not PMID_REGEX.match(clean_pmid):
        raise ValueError(f"Invalid PMID format. Expected 1-8 digits: {input}")

    pmid_int = int(clean_pmid)
    if pmid_int < 1 or pmid_int > 99999999:  # noqa: PLR2004
        raise ValueError(f"PMID out of range (1-99999999): {input}")

    return clean_pmid


def validate_arxiv_id(input: str) -> str:
    """
    Validate and normalize arXiv ID format.

    Args:
        input (str): The arXiv ID to validate
    Returns:
        str: The normalized arXiv ID
    Raises:
        ValueError: If the input is not a valid arXiv ID
    """
    try:
        arxiv_id = validate_input(input)
    except ValueError as e:
        raise ValueError(f"Invalid arXiv ID: {e}") from None

    prefixes = {
        "arxiv:": "",
        "arXiv:": "",
        "https://arxiv.org/abs/": "",
        "http://arxiv.org/abs/": "",
        "arxiv.org/abs/": "",
    }

    clean_id = clean_prefix(arxiv_id, prefixes)

    # Check for old format (before April 2007): YYMM.numbervV
    old_match = ARXIV_OLD_REGEX.match(clean_id)
    if old_match:
        base_id, version = old_match.groups()
        if version is None:
            version = ""
        return f"arXiv:{base_id}{version}"

    # Check for new format (starting April 2007): YYMM.number(vV)
    new_match = ARXIV_NEW_REGEX.match(clean_id)
    if new_match:
        year, month, number, version = new_match.groups()

        if int(year) < 7 or int(year) > 99:
            raise ValueError(f"Invalid arXiv ID year: {input}")

        if int(month) < 1 or int(month) > 12:
            raise ValueError(f"Invalid arXiv ID month: {input}")

        year_month = int(f"{year}{month}")
        if year_month < 1501:  # Before 2015-01
            if len(number) != 4:
                raise ValueError(
                    f"Invalid arXiv ID number format. Expected 4 digits for IDs before 1501: {input}"
                )
        elif len(number) != 5:
            raise ValueError(
                f"Invalid arXiv ID number format. Expected 5 digits for IDs from 1501 onwards: {input}"
            )

        if version is None:
            version = ""

        return f"arXiv:{year}{month}.{number}{version}"

    raise ValueError(f"Invalid arXiv ID format: {input}")


def validate_pure_id(input: str) -> str:
    """
    Validate Pure ID format (either an integer or UUID).

    Args:
        input (str): The Pure ID to validate
    Returns:
        str: The normalized Pure ID
    Raises:
        ValueError: If the input is not a valid Pure ID
    """
    try:
        pure_id = validate_input(input)
    except ValueError as e:
        raise ValueError(f"Invalid Pure ID: {e}") from None

    prefixes = {
        "pure:": "",
        "pureid:": "",
        "pure-id:": "",
        "pure_id:": "",
    }

    clean_id = clean_prefix(pure_id, prefixes)

    if clean_id.isdigit():
        return clean_id

    if UUID_REGEX.match(clean_id):
        try:
            # Validate UUID format
            return str(uuid.UUID(clean_id))
        except ValueError:
            raise ValueError(f"Invalid UUID format for Pure ID: {input}") from None

    raise ValueError(f"Invalid Pure ID format. Expected integer or UUID: {input}")


def validate_patent_number(input: str) -> str:
    """
    Validate and normalize patent number format.

    Args:
        input (str): The patent number to validate
    Returns:
        str: The normalized patent number
    Raises:
        ValueError: If the input is not a valid patent number
    """
    try:
        patent_num = validate_input(input)
    except ValueError as e:
        raise ValueError(f"Invalid patent number: {e}") from None

    # Patent numbers can have various formats depending on the country and type
    # This is a simplified validation focusing on common patent number formats

    us_pattern = re.compile(r"^(US)?[,\d]{1,10}$", re.IGNORECASE)
    ep_pattern = re.compile(r"^EP\d{6,8}(?:\.\d)?$", re.IGNORECASE)
    wo_pattern = re.compile(r"^WO\d{2,4}/\d{6}$", re.IGNORECASE)
    jp_pattern = re.compile(r"^JP\d{4}-\d{6}$", re.IGNORECASE)

    clean_patent = re.sub(r"\s", "", patent_num)

    if us_pattern.match(clean_patent):
        clean_patent = re.sub(r",", "", clean_patent)
        if not clean_patent.upper().startswith("US"):
            clean_patent = f"US{clean_patent}"
        return clean_patent.upper()

    if (
        (
            ep_pattern.match(clean_patent)
            or wo_pattern.match(clean_patent)
            or jp_pattern.match(clean_patent)
        )
        or re.search(r"\d", clean_patent)
        and len(clean_patent) >= 4
    ):
        return clean_patent.upper()
    raise ValueError(f"Unrecognized patent number format: {input}")


def validate_orcid(input: str) -> str:
    """
    Validate and normalize ORCID identifier format.

    ORCID uses 16-character identifiers with the digits 0-9 separated into groups of four by hyphens.
    By default, the ORCID identifier is represented in the form of a URL, such as https://orcid.org/0000-0002-9079-593X.

    Args:
        input (str): The ORCID identifier to validate
    Returns:
        str: The canonical form of the ORCID (https://orcid.org/0000-0002-9079-593X)
    Raises:
        ValueError: If the input is not a valid ORCID
    """
    try:
        orcid = validate_input(input)
    except ValueError as e:
        raise ValueError(f"Invalid ORCID: {e}") from None

    url_prefixes = [
        "https://orcid.org/",
        "http://orcid.org/",
        "orcid.org/",
        "orcid:",
    ]

    extracted_id = orcid
    for prefix in url_prefixes:
        if orcid.lower().startswith(prefix):
            extracted_id = orcid[len(prefix) :]
            break

    extracted_id = extracted_id.replace(" ", "").replace("/", "").replace("\\", "")

    if len(extracted_id) == 16 and "-" not in extracted_id:
        extracted_id = f"{extracted_id[0:4]}-{extracted_id[4:8]}-{extracted_id[8:12]}-{extracted_id[12:16]}"

    if not ORCID_REGEX.match(extracted_id):
        raise ValueError(
            f"Invalid ORCID format. Expected 4 groups of 4 digits/characters: {input}"
        )

    # Verify the checksum (ISO/IEC 7064:2003 MOD 11-2)
    digits = extracted_id.replace("-", "")
    total = 0
    for digit in digits[:-1]:
        total = (total + int(digit)) * 2
    last_digit = 10 if digits[-1] == "X" else int(digits[-1])

    checksum = (12 - (total % 11)) % 11
    if checksum == 10:
        checksum = "X"

    if str(checksum) != str(last_digit):
        raise ValueError(f"Invalid ORCID checksum: {input}") from None

    return f"https://orcid.org/{extracted_id}"


def validate_email(input: str) -> str:
    """
    Validate email format.

    Args:
        input (str): The email address to validate
    Returns:
        str: The normalized email address
    Raises:
        ValueError: If the input is not a valid email
    """
    try:
        email = validate_input(input)
    except ValueError as e:
        raise ValueError(f"Invalid email: {e}") from None

    email = email.strip().lower()

    if not EMAIL_REGEX.match(email):
        raise ValueError(f"Invalid email format: {input}")

    # check for valid TLD
    domain_parts = email.split("@")[1].split(".")
    if len(domain_parts[-1]) < 2:
        raise ValueError(f"Invalid email domain TLD: {input}")

    return email


def validate_url(input: str) -> str:
    """
    Validate URL format.

    Args:
        input (str): The URL to validate
    Returns:
        str: The normalized URL
    Raises:
        ValueError: If the input is not a valid URL
    """
    try:
        url = validate_input(input)
    except ValueError as e:
        raise ValueError(f"Invalid URL: {e}") from None

    url = url.strip()

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    if not URL_REGEX.match(url):
        raise ValueError(f"Invalid URL format: {input}")

    return url


def is_openalex_id(openalex_id: str):
    if not openalex_id:
        return False
    openalex_id = openalex_id.lower()
    if re.findall(r"http[s]://openalex.org/([waicfvpst]\d{2,})", openalex_id):
        return True
    if re.findall(r"^([waicfvpst]\d{2,})", openalex_id):
        return True
    return bool(re.findall(r"(openalex:[waicfvpst]\d{2,})", openalex_id))


def validate_openalex_id(openalex_id: str) -> str:
    if not is_openalex_id(openalex_id):
        raise ValueError(f"Input not recognized as an OpenAlex ID: {openalex_id}")
    openalex_id = openalex_id.strip().upper()
    matches: list[str] = re.findall(OPENALEX_ID_REGEX, openalex_id)
    if len(matches) == 0:
        raise ValueError(f"Input not recognized as an OpenAlex ID: {openalex_id}")

    return matches[0].replace("\0", "")


def get_full_openalex_id(openalex_id):
    short_openalex_id = validate_openalex_id(openalex_id)
    if short_openalex_id:
        full_openalex_id = f"https://openalex.org/{short_openalex_id}"
    else:
        full_openalex_id = None
    return full_openalex_id


def get_validator(identifier_str: str) -> None | Callable[[str], str]:
    """
    Get the validation function for a specific identifier type.

    Args:
        identifier_str (str): a str representation of the identifier to validate.

    Returns:
        function: The validation function for the specified identifier type.
    """
    if not is_valid_input(identifier_str):
        return None

    identifier_str = identifier_str.lower()
    if "_id" in identifier_str:
        identifier_str = identifier_str.replace("_id", "")
    for k, v in VALIDATION_MAPPING.items():
        if identifier_str in k:
            return v
    return None


VALIDATION_MAPPING: dict[str, Callable] = {
    "doi": validate_doi,
    "isbn": validate_isbn,
    "scopus_id": validate_scopus_id,
    "openaire_id": validate_openaire_id,
    "pmid": validate_pmid,
    "arxiv_id": validate_arxiv_id,
    "pure_id": validate_pure_id,
    "patent_number": validate_patent_number,
    "orcid": validate_orcid,
    "email": validate_email,
    "url": validate_url,
    "openalex_id": validate_openalex_id,
}
