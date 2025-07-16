import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables from the .env file in the project root
# This line looks for a .env file and loads its key-value pairs as environment variables.
load_dotenv()

# --- DATABASE CONFIGURATION ---
# Retrieve database credentials securely from the environment variables.
# os.getenv() fetches the value of a variable, returning None if it's not found.
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# Check if all required environment variables are set
if not all([DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME]):
    raise ValueError("One or more database environment variables are not set. Please check your .env file.")

# The connection string for your MySQL database, constructed from the environment variables.
# Using an f-string to build the URL makes the code clean and readable.
SQLALCHEMY_DATABASE_URL = (
    f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)


# --- SQLALCHEMY ENGINE ---
# The engine is the central point of contact for the database.
# It manages the connection pool and dialect for communicating with the DB.
engine = create_engine(SQLALCHEMY_DATABASE_URL)


# --- DATABASE SESSION ---
# A SessionLocal class is created. Each instance of SessionLocal will be a
# database session. This is the primary interface for all database operations.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# --- DECLARATIVE BASE ---
# We will inherit from this class to create each of the ORM models (database tables).
# It provides the base functionality for SQLAlchemy's declarative class mapping.
Base = declarative_base()


# --- DEPENDENCY FOR GETTING DB SESSION ---
def get_db():
    """
    A generator function that yields a database session for a single request
    and ensures it's properly closed afterward using a try...finally block.
    This is a dependency that will be injected into our API endpoint functions.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()