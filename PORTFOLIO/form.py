"""
Form definitions using WTForms
Contact forms and validation
"""

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, EmailField, BooleanField
from wtforms.validators import DataRequired, Email, Length, Optional

class ContactForm(FlaskForm):
    """Contact form for portfolio website"""
    
    name = StringField('Name', validators=[
        DataRequired(message='Name is required'),
        Length(min=2, max=100, message='Name must be between 2 and 100 characters')
    ])
    
    email = EmailField('Email', validators=[
        DataRequired(message='Email is required'),
        Email(message='Please enter a valid email address')
    ])
    
    subject = StringField('Subject', validators=[
        DataRequired(message='Subject is required'),
        Length(min=5, max=200, message='Subject must be between 5 and 200 characters')
    ])
    
    message = TextAreaField('Message', validators=[
        DataRequired(message='Message is required'),
        Length(min=10, max=1000, message='Message must be between 10 and 1000 characters')
    ])
    
    newsletter = BooleanField('Subscribe to newsletter', default=False)

class ProjectInquiryForm(FlaskForm):
    """Form for project inquiries"""
    
    project_type = StringField('Project Type', validators=[
        DataRequired(),
        Length(min=2, max=50)
    ])
    
    budget = StringField('Budget Range', validators=[
        DataRequired(),
        Length(min=2, max=50)
    ])
    
    timeline = StringField('Timeline', validators=[
        DataRequired(),
        Length(min=2, max=50)
    ])
    
    description = TextAreaField('Project Description', validators=[
        DataRequired(),
        Length(min=20, max=2000)
    ])

class NewsletterForm(FlaskForm):
    """Newsletter subscription form"""
    
    email = EmailField('Email', validators=[
        DataRequired(),
        Email()
    ])
    
    name = StringField('Name', validators=[
        Optional(),
        Length(max=100)
    ])