This is a flask application with a basic 2-table database attached.   

### Database schema
Used tables described below with sqlalchemy syntax.

```python
book_authors = db.Table('book_authors',
    db.Column('author_id', db.Integer, db.ForeignKey('author.id'), primary_key=True, nullable=False),
    db.Column('book_id', db.Integer, db.ForeignKey('book.id'), primary_key=True, nullable=False)
)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(160), nullable=False)
    publish_date = db.Column(db.Date, nullable=False)
    avg_rating = db.Column(db.Float, nullable=False, default=0)
    num_rating = db.Column(db.Integer, nullable=False, default=0)
    author_ids = db.relationship('Author', secondary=book_authors, lazy='subquery',
        backref=db.backref('books', lazy=True))
    def __repr__(self):
        return '<Bookname %r>' % self.title

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), nullable=False)
    date_of_birth = db.Column(db.Date)
    country = db.Column(db.String(60))
``` 

We have many-to-many relationship between books and authors, so we need to create intermediary table, which will store connections. 


### On requirements

File requirements.txt describes python libraries needed to run application. If you are not using postgreSQL installing psycopg2 labrary should fail. In this case exclude it from requirements file. 

### Configuration

Application configuration stored in flask_cfg.py. It mainly describes database type and connection. Relevant parameters:

- BASE_TYPE - database type to connect to. By default postgresql+psycopg2
- POSTGRES_URL - host:port to connect to
- POSTGRES_USER - name of the database user with appropriate rights
- POSTGRES_PW - password to the POSTGRES_USER
- POSTGRES_DB - name of production database

### Run application

To launch application do the following from main application directory:

1. Register flask aplication

```bash
export FLASK_APP=main.py
```
Or on windows:
```bash
set FLASK_APP=main.py
```

2. Before running application it is neccessary to first create database. It is not created automatically. 

```bash
flask command resetdb
```

3. Then run the application. 

```bash
flask run
```

### Additional commands

If is also possible to drop database or fill it with dummy test data:

```bash
flask command dropdb
flask command filldb
```

### API

Application api is coded in project/blueprint.py. All commands below(described in python code):

```python
# Get requests
requests.get('localhost:5000/books/api/v1.0/books') # Gets books list. By default gets first 3 books. Number of books can be changed
# in route_config.py file with ITEMS_PER_PAGE variable
requests.get('localhost:5000/books/api/v1.0/books?page=2') # Get second list of book list. page can be any int
requests.get('localhost:5000/books/api/v1.0/authors?page=2') # Get author list. It's too support pagination
requests.get('localhost:5000/books/api/v1.0/books/<int:book_id>') # Get single book. Put any book id insted of <int:book_id>
requests.get('localhost:5000/books/api/v1.0/authors/<int:author_id>') # Get single author. Put any author id insted of <int:author_id>
# Put delete
requests.delete('localhost:5000/books/api/v1.0/books/<int:book_id>') # Delete single book. Put any book id insted of <int:book_id>
requests.delete('localhost:5000/books/api/v1.0/authors/<int:author_id>') # Delete single author. Put any author id insted of <int:author_id>
# Put requests
requests.put('localhost:5000/books/api/v1.0/books/12', json = {'new_rating': 5}) # Put new rating. Should be int between 1 and 5. Request json must contain new_rating field
# Post requests
requests.post("http://127.0.0.1:5000/books/api/v1.0/authors", json={"name":"Patrick Rothfuss", "date_of_birth": "1967-03-12", "country": 'USA'})
# Create new author in the database. Request json must contain name, date_of_birth and country fields
requests.post("http://127.0.0.1:5000/books/api/v1.0/books", json={"title":"Bad omens", "publish_date": "2018-11-04", "author_ids": [1,5]})
# Create new book in the database. Request json must contain title, publish_date and author_ids fields. author_ids must be int or list with existing author id. Otherwise app will return exception, but won't fail.
```

### Run test

Test should be run after registering application on environment variable. After this is done, to run test use following command in application directory:

```bash
python -m pytest -v
```