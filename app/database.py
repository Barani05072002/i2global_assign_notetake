from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

MYSQL_USER = os.getenv("MYSQL_USER","root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD","password")
MYSQL_HOST = os.getenv("MYSQL_HOST","localhost")
MYSQL_PORT = os.getenv("MYSQL_PORT","3306")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE","NoteTakeApp")

URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"

engine = create_engine(URL)

SessionLocal = sessionmaker(bind=engine,autoflush=False,autocommit=False)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()