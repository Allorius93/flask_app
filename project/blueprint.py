from flask import Blueprint

tables_blueprint = Blueprint('tables', __name__)

from datetime import datetime
from flask import jsonify, abort, request
from project.models import *
from project import db
from project import route_config
from project.helper import count_rating


def parse_book(book):
    dict_book = {"id": book.id, 
                 "title": book.title, 
                 "publish_date": book.publish_date,
                 "avg_rating": book.avg_rating,
                 "num_rating": book.num_rating,
                 "authors":[{"name": author.name, "country": author.country} 
                            for author in book.author_ids]}
    return dict_book

@tables_blueprint.route('/books/api/v1.0/books', methods=['GET'])
def get_books():
    '''This function is for getting full book list'''
    page = request.args.get('page', 1, type=int)
    books = Book.query.paginate(page, route_config.ITEMS_PER_PAGE, False).items
    answer = {'books': [parse_book(book) for book in books]}
    return jsonify(answer)

@tables_blueprint.route('/books/api/v1.0/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get(book_id)
    if book is None:
        abort(404, description='Book is not in database')
    return jsonify(parse_book(book))

def get_authors_by_id(id_list):
    author_list = []
    for single_id in id_list:
        single_author = Author.query.get(single_id)
        author_list.append(single_author)
    if not author_list or None in author_list:
        raise Exception('author is is not found in the database')
    return author_list


# example request: curl -i -H "Content-Type: application/json" -X POST -d '{"title":"Bad omens", "publish_date": "2018-11-04", "author_ids": [1,5]}' http://127.0.0.1:5000/books/api/v1.0/books
@tables_blueprint.route('/books/api/v1.0/books', methods=['POST'])
def create_book():
    parsed_json = request.json
    # Check necessary fields
    if (not parsed_json or 'title' not in parsed_json
       or 'publish_date' not in parsed_json or 'author_ids' not in parsed_json):
        abort(400, description="Parse error")
    try: 
        author_list = get_authors_by_id(parsed_json['author_ids'])
        new_book = Book(title=parsed_json['title'], publish_date=datetime.strptime(parsed_json['publish_date'], '%Y-%m-%d'),
                        author_ids=author_list)
        db.session.add(new_book)
        db.session.commit()
    except Exception as ex:
        abort(400, description=str(ex))
    else: 
        return "Success", 201


@tables_blueprint.route("/books/api/v1.0/books/<int:book_id>", methods=["PUT"])
def put_rating(book_id):
    parsed_json = request.json
    if (not parsed_json or 'new_rating' not in parsed_json):
        abort(400, "Parse error")
    new_rating = parsed_json['new_rating']
    if new_rating < 1 or new_rating > 5:
        abort(400, "Rating should be between 1 and 5")
    try:
        book_item = Book.query.get(book_id)
        if book_item is None:
            abort(400, description="Book with %i id not found" % (book_id))
        new_num, new_avg = count_rating(book_item.num_rating, 
                                        book_item.avg_rating, new_rating)
        book_item.num_rating = new_num
        book_item.avg_rating = new_avg
        db.session.commit()
    except Exception as ex:
        return "Failed with an exception %s" % str(ex), 400
    return "Success", 201


# example requests.delete('http://127.0.0.1:5000/books/api/v1.0/books/6')
@tables_blueprint.route("/books/api/v1.0/<string:collection>/<int:item_id>", methods=["DELETE"])
def delete_item(collection, item_id):
    if collection == "authors":
        item = Author.query.get(item_id)
    elif collection == "books":
        item = Book.query.get(item_id)
    else:
        abort(400, description="Wrong resource, can only be books or authors")
    if item is None:
        abort(400, description="%s with %i id not found" % (collection, item_id))
    else:
        db.session.delete(item)
        db.session.commit()
        return "deleted succesfully", 204

def parse_author(author):
    dict_author = {"id": author.id,
                   "name": author.name,
                   "date_of_birth": author.date_of_birth,
                   "country": author.country} 
    return dict_author

def get_author_top(author):
    top_books = db.session.query(Book).select_from(Author).\
                join(Author.books).\
                filter(Author.id == author.id).order_by(Book.avg_rating.desc()).\
                limit(5)
    author_top = [{"title": top_book.title,
                   "rating": top_book.avg_rating}
                  for top_book in top_books]
    return author_top

@tables_blueprint.route('/books/api/v1.0/authors', methods=['GET'])
def get_authors():
    '''This function is for getting full author list'''
    page = request.args.get('page', 1, type=int)
    authors = Author.query.paginate(page, route_config.ITEMS_PER_PAGE, False).items
    answer = {'Authors': [parse_author(author) for author in authors]}
    return jsonify(answer)

@tables_blueprint.route('/books/api/v1.0/authors/<int:author_id>', methods=['GET'])
def get_author(author_id):
    author = Author.query.get(author_id)
    if author is None:
        abort(404, description='Author is not in database')
    result = parse_author(author)
    author_top = get_author_top(author)
    result['books'] = author_top
    return jsonify(result)


# example requests.post("http://127.0.0.1:5000/books/api/v1.0/authors", json={"name":"Patrick Rothfuss", "date_of_birth": "1967-03-12", "country": 'USA'})
# example request: curl -i -H "Content-Type: application/json" -X POST -d '{"name":"Patrick Rothfuss", "date_of_birth": "1967-03-12", "country": 'USA'}' http://127.0.0.1:5000/books/api/v1.0/authors
@tables_blueprint.route('/books/api/v1.0/authors', methods=['POST'])
def create_author():
    parsed_json = request.json
    if (not parsed_json or 'name' not in parsed_json
       or 'date_of_birth' not in parsed_json or 'country' not in parsed_json):
        abort(400, print("Parse error"))
    # Check necessary fields
    try: 
        new_author = Author(name=parsed_json['name'], date_of_birth=datetime.strptime(parsed_json['date_of_birth'], '%Y-%m-%d'),
                        country=parsed_json['country'])
        db.session.add(new_author)
        db.session.commit()
    except Exception as ex:
        abort(400, description=str(ex))
    else: 
        return "Success", 201
