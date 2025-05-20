import os
from flask import Flask
from .models import db
from .routes import main  # Your blueprint


def create_app():
    # Create Flask app with specified static and template folder paths
    app = Flask(
        __name__,
        static_folder='static',
        template_folder='templates'
    )

    # Load configuration from environment or defaults
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///data.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'change-this-in-production')

    # Initialize extensions
    db.init_app(app)

    # Register blueprints
    app.register_blueprint(main)

    # Optional: add more setup hooks here (e.g., CLI, error handlers, etc.)
    return app
