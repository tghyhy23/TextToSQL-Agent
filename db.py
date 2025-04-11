import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

def get_engine():
    db_uri = os.getenv("DB_URI")
    if not db_uri:
        raise ValueError("Setup your DB_URI in file .env")
    engine = create_engine(db_uri)
    return engine
