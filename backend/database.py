import os
from pathlib import Path
from urllib.parse import quote_plus

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

# Project root
BASE_DIR = Path(__file__).resolve().parent.parent

# Load local .env file
ENV_FILE = BASE_DIR / ".env"
load_dotenv(ENV_FILE)

# Use Render DATABASE_URL when available
DATABASE_URL = os.getenv("DATABASE_URL")

# If DATABASE_URL is not available, use local PostgreSQL
if not DATABASE_URL:
    DB_PASSWORD = os.getenv("DB_PASSWORD")

    if not DB_PASSWORD:
        raise ValueError(
            f"Neither DATABASE_URL nor DB_PASSWORD was found. "
            f"Expected .env at: {ENV_FILE}"
        )

    DATABASE_URL = (
        f"postgresql://postgres:{quote_plus(DB_PASSWORD)}"
        "@localhost:5432/finance_db"
    )

# Render may provide postgres:// instead of postgresql://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace(
        "postgres://",
        "postgresql://",
        1
    )

engine = create_engine(DATABASE_URL)

Base = declarative_base()