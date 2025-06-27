from flask import request
from flask_restx import Namespace, Resource, fields
from werkzeug.exceptions import NotFound

from app.services import (
    get_all_books,
    get_book_by_id,
    add_book,
    update_book,
    delete_book
)

book_ns = Namespace('books', description='Book operations')

book_model = book_ns.model('Book', {
    'id': fields.Integer(readOnly=True),
    'title': fields.String(required=True),
    'author': fields.String(required=True),
    'price': fields.Float(required=True)
})

# Helper to serialize book objects
def serialize_book(book):
    return {
        'id': book.id,
        'title': book.title,
        'author': book.author,
        'price': book.price
    }

# Helper to extract only specified fields from book
def filter_fields(book, fields_list):
    return {field: getattr(book, field, None) for field in fields_list}


@book_ns.route('/')
class BookList(Resource):
    @book_ns.marshal_list_with(book_model)
    def get(self):
        """Get all books, with optional X-Fields header"""
        books = get_all_books() or []
        x_fields = request.headers.get('X-Fields')

        if x_fields:
            fields_list = x_fields.split(',')
            return [filter_fields(book, fields_list) for book in books]

        return [serialize_book(book) for book in books]

    @book_ns.expect(book_model, validate=True)
    @book_ns.marshal_with(book_model, code=201)
    def post(self):
        """Add a new book"""
        data = request.get_json()

        for field in ['title', 'author']:
            if not data.get(field) or str(data.get(field)).strip() == '':
                book_ns.abort(400, f"{field.capitalize()} cannot be empty")

        try:
            data['price'] = float(data['price'])
        except (ValueError, TypeError):
            book_ns.abort(400, "Price must be a valid number")

        book = add_book(data)
        return serialize_book(book), 201


@book_ns.route('/<int:id>')
@book_ns.param('id', 'The Book ID')
class BookByID(Resource):
    def get(self, id):
        """Get book by ID, with optional X-Fields header"""
        try:
            book = get_book_by_id(id)
        except NotFound:
            book_ns.abort(404, "Book not found")

        x_fields = request.headers.get('X-Fields')
        if x_fields:
            fields_list = x_fields.split(',')
            return filter_fields(book, fields_list)

        return serialize_book(book)

    def delete(self, id):
        """Delete a book"""
        try:
            book = get_book_by_id(id)
        except NotFound:
            book_ns.abort(404, "Book not found")

        delete_book(book)
        return {"message": "Book deleted"}, 200

    @book_ns.expect(book_model, validate=True)
    @book_ns.marshal_with(book_model)
    def put(self, id):
        """Update a book"""
        try:
            book = get_book_by_id(id)
        except NotFound:
            book_ns.abort(404, "Book not found")

        data = request.get_json()

        for field in ['title', 'author']:
            if not data.get(field) or str(data.get(field)).strip() == '':
                book_ns.abort(400, f"{field.capitalize()} cannot be empty")

        try:
            data['price'] = float(data['price'])
        except (ValueError, TypeError):
            book_ns.abort(400, "Price must be a valid number")

        result, updated_book = update_book(book, data)
        if result == "duplicate_id":
            return {"error": "Duplicate ID"}, 409

        return serialize_book(updated_book), 200
