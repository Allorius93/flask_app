from project import db


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
    def __repr__(self):
        return '<Author %r>' % self.name