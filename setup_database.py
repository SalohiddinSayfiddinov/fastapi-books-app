#!/usr/bin/env python3
"""
Database setup script for Render.com deployment
Run this script to initialize the database and create tables
"""

import os
import sys
from database import engine, Base
from auth.models import User

def setup_database():
    """Create all database tables"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

def check_database_connection():
    """Check if database connection is working"""
    try:
        # Try to connect to the database
        with engine.connect() as connection:
            result = connection.execute("SELECT 1")
            print("Database connection successful!")
            return True
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False

if __name__ == "__main__":
    print("Setting up database for FastAPI Books App...")
    
    # Check database connection
    if not check_database_connection():
        sys.exit(1)
    
    # Setup database tables
    setup_database()
    
    print("Database setup completed!") 