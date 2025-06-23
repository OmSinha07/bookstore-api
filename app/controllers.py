from flask import Blueprint, request, jsonify, render_template
from .services import get_all_books, get_book_by_id, add_book, update_book, delete_book
from .models import Book
from app import db

# Blueprint setup
book_bp = Blueprint('book', __name__)

# Home route (UI page)
@book_bp.route('/')
def home():
    return render_template("index.html")

# GET all books
@book_bp.route('/books', methods=['GET'])
def get_books():
    books = get_all_books()
    return jsonify([
        {
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "price": book.price
        } for book in books
    ])

# GET book by ID
@book_bp.route('/books/<int:id>', methods=['GET'])
def get_book(id):
    try:
        book = get_book_by_id(id)
        return jsonify({
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "price": book.price
        }), 200
    except Exception:
        return jsonify({"error": "Book not found"}), 404

# POST create new book
@book_bp.route('/books', methods=['POST'])
def create_book():
    data = request.get_json()
    if not data or not all(k in data for k in ['title', 'author', 'price']):
        return jsonify({"error": "Missing required fields"}), 400
    try:
        book = add_book(data)
        return jsonify({"message": "Book added", "id": book.id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# PUT update book
@book_bp.route('/books/<int:id>', methods=['PUT'])
def edit_book(id):
    try:
        book = get_book_by_id(id)
    except:
        return jsonify({"error": "Book not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing data"}), 400

    result, updated_book = update_book(book, data)
    if result == "duplicate_id":
        return jsonify({"error": "A book with this new ID already exists."}), 409

    return jsonify({
        "message": "Book updated",
        "book": {
            "id": updated_book.id,
            "title": updated_book.title,
            "author": updated_book.author,
            "price": updated_book.price
        }
    }), 200

# DELETE book
@book_bp.route('/books/<int:id>', methods=['DELETE'])
def remove_book(id):
    try:
        book = get_book_by_id(id)
        delete_book(book)
        return jsonify({"message": "Book deleted"}), 200
    except Exception:
        return jsonify({"error": "Book not found"}), 404

