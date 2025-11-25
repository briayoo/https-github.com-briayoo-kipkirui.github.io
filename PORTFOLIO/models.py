"""
Database models using SQLAlchemy
User, Project, and other data models
"""

from datetime import datetime
from database import db
from base import TimestampMixin, SerializerMixin

class User(db.Model, TimestampMixin, SerializerMixin):
    """User model for authentication and profiles"""
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    
    # Relationships
    projects = db.relationship('Project', backref='user', lazy=True)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_timestamps()
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def to_dict(self):
        """Convert user to dictionary"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Project(db.Model, TimestampMixin, SerializerMixin):
    """Project model for portfolio items"""
    
    __tablename__ = 'projects'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    technologies = db.Column(db.String(300))
    github_url = db.Column(db.String(200))
    live_url = db.Column(db.String(200))
    image_url = db.Column(db.String(200))
    featured = db.Column(db.Boolean, default=False)
    completed = db.Column(db.Boolean, default=False)
    completion_date = db.Column(db.DateTime)
    
    # Foreign key
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_timestamps()
    
    def __repr__(self):
        return f'<Project {self.title}>'
    
    def to_dict(self):
        """Convert project to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'technologies': self.technologies,
            'github_url': self.github_url,
            'live_url': self.live_url,
            'image_url': self.image_url,
            'featured': self.featured,
            'completed': self.completed,
            'completion_date': self.completion_date.isoformat() if self.completion_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class ContactMessage(db.Model, TimestampMixin):
    """Contact message model"""
    
    __tablename__ = 'contact_messages'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    read = db.Column(db.Boolean, default=False)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_timestamps()
    
    def __repr__(self):
        return f'<ContactMessage from {self.name}>'