"""
Database connection testing and utilities
Test scripts for database connectivity and operations
"""

import sqlite3
import sys
import os
from database import db, init_db
from app import create_app

def test_sqlite_connection():
    """Test basic SQLite connection"""
    try:
        conn = sqlite3.connect('portfolio.db')
        cursor = conn.cursor()
        
        # Test query
        cursor.execute("SELECT sqlite_version();")
        version = cursor.fetchone()
        
        print(f"✅ SQLite version: {version[0]}")
        print("✅ SQLite connection successful")
        
        conn.close()
        return True
        
    except sqlite3.Error as e:
        print(f"❌ SQLite connection failed: {e}")
        return False

def test_database_models():
    """Test database models and relationships"""
    try:
        # Create test app context
        app = create_app()
        
        with app.app_context():
            # Test database initialization
            init_db(app)
            print("✅ Database initialization successful")
            
            # Test model creation
            from models import User, Project
            
            # Create test user
            test_user = User(
                username="testuser",
                email="test@example.com",
                first_name="Test",
                last_name="User"
            )
            
            # Create test project
            test_project = Project(
                title="Test Project",
                description="A test project description",
                technologies="Python, Flask, SQLite",
                user_id=1,
                completed=True
            )
            
            print("✅ Model creation test successful")
            print(f"   User: {test_user}")
            print(f"   Project: {test_project}")
            
            return True
            
    except Exception as e:
        print(f"❌ Database model test failed: {e}")
        return False

def test_flask_app():
    """Test Flask application setup"""
    try:
        app = create_app()
        
        # Test app configuration
        assert app.config['DEBUG'] is not False, "Debug mode should be enabled"
        assert 'SECRET_KEY' in app.config, "Secret key should be configured"
        
        print("✅ Flask app configuration test successful")
        
        # Test database connection in app context
        with app.app_context():
            db.create_all()
            print("✅ Database tables created successfully")
            
        return True
        
    except Exception as e:
        print(f"❌ Flask app test failed: {e}")
        return False

def run_all_tests():
    """Run all connection tests"""
    print("🚀 Running Portfolio Application Tests...")
    print("=" * 50)
    
    tests = [
        ("SQLite Connection", test_sqlite_connection),
        ("Database Models", test_database_models),
        ("Flask Application", test_flask_app)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🧪 Running {test_name}...")
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    print("=" * 50)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    # Overall result
    all_passed = all(result[1] for result in results)
    if all_passed:
        print("\n🎉 All tests passed! Your portfolio setup is ready.")
    else:
        print("\n⚠️  Some tests failed. Please check the configuration.")
    
    return all_passed

if __name__ == "__main__":
    # Run tests when script is executed directly
    success = run_all_tests()
    sys.exit(0 if success else 1)