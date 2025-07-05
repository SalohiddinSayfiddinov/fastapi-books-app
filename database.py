import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Get the DATABASE_URL from environment or fallback to SQLite for local dev
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./books_app.db")

# Fix for Render.com's URL format (if needed)
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Enable SQL logging only for SQLite/local development
echo_setting = DATABASE_URL.startswith("sqlite")

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=echo_setting)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all ORM models
Base = declarative_base()

# Dependency to get a DB session (used in FastAPI routes)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Optional: Print connection info for Render debug logs (remove in prod if needed)
print(f"[INFO] Using database: {DATABASE_URL}")
