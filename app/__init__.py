from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'main.login'

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'your_secret_key_here'

    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)

    # Import models (important for db.create_all)
    from .models import User, Task

    # Create database tables
    with app.app_context():
        db.create_all()

    # Register blueprints
    from .routes import main
    app.register_blueprint(main)
# Setup user loader
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    return app
