import os

from dotenv import load_dotenv


def get_connection_string() -> str:
    load_dotenv()
    return os.getenv("PG_URL")
