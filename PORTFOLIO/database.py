"""
Database configuration and setup
SQLAlchemy database instance and connection management
"""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    """Base class for all models"""
    pass

# Initialize SQLAlchemy
db = SQLAlchemy(model_class=Base)

def init_db(app):
    """Initialize database with app context"""
    with app.app_context():
        db.create_all()

def get_db_session():
    """Get database session"""
    return db.session

def close_db_session(exception=None):
    """Close database session"""
    db.session.remove()

class DatabaseManager:
    """Database management utilities"""
    
    @staticmethod
    def add_item(item):
        """Add item to database"""
        try:
            db.session.add(item)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error adding item: {e}")
            return False
    
    @staticmethod
    def delete_item(item):
        """Delete item from database"""
        try:
            db.session.delete(item)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting item: {e}")
            return False
    
    @staticmethod
    def update_item():
        """Commit changes to database"""
        try:
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error updating item: {e}")
            return False