import os
from pathlib import Path
from urllib.parse import quote_plus

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

# Find .env in the project root
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR / ".env"

load_dotenv(ENV_FILE)

DB_PASSWORD = os.getenv("DB_PASSWORD")

if not DB_PASSWORD:
    raise ValueError(f"DB_PASSWORD is missing. Expected .env at: {ENV_FILE}")

DATABASE_URL = (
    f"postgresql://postgres:{quote_plus(DB_PASSWORD)}"
    "@localhost:5432/finance_db"
)

engine = create_engine(DATABASE_URL)

Base = declarative_base()