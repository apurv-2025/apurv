#!/usr/bin/env python3
"""
Database initialization script
Runs migrations and seeds initial data
"""

import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from migrations.initial_schema import run_migration
from seed_data import seed_database

def init_database():
    """Initialize the database with schema and seed data"""
    print("Initializing Medical Codes Database...")
    
    # Run migrations
    print("Running database migrations...")
    run_migration()
    
    # Seed the database
    print("Seeding database with sample data...")
    seed_database()
    
    print("Database initialization completed successfully!")

if __name__ == "__main__":
    init_database() 