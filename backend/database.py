from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from urllib.parse import quote_plus
from dotenv import load_dotenv
import os

load_dotenv()

DB_PASSWORD = os.getenv("DB_PASSWORD")

DATABASE_URL = (
    f"postgresql://postgres:{quote_plus(DB_PASSWORD)}"
    "@localhost:5432/finance_db"
)

engine = create_engine(DATABASE_URL)

Base = declarative_base()