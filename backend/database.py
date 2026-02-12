from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WORKING_DB = os.path.join(BASE_DIR, 'system_design_ref.db')
STARTER_DB = os.path.join(BASE_DIR, 'starter.db')

# Auto-initialize from starter database if working database doesn't exist
if not os.path.exists(WORKING_DB) and os.path.exists(STARTER_DB):
    shutil.copy(STARTER_DB, WORKING_DB)
    print("✓ Created working database from starter.db")

DATABASE_URL = f"sqlite:///{WORKING_DB}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    Base.metadata.create_all(bind=engine)
