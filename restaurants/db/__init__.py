from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()

def init_db(app):
    # Initialize the SQLAlchemy database object with the Flask app
    db.init_app(app)
    
    # Create a new application context (needed to access app-specific resources)
    with app.app_context():
        # Use SQLAlchemy's inspector to check existing database tables
        inspector = inspect(db.engine)
        existing_tables = inspector.get_table_names()

        # If there are no existing tables, create all tables defined in the models
        if not existing_tables:
            db.create_all()
    
    # Return the initialized database object
    return db

def init_ma(app):
    # Initialize the Marshmallow object with the Flask app
    ma.init_app(app)

    # Return the initialized Marshmallow object
    return ma