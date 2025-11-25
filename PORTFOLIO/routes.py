"""
Application routes and view functions
URL routing and request handling
"""

from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from form import ContactForm, ProjectInquiryForm
from models import ContactMessage, Project, User
from database import db
from datetime import datetime

# Create blueprint
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    """Home page route"""
    featured_projects = Project.query.filter_by(featured=True, completed=True).all()
    return render_template('home.html', 
                         featured_projects=featured_projects,
                         title='Home - Python Developer Portfolio')

@main_bp.route('/about')
def about():
    """About page route"""
    skills = [
        'Python', 'Flask', 'Django', 'JavaScript', 'React',
        'PostgreSQL', 'Docker', 'AWS', 'REST APIs', 'Git'
    ]
    return render_template('about.html',
                         skills=skills,
                         title='About Me - Python Developer')

@main_bp.route('/services')
def services():
    """Services page route"""
    services_list = [
        {
            'name': 'Python Development',
            'description': 'Custom Python applications, automation scripts, and backend systems.',
            'icon': 'fab fa-python'
        },
        {
            'name': 'Web Applications',
            'description': 'Full-stack web development using Flask and Django.',
            'icon': 'fas fa-globe'
        },
        {
            'name': 'Database Design',
            'description': 'Efficient database architecture and optimization.',
            'icon': 'fas fa-database'
        },
        {
            'name': 'API Development',
            'description': 'RESTful API design and implementation.',
            'icon': 'fas fa-plug'
        }
    ]
    return render_template('my_service.html',
                         services=services_list,
                         title='My Services - Python Developer')

@main_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact page route"""
    form = ContactForm()
    
    if form.validate_on_submit():
        # Create new contact message
        message = ContactMessage(
            name=form.name.data,
            email=form.email.data,
            subject=form.subject.data,
            message=form.message.data
        )
        
        try:
            db.session.add(message)
            db.session.commit()
            flash('Thank you for your message! I will get back to you soon.', 'success')
            return redirect(url_for('main.contact'))
        except Exception as e:
            db.session.rollback()
            flash('Sorry, there was an error sending your message. Please try again.', 'error')
    
    return render_template('contact.html',
                         form=form,
                         title='Contact - Python Developer')

@main_bp.route('/api/contact', methods=['POST'])
def api_contact():
    """API endpoint for contact form"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Validate required fields
    required_fields = ['name', 'email', 'subject', 'message']
    for field in required_fields:
        if field not in data or not data[field].strip():
            return jsonify({'error': f'{field} is required'}), 400
    
    # Create contact message
    message = ContactMessage(
        name=data['name'],
        email=data['email'],
        subject=data['subject'],
        message=data['message']
    )
    
    try:
        db.session.add(message)
        db.session.commit()
        return jsonify({'message': 'Message sent successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to send message'}), 500

@main_bp.route('/projects')
def projects():
    """Projects showcase page"""
    projects = Project.query.filter_by(completed=True).order_by(Project.created_at.desc()).all()
    return render_template('projects.html',
                         projects=projects,
                         title='Projects - Python Developer')

@main_bp.route('/api/projects')
def api_projects():
    """API endpoint for projects"""
    projects = Project.query.filter_by(completed=True).all()
    projects_data = [project.to_dict() for project in projects]
    return jsonify(projects_data)

@main_bp.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()})

# Error handlers
@main_bp.app_errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@main_bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500