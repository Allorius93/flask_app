from datetime import datetime
import pytest
from project import create_app, db
from project.models import Author, Book
from sqlalchemy_utils import database_exists, create_database
from flask_cfg import TestingConfig

@pytest.fixture(scope='session')
def test_client(request):
    flask_app = create_app(TestingConfig)
    testing_client = flask_app.test_client()
    # Establish an application context before running the tests.
    ctx = flask_app.app_context()
    ctx.push()
    def teardown():
        ctx.pop()
    request.addfinalizer(teardown)
    return testing_client

@pytest.fixture(scope='session')
def init_database(request):
    DB_URL = TestingConfig.SQLALCHEMY_DATABASE_URI
    if not database_exists(DB_URL):
        print('Creating database.')
        create_database(DB_URL)
    db.create_all()
    # Fill database with data for testing
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
    book_3 = Book(title="Wind-up girl", publish_date=datetime.strptime('2009-07-12', '%Y-%m-%d'), author_ids=[author_6, author_7], avg_rating=5, num_rating = 10)
    book_4 = Book(title="Great omens", publish_date=datetime.strptime('2002-12-29', '%Y-%m-%d'), author_ids=[author_1, author_3], avg_rating=3, num_rating=10)
    book_5 = Book(title="Game of thrones", publish_date=datetime.strptime('2003-12-29', '%Y-%m-%d'), author_ids=[author_1, author_3, author_5], avg_rating=4, num_rating=10)
    book_6 = Book(title="Feast for crows", publish_date=datetime.strptime('2015-12-29', '%Y-%m-%d'), author_ids=[author_3], avg_rating=2, num_rating=10)
    book_7 = Book(title="Fever dreams", publish_date=datetime.strptime('2002-12-29', '%Y-%m-%d'), author_ids=[author_3], avg_rating=2, num_rating=10)
    book_8 = Book(title="Song of Lia", publish_date=datetime.strptime('2018-01-29', '%Y-%m-%d'), author_ids=[author_3], avg_rating=1, num_rating=10)
    book_9 = Book(title="Wind-up Girl 2", publish_date=datetime.strptime('2011-03-29', '%Y-%m-%d'), author_ids=[author_7, author_5], avg_rating=3.4, num_rating=10)
    book_10 = Book(title="Name of the wind", publish_date=datetime.strptime('2011-12-11', '%Y-%m-%d'), author_ids=[author_7, author_3], avg_rating=1.3, num_rating=10)
    book_11 = Book(title="Wise man fear", publish_date=datetime.strptime('2018-12-22', '%Y-%m-%d'), author_ids=[author_1, author_7], avg_rating=5, num_rating=10)
    book_12 = Book(title="Don Quihote", publish_date=datetime.strptime('1670-12-02', '%Y-%m-%d'), author_ids=[author_9], avg_rating=1, num_rating=9)
    book_13 = Book(title="Foundation and Empire", publish_date=datetime.strptime('2018-12-29', '%Y-%m-%d'), author_ids=[author_8], avg_rating=1, num_rating=9)

    db.session.add_all([author_1, author_2, author_3, author_4, author_5, author_6, author_7, author_8, author_9,
                        book_1, book_2, book_3, book_4, book_5, book_6, book_7, book_8, book_9,
                        book_10, book_11, book_12, book_13])
    db.session.commit()
    def teardown():
        db.drop_all()
    request.addfinalizer(teardown)
    return db

def test_get_books(test_client, init_database):
    response = test_client.get('/books/api/v1.0/books')
    assert response.status_code == 200

def test_get_book(test_client, init_database):
    response = test_client.get('/books/api/v1.0/books/1')
    assert response.status_code == 200
    assert response.get_json()['title'] == 'Good omens'

def test_post_book(test_client, init_database):
    new_book = {"title":"Bad omens", "publish_date": "2018-11-04", "author_ids": [1,5]}
    response = test_client.post('/books/api/v1.0/books', json=new_book)
    assert response.status_code == 201

def test_post_wrong_book(test_client, init_database):
    new_book = {"publish_date": "2018-11-04", "author_ids": [1,5]}
    response = test_client.post('/books/api/v1.0/books', json=new_book)
    assert response.status_code == 400

def test_delete_book(test_client, init_database):
    response = test_client.delete('/books/api/v1.0/books/14')
    assert response.status_code == 204

def test_put_rating(test_client, init_database):
    # Test putting rating and correct new rating
    response = test_client.put('/books/api/v1.0/books/12', json = {'new_rating': 5})
    assert response.status_code == 201
    book = test_client.get('/books/api/v1.0/books/12').get_json()
    assert book['avg_rating'] == 1.4
    assert book['num_rating'] == 10

def test_get_authors(test_client, init_database):
    response = test_client.get('/books/api/v1.0/authors')
    assert response.status_code == 200

def test_get_author(test_client, init_database):
    response = test_client.get('/books/api/v1.0/authors/3')
    assert response.status_code == 200
    assert response.get_json()['name'] == 'George Martin'
    # This part tests if author has correct top 5 books
    book_titles = [single_book['title'] for single_book in response.get_json()['books']]
    assert 'Game of thrones' in book_titles
    assert 'Storm of swords' in book_titles
    assert 'Name of the wind' not in book_titles

def test_get_wrong_author(test_client, init_database):
    response = test_client.get('/books/api/v1.0/authors/19999999')
    assert response.status_code == 404

def test_post_author(test_client, init_database):
    new_author = {"name":"Jhon Smith", "date_of_birth": "1911-03-12", "country": 'USA'}
    response = test_client.post('/books/api/v1.0/authors', json=new_author)
    assert response.status_code == 201

def test_post_wrong_author(test_client, init_database):
    new_author = {"date_of_birth": "1967-03-12", "country": 'USA'}
    response = test_client.post('/books/api/v1.0/authors', json=new_author)
    assert response.status_code == 400

def test_delete_author(test_client, init_database):
    response = test_client.delete('/books/api/v1.0/books/10')
    assert response.status_code == 204

def test_delete_wrong(test_client, init_database):
    response = test_client.delete('/books/api/v1.0/non_collection/10')
    assert response.status_code == 400

