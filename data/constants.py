"""
This module defines global constants used throughout the application.
e.g., file paths, API keys, etc.
sensitive info will be imported from a .env file / environment variables at runtime.
Some specific constants will be split into separate files for better organization, e.g. data definitions, CERIF structure, etc

guidelines:
- store key-value pairs as enums
- use uppercase for constants
- use descriptive names for constants
- prefix constants with a short identifier for their use, e.g., "API_" for API keys
- use pathlib instead of os for file paths and operations wherever possible
- use dotenv to load environment variables from a .env file
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
            with open(Path(__file__).parent / ".env", "w") as f:
                f.write("# Add your environment variables here\n")
                f.write("# e.g., API_KEY=your_api_key\n")

            raise FileNotFoundError(
                f"No .env file found in root directory {Path(__file__).parent}. A template .env has been created at {Path(__file__).parent / '.env'}. Please open the file, fill in the required variables and rerun the script."
            )
