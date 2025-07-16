import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# --- DATABASE CONFIGURATION ---
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

if not all([DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME]):
    print("Error: One or more database environment variables are not set.")
    sys.exit(1)

SQLALCHEMY_DATABASE_URL = (
    f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# --- SQLALCHEMY ENGINE ---
try:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    # Test the connection to ensure it's valid
    with engine.connect() as connection:
        print("Successfully connected to the database.")
except SQLAlchemyError as e:
    print(f"Error connecting to the database: {e}")
    # Exit the application if a database connection cannot be established
    sys.exit(1)


# --- DATABASE SESSION ---
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# --- DECLARATIVE BASE ---
Base = declarative_base()


# --- DEPENDENCY FOR GETTING DB SESSION ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
