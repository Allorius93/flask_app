from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import database_exists, create_database, drop_database

db = SQLAlchemy()

def create_app(config_object=None):
    # Create flask application and register all its features 
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_object)
    db.init_app(app)
    register_blueprints(app)
    from project.models import Book, Author
    #run_database(app.config['SQLALCHEMY_DATABASE_URI'], app)
    return app

def register_blueprints(app):
    from project.blueprint import tables_blueprint
    from project.commands import command_blueprint
    app.register_blueprint(tables_blueprint)
    app.register_blueprint(command_blueprint)

def run_database(DB_URL, app):
    if not database_exists(DB_URL):
        print('Creating database.')
        create_database(DB_URL)
    with app.app_context():
        db.create_all()
