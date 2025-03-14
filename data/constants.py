"""
Global constants for the MEEWI application.

This module defines constants that are used throughout the application.
"""

from pathlib import Path

from dotenv import load_dotenv

# Load environment variables from .env file
try:
    load_dotenv(Path(__file__).parent / "secrets.env")
except Exception:
    try:
        load_dotenv(Path(__file__).parent / ".env")
    except Exception:
        matches = Path(__file__).parent.glob("*.env")
        if matches:
            load_dotenv(matches[0])
        else:
            with (Path(__file__).parent / ".env").open("w", encoding="utf-8") as f:
                f.write("# Add your environment variables here\n")
                f.write("# e.g., API_KEY=your_api_key\n")

            raise FileNotFoundError(
                f"No .env file found in root directory {Path(__file__).parent}. A template .env has been created at {Path(__file__).parent / '.env'}. Please open the file, fill in the required variables and rerun the script."
            ) from None

# Application paths
APP_ROOT = Path(__file__).parent.parent
DATA_DIR = APP_ROOT / "data"
EXPORT_DIR = APP_ROOT / "exports"
CACHE_DIR = APP_ROOT / "cache"
LOG_DIR = APP_ROOT / "logs"

# Default export format
DEFAULT_EXPORT_FORMAT = "json"


# Supported export formats
EXPORT_FORMATS: list[str] = ["json", "csv", "bibtex", "bib", "parquet", "cerif"]

# Retry settings
MAX_RETRIES = 3
RETRY_BACKOFF_FACTOR = 0.5
RETRY_STATUS_CODES = [429, 500, 502, 503, 504]

# Caching settings
CACHE_ENABLED = True
CACHE_TTL_DAYS = 30  # Time-to-live for cached data in days

# Publication types mapping
# Maps various publication type values from different sources to our standard types
