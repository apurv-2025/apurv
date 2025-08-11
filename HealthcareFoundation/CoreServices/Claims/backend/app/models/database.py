# models/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Database URL - modify according to your PostgreSQL setup
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://fhir_user:fhir_password_2024!@localhost:5433/fhir_claims_db"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
