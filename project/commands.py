from flask import Blueprint

command_blueprint = Blueprint('command', __name__)

from datetime import datetime
from sqlalchemy_utils import database_exists, create_database, drop_database
from project.models import *
from project import db
from flask_cfg import Config as cfg

DB_URL = cfg.SQLALCHEMY_DATABASE_URI

def resetdb_func():
    """Destroys and creates the database + tables."""
    if database_exists(DB_URL):
        print('Deleting database.')
        drop_database(DB_URL)
    if not database_exists(DB_URL):
        print('Creating database.')
        create_database(DB_URL)

    print('Creating tables.')
    db.create_all()
    print('Done!')

@command_blueprint.cli.command('resetdb')
def resetdb_command():
    resetdb_func()

def drop_func():
    if database_exists(DB_URL):
        print('Deleting database.')
        drop_database(DB_URL)

@command_blueprint.cli.command('dropdb')
def dropdb_command():
    drop_func()

@command_blueprint.cli.command('filldb')
def fill_command():
    if not database_exists(DB_URL):
        raise Exception('Database does not exist. Create database with resetdb command')

    print('Filling tables.')
    author_1 = Author(name="Niel Gaiman", date_of_birth=datetime.strptime('1976-12-29', '%Y-%m-%d'), country="UK")
    author_2 = Author(name="Terry Pratchet", date_of_birth=datetime.strptime('1950-02-15', '%Y-%m-%d'), country="UK")
    author_3 = Author(name="George Martin", date_of_birth=datetime.strptime('1960-06-09', '%Y-%m-%d'), country="USA")
    author_4 = Author(name="Stephen King", date_of_birth=datetime.strptime('1970-07-21', '%Y-%m-%d'), country="USA")
    author_5 = Author(name="Niel Stephenson", date_of_birth=datetime.strptime('1974-05-29', '%Y-%m-%d'), country="USA")
    author_6 = Author(name="Paolo Bachigalupi", date_of_birth=datetime.strptime('1976-12-13', '%Y-%m-%d'), country="USA")
    author_7 = Author(name="Patrick Rothfuss", date_of_birth=datetime.strptime('1970-12-13', '%Y-%m-%d'), country="USA")
    author_8 = Author(name="Isaak Asimov", date_of_birth=datetime.strptime('1940-12-13', '%Y-%m-%d'), country="USA")
    author_9 = Author(name="Miguel de Servantes", date_of_birth=datetime.strptime('1630-02-13', '%Y-%m-%d'), country="Spain")

    book_1 = Book(title="Good omens", publish_date=datetime.strptime('2008-12-29', '%Y-%m-%d'), author_ids=[author_1, author_2], avg_rating=1, num_rating=10)
    book_2 = Book(title="Storm of swords", publish_date=datetime.strptime('2005-11-29', '%Y-%m-%d'), author_ids=[author_3], avg_rating=5, num_rating=10)
    book_3 = Book(title="Wind-up girl", publish_date=datetime.strptime('2009-07-12', '%Y-%m-%d'), author_ids=[author_6,author_7], avg_rating=5, num_rating = 10)
    book_4 = Book(title="Great omens", publish_date=datetime.strptime('2002-12-29', '%Y-%m-%d'), author_ids=[author_1, author_3], avg_rating=3, num_rating=10)
    book_5 = Book(title="Game of thrones", publish_date=datetime.strptime('2003-12-29', '%Y-%m-%d'), author_ids=[author_1, author_3, author_5], avg_rating=4, num_rating=10)
    book_6 = Book(title="Feast for crows", publish_date=datetime.strptime('2015-12-29', '%Y-%m-%d'), author_ids=[author_3], avg_rating=2, num_rating=10)
    book_7 = Book(title="Fever dreams", publish_date=datetime.strptime('2002-12-29', '%Y-%m-%d'), author_ids=[author_3], avg_rating=2, num_rating=10)
    book_8 = Book(title="Song of Lia", publish_date=datetime.strptime('2018-01-29', '%Y-%m-%d'), author_ids=[author_3], avg_rating=1, num_rating=10)
    book_9 = Book(title="Wind-up Girl 2", publish_date=datetime.strptime('2011-03-29', '%Y-%m-%d'), author_ids=[author_7, author_5], avg_rating=3.4, num_rating=10)
    book_10 = Book(title="Name of the wind", publish_date=datetime.strptime('2011-12-11', '%Y-%m-%d'), author_ids=[author_7, author_3], avg_rating=1.3, num_rating=10)
    book_11 = Book(title="Wise man fear", publish_date=datetime.strptime('2018-12-22', '%Y-%m-%d'), author_ids=[author_1, author_7], avg_rating=5, num_rating=10)
    book_12 = Book(title="Don Quihote", publish_date=datetime.strptime('1670-12-02', '%Y-%m-%d'), author_ids=[author_9], avg_rating=1, num_rating=10)
    book_13 = Book(title="Foundation and Empire", publish_date=datetime.strptime('2018-12-29', '%Y-%m-%d'), author_ids=[author_8], avg_rating=1, num_rating=10)

    db.session.add_all([author_1, author_2, author_3, author_4, author_5, author_6, author_7, author_8, author_9,
                        book_1, book_2, book_3, book_4, book_5, book_6, book_7, book_8, book_9,
                        book_10, book_11, book_12, book_13])
    db.session.commit()

    print('Done!')