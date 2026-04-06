from flask import Flask
from app.database import db

def create_app():
    # Initialize the core Flask application
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    
    # Configure SQLite database (Beginner friendly: stored locally as app.db)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize the database with the app
    db.init_app(app)
    
    # Import and register routing logic
    from app.routes import main
    app.register_blueprint(main)
    
    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()
        
    return app
