// Portfolio Navigation and Functionality
class Portfolio {
    constructor() {
        this.currentSection = 'home';
        this.init();
    }

    init() {
        this.setupNavigation();
        this.setupContactForm();
        this.setupSocialLinks();
        this.setupProjectStructure();
        this.showSection('home');
    }

    // Navigation System
    setupNavigation() {
        const navLinks = document.querySelectorAll('.nav-link');
        
        navLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const section = link.getAttribute('data-section');
                this.showSection(section);
                
                // Update URL hash
                window.history.pushState(null, '', `#${section}`);
                
                // Scroll to top
                window.scrollTo({ top: 0, behavior: 'smooth' });
            });
        });

        // Handle browser back/forward buttons
        window.addEventListener('popstate', () => {
            const hash = window.location.hash.substring(1) || 'home';
            this.showSection(hash);
        });

        // Check initial URL hash
        const initialHash = window.location.hash.substring(1);
        if (initialHash) {
            this.showSection(initialHash);
        }
    }

    showSection(sectionId) {
        // Hide all sections
        document.querySelectorAll('.section').forEach(section => {
            section.classList.remove('active');
        });

        // Remove active class from all nav links
        document.querySelectorAll('.nav-link').forEach(link => {
            link.classList.remove('active');
        });

        // Show target section
        const targetSection = document.getElementById(sectionId);
        if (targetSection) {
            targetSection.classList.add('active');
            this.currentSection = sectionId;
        }

        // Activate corresponding nav link
        const activeLink = document.querySelector(`.nav-link[data-section="${sectionId}"]`);
        if (activeLink) {
            activeLink.classList.add('active');
        }
    }

    // Contact Form Handling
    setupContactForm() {
        const contactForm = document.getElementById('contactForm');
        if (!contactForm) return;

        contactForm.addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleFormSubmission(contactForm);
        });

        // Add input validation
        const inputs = contactForm.querySelectorAll('input, textarea');
        inputs.forEach(input => {
            input.addEventListener('blur', () => {
                this.validateField(input);
            });
            
            input.addEventListener('input', () => {
                this.clearFieldError(input);
            });
        });
    }

    validateField(field) {
        const value = field.value.trim();
        const fieldName = field.getAttribute('name');
        
        this.clearFieldError(field);

        if (field.hasAttribute('required') && !value) {
            this.showFieldError(field, 'This field is required');
            return false;
        }

        if (fieldName === 'email' && value) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(value)) {
                this.showFieldError(field, 'Please enter a valid email address');
                return false;
            }
        }

        return true;
    }

    showFieldError(field, message) {
        field.style.borderColor = '#dc3545';
        
        let errorElement = field.parentNode.querySelector('.field-error');
        if (!errorElement) {
            errorElement = document.createElement('div');
            errorElement.className = 'field-error';
            field.parentNode.appendChild(errorElement);
        }
        
        errorElement.textContent = message;
        errorElement.style.color = '#dc3545';
        errorElement.style.fontSize = '0.875rem';
        errorElement.style.marginTop = '5px';
    }

    clearFieldError(field) {
        field.style.borderColor = '#e9ecef';
        const errorElement = field.parentNode.querySelector('.field-error');
        if (errorElement) {
            errorElement.remove();
        }
    }

    async handleFormSubmission(form) {
        const formData = new FormData(form);
        const submitBtn = form.querySelector('button[type="submit"]');
        const originalText = submitBtn.innerHTML;

        // Validate all fields
        let isValid = true;
        const inputs = form.querySelectorAll('input, textarea');
        inputs.forEach(input => {
            if (!this.validateField(input)) {
                isValid = false;
            }
        });

        if (!isValid) {
            this.showNotification('Please fix the errors in the form', 'error');
            return;
        }

        // Show loading state
        submitBtn.innerHTML = '<div class="loading"></div> Sending...';
        submitBtn.disabled = true;

        try {
            // Simulate API call
            await this.simulateAPICall(formData);
            
            // Show success message
            this.showNotification('Thank you! Your message has been sent successfully. I\'ll get back to you within 24 hours.', 'success');
            
            // Reset form
            form.reset();
            
        } catch (error) {
            this.showNotification('Sorry, there was an error sending your message. Please try again.', 'error');
        } finally {
            // Restore button
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
        }
    }

    simulateAPICall(formData) {
        return new Promise((resolve) => {
            setTimeout(() => {
                // In a real application, you would send the data to your server here
                console.log('Form data:', {
                    name: formData.get('name'),
                    email: formData.get('email'),
                    subject: formData.get('subject'),
                    message: formData.get('message')
                });
                resolve();
            }, 2000);
        });
    }

    // Project Structure Setup
    setupProjectStructure() {
        // Tab functionality for code preview
        const tabButtons = document.querySelectorAll('.tab-button');
        const codePreviews = document.querySelectorAll('.code-preview');

        tabButtons.forEach(button => {
            button.addEventListener('click', () => {
                const tabName = button.getAttribute('data-tab');
                
                // Remove active class from all buttons and previews
                tabButtons.forEach(btn => btn.classList.remove('active'));
                codePreviews.forEach(preview => preview.classList.remove('active'));
                
                // Add active class to clicked button and corresponding preview
                button.classList.add('active');
                const targetPreview = document.getElementById(`${tabName}-tab`);
                if (targetPreview) {
                    targetPreview.classList.add('active');
                }
            });
        });

        // File tree interaction
        const fileItems = document.querySelectorAll('.file-list li');
        fileItems.forEach(item => {
            item.addEventListener('click', () => {
                // Remove active class from all items
                fileItems.forEach(i => i.classList.remove('active'));
                // Add active class to clicked item
                item.classList.add('active');
                
                // You could add functionality to show file content here
                const fileName = item.querySelector('i').nextSibling.textContent.trim();
                this.showNotification(`Selected: ${fileName}`, 'info');
            });
        });
    }

    // Social Links
    setupSocialLinks() {
        const socialLinks = document.querySelectorAll('.social-link');
        socialLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                if (!link.getAttribute('href') || link.getAttribute('href') === '#') {
                    e.preventDefault();
                    this.showNotification('Please update the social media links with your actual profiles', 'info');
                }
            });
        });
    }

    showNotification(message, type = 'info') {
        // Remove existing notifications
        const existingNotification = document.querySelector('.notification');
        if (existingNotification) {
            existingNotification.remove();
        }

        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        
        // Style the notification
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 20px;
            border-radius: 10px;
            color: white;
            font-weight: 600;
            z-index: 10000;
            animation: slideIn 0.3s ease-out;
            max-width: 400px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        `;

        if (type === 'success') {
            notification.style.background = 'var(--success)';
        } else if (type === 'error') {
            notification.style.background = '#dc3545';
        } else {
            notification.style.background = 'var(--primary)';
        }

        document.body.appendChild(notification);

        // Remove notification after 5 seconds
        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease-in';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }, 5000);
    }
}

// Add CSS for notifications and animations
const notificationStyles = `
@keyframes slideIn {
    from { transform: translateX(100%); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
}

@keyframes slideOut {
    from { transform: translateX(0); opacity: 1; }
    to { transform: translateX(100%); opacity: 0; }
}

.field-error {
    color: #dc3545;
    font-size: 0.875rem;
    margin-top: 5px;
}

.file-list li.active {
    background: rgba(67, 97, 238, 0.2);
    border-left: 3px solid var(--primary);
}

@keyframes typewriter {
    from { width: 0; }
    to { width: 100%; }
}

.typewriter {
    overflow: hidden;
    border-right: 3px solid var(--primary);
    white-space: nowrap;
    margin: 0 auto;
    animation: typewriter 3s steps(40, end);
}
`;

// Inject styles
const styleSheet = document.createElement('style');
styleSheet.textContent = notificationStyles;
document.head.appendChild(styleSheet);

// Global function for navigation
function showSection(sectionId) {
    portfolio.showSection(sectionId);
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Initialize portfolio when DOM is loaded
let portfolio;
document.addEventListener('DOMContentLoaded', () => {
    portfolio = new Portfolio();
    
    // Add interactive effects
    this.addInteractiveEffects();
});

// Interactive effects
function addInteractiveEffects() {
    // Add hover effects to service cards
    const serviceCards = document.querySelectorAll('.service-card');
    serviceCards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            card.style.transform = 'translateY(-10px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'translateY(0) scale(1)';
        });
    });

    // Add typing effect to hero text
    const heroText = document.querySelector('.hero h1');
    if (heroText) {
        const text = heroText.textContent;
        heroText.textContent = '';
        heroText.style.borderRight = '3px solid var(--primary)';
        
        let i = 0;
        function typeWriter() {
            if (i < text.length) {
                heroText.textContent += text.charAt(i);
                i++;
                setTimeout(typeWriter, 50);
            } else {
                heroText.style.borderRight = 'none';
            }
        }
        
        // Start typing after a short delay
        setTimeout(typeWriter, 500);
    }

    // Add scroll animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Observe elements for animation
    document.querySelectorAll('.service-card, .skill, .contact-item').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
}