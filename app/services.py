from .models import Book
from . import db

def get_all_books():
    return Book.query.all()

def get_book_by_id(book_id):
    book = db.session.get(Book, book_id)  # ✅ SQLAlchemy 2.0 syntax
    if not book:
        raise Exception("Book not found")
    return book

def add_book(data):
    book = Book(
        id=data.get('id'),
        title=data['title'],
        author=data['author'],
        price=data['price']
    )
    db.session.add(book)
    db.session.commit()
    return book

def update_book(book, data):
    # If new ID is provided and different from current
    if 'id' in data and data['id'] != book.id:
        if db.session.get(Book, data['id']):
            return "duplicate_id", None
        book.id = data['id']

    book.title = data['title']
    book.author = data['author']
    book.price = data['price']
    db.session.commit()
    return "success", book

def delete_book(book):
    db.session.delete(book)
    db.session.commit()
