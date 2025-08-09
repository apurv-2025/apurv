#!/usr/bin/env python3
"""
Script to create a test user for the Mental Health EHR system
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import Base, User
from app.auth import get_password_hash
import uuid

def create_test_user():
    """Create a test user for development/testing"""
    
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == "admin@clinic.com").first()
        if existing_user:
            print("✅ Test user 'admin@clinic.com' already exists!")
            print(f"   - Name: {existing_user.first_name} {existing_user.last_name}")
            print(f"   - Role: {existing_user.role}")
            return existing_user
        
        # Create test user
        test_user = User(
            id=str(uuid.uuid4()),
            email="admin@clinic.com",
            password_hash=get_password_hash("admin123"),
            first_name="Admin",
            last_name="User",
            role="admin",
            license_number="ADMIN001",
            is_active=True
        )
        
        db.add(test_user)
        db.commit()
        db.refresh(test_user)
        
        print("✅ Test user created successfully!")
        print(f"   - Email: {test_user.email}")
        print(f"   - Password: admin123")
        print(f"   - Name: {test_user.first_name} {test_user.last_name}")
        print(f"   - Role: {test_user.role}")
        
        return test_user
        
    except Exception as e:
        print(f"❌ Error creating test user: {e}")
        db.rollback()
        return None
    finally:
        db.close()

def create_additional_users():
    """Create additional test users"""
    db = SessionLocal()
    
    try:
        # Create a clinician user
        clinician = User(
            id=str(uuid.uuid4()),
            email="clinician@clinic.com",
            password_hash=get_password_hash("clinician123"),
            first_name="Dr. Jane",
            last_name="Smith",
            role="clinician",
            license_number="LIC001",
            is_active=True
        )
        
        # Create a supervisor user
        supervisor = User(
            id=str(uuid.uuid4()),
            email="supervisor@clinic.com",
            password_hash=get_password_hash("supervisor123"),
            first_name="Dr. John",
            last_name="Doe",
            role="supervisor",
            license_number="SUP001",
            is_active=True
        )
        
        # Check if they exist first
        existing_clinician = db.query(User).filter(User.email == "clinician@clinic.com").first()
        existing_supervisor = db.query(User).filter(User.email == "supervisor@clinic.com").first()
        
        if not existing_clinician:
            db.add(clinician)
            print("✅ Clinician user created: clinician@clinic.com / clinician123")
            
        if not existing_supervisor:
            db.add(supervisor)
            print("✅ Supervisor user created: supervisor@clinic.com / supervisor123")
            
        db.commit()
        
    except Exception as e:
        print(f"❌ Error creating additional users: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("🏥 Creating test users for Mental Health EHR...")
    print("=" * 50)
    
    # Create main admin user
    admin_user = create_test_user()
    
    if admin_user:
        # Create additional users
        create_additional_users()
        
        print("\n📝 Test Login Credentials:")
        print("=" * 30)
        print("1. Admin User:")
        print("   Email: admin@clinic.com")
        print("   Password: admin123")
        print("\n2. Clinician User:")
        print("   Email: clinician@clinic.com") 
        print("   Password: clinician123")
        print("\n3. Supervisor User:")
        print("   Email: supervisor@clinic.com")
        print("   Password: supervisor123")
        
        print(f"\n🚀 Backend API: http://127.0.0.1:8000")
        print(f"📖 API Docs: http://127.0.0.1:8000/docs")
        print(f"🌐 Frontend: http://localhost:3000")
        
    else:
        sys.exit(1)