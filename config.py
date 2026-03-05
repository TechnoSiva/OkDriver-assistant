import os

from dotenv import load_dotenv


load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
PICOVOICE_ACCESS_KEY = os.getenv("PICOVOICE_ACCESS_KEY")
WAKE_WORD_PATH = os.getenv("WAKE_WORD_PATH", "wake_word.ppn")

missing_keys = [
    key_name
    for key_name, value in (
        ("GROQ_API_KEY", GROQ_API_KEY),
        ("PICOVOICE_ACCESS_KEY", PICOVOICE_ACCESS_KEY),
    )
    if not value
]

if missing_keys:
    raise ValueError(
        "Missing environment variables in .env: " + ", ".join(missing_keys)
    )
