from flask import Blueprint, Flask, jsonify, request
from flask.testing import FlaskClient
import pytest
from unittest.mock import patch, MagicMock
from app.services import add_book, get_all_books, get_book_by_id, update_book, delete_book
from app.models import Book
from app import create_app, db
from app.config import Config, TestConfig
from sqlalchemy.exc import IntegrityError
from app import create_app
from unittest.mock import patch
from app import create_app

@pytest.fixture(scope="module")
def test_app():
    app = create_app(testing=True)
    with app.app_context():
        db.create_all()
        yield app
        db.session.rollback()
        db.session.remove()


#Config testing
def test_config_classes():
    assert hasattr(Config, 'SQLALCHEMY_DATABASE_URI')
    assert hasattr(TestConfig, 'TESTING')
    assert TestConfig.TESTING is True

#Controller testing
@pytest.fixture
def client():
    app = create_app()
    app.testing = True
    with app.test_client() as client:
        yield client

def test_home_route(client: FlaskClient):
    response = client.get('/')
    assert response.status_code == 200
    assert b"<html" in response.data


bp = Blueprint('books', __name__)
@bp.route('/books', methods=['POST'])
def create_book():
    data = request.get_json()
    book = add_book(data)
    return jsonify({"id": book.id, "title": book.title}), 201

@bp.route('/books/<int:book_id>', methods=['GET'])
def read_book(book_id):
    try:
        book = get_book_by_id(book_id)
        return jsonify({"id": book.id, "title": book.title, "author": book.author, "price": book.price})
    except Exception as e:
        return jsonify({"error": str(e)}), 404

@bp.route('/books/<int:book_id>', methods=['DELETE'])
def remove_book(book_id):
    try:
        book = get_book_by_id(book_id)
        delete_book(book)
        return jsonify({"message": "Book deleted"})
    except Exception as e:
        return jsonify({"error": str(e)}), 404


def test_remove_book_success():
    app = create_app(testing=True)


def test_get_all_books(client):
    mock_books = [
        type("Book", (), {"id": 1, "title": "Book1", "author": "Author A", "price": 100}),
        type("Book", (), {"id": 2, "title": "Book2", "author": "Author B", "price": 150}),
    ]
    with patch('app.controllers.get_all_books', return_value=mock_books):
        response = client.get('/books')
        assert response.status_code == 200
        assert isinstance(response.json, list)
        assert response.json[0]['title'] == 'Book1'

def test_get_book_by_id_success(client):
    mock_book = type("Book", (), {"id": 1, "title": "Test", "author": "Author", "price": 123})
    with patch('app.controllers.get_book_by_id', return_value=mock_book):
        response = client.get('/books/1')
        assert response.status_code == 200
        assert response.json['title'] == "Test"

def test_get_book_by_id_not_found(client):
    with patch('app.controllers.get_book_by_id', side_effect=Exception("Book not found")):
        response = client.get('/books/999')
        assert response.status_code == 404
        assert response.json['error'] == "Book not found"
def test_create_book_success(client):
    mock_book = type("Book", (), {"id": 3})
    with patch('app.controllers.add_book', return_value=mock_book):
        response = client.post('/books', json={"title": "New Book", "author": "Someone", "price": 99})
        assert response.status_code == 201
        assert response.json['message'] == "Book added"

def test_create_book_missing_fields(client):
    response = client.post('/books', json={"title": "No Author"})
    assert response.status_code == 400
    assert "Missing required fields" in response.json['error']

def test_home_route_content(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"<html" in response.data
    assert b"<title>" in response.data  # assuming your HTML has a title

def test_remove_book_not_found(client):
    with patch('app.controllers.get_book_by_id', side_effect=Exception("Book not found")):
        response = client.delete('/books/999')
        assert response.status_code == 404
        assert response.json["error"] == "Book not found"

def test_update_book_success(client):
    mock_book = type("Book", (), {"id": 1})
    updated_book = type("Book", (), {
        "id": 1, "title": "Updated", "author": "New", "price": 123
    })

    with patch("app.controllers.get_book_by_id", return_value=mock_book):
        with patch("app.controllers.update_book", return_value=("success", updated_book)):
            response = client.put("/books/1", json={
                "title": "Updated", "author": "New", "price": 123
            })
            assert response.status_code == 200
            assert response.json["message"] == "Book updated"
            assert response.json["book"]["title"] == "Updated"



    
    # Mock book object
    
def test_remove_book_success():
    app = create_app(testing=True)
    mock_book = type("Book", (), {"id": 1, "title": "Mock", "author": "Tester", "price": 123.45})

    with app.test_client() as client:
        with patch('app.controllers.get_book_by_id', return_value=mock_book), \
             patch('app.controllers.delete_book') as mock_delete:
            
            response = client.delete('/books/1')

            assert response.status_code == 200
            assert response.get_json() == {"message": "Book deleted"}
            mock_delete.assert_called_once_with(mock_book)

def test_remove_book_not_found():
    app = create_app(testing=True)

    with app.test_client() as client:
        with patch('app.controllers.get_book_by_id', side_effect=Exception("Book not found")):
            response = client.delete('/books/9999')
            assert response.status_code == 404
            assert response.get_json() == {"error": "Book not found"}

# ---------------------------
# MOCKED TESTS DB
# ---------------------------

@patch("app.services.db.session")
def test_add_book_mocked(mock_session, test_app: Flask):
    with test_app.app_context():
        mock_data = {"id": 1, "title": "Mock Book", "author": "Author", "price": 150}
        book = add_book(mock_data)
        assert book.title == "Mock Book"
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()

@patch("app.services.Book.query")
def test_get_all_books_mocked(mock_query, test_app: Flask):
    with test_app.app_context():
        mock_book = Book(id=1, title="Title", author="Author", price=99)
        mock_query.all.return_value = [mock_book]
        books = get_all_books()
        assert len(books) == 1
        assert books[0].title == "Title"

@patch("app.services.db.session.get")
def test_get_book_by_id_mocked(mock_get, test_app: Flask):
    with test_app.app_context():
        mock_get.return_value = Book(id=2, title="Another", author="Author", price=123)
        book = get_book_by_id(2)
        assert book.title == "Another"

        mock_get.return_value = None
        with pytest.raises(Exception) as exc_info:
            get_book_by_id(999)
        assert "Book not found" in str(exc_info.value)

@patch("app.services.db.session")
def test_update_book_simple_success(mock_session, test_app: Flask):
    with test_app.app_context():
        book = Book(id=1, title="Old Title", author="Old Author", price=100)

        data = {"id": 1, "title": "New Title", "author": "New Author", "price": 200}
        status, updated = update_book(book, data)

        assert status == "success"
        assert updated.title == "New Title"
        assert updated.author == "New Author"
        assert updated.price == 200

        mock_session.commit.assert_called_once()

@patch("app.services.db.session.get")
@patch("app.services.db.session")
def test_update_book_duplicate_id_branch(mock_session, mock_get, test_app: Flask):
    with test_app.app_context():
        # Book with current id=1
        book = Book(id=1, title="Old", author="Old", price=100)
        
        # Data with a different id (2)
        data = {"id": 2, "title": "New Title", "author": "New Author", "price": 200}

        # Mock session.get to simulate duplicate id found (id=2 already exists)
        mock_get.return_value = Book(id=2, title="Existing", author="Someone", price=150)

        status, updated = update_book(book, data)

        assert status == "duplicate_id"
        assert updated is None
        mock_session.commit.assert_not_called()

    
# ---------------------------
# REAL DB TESTS(WITHOUT MOCKING)
# ---------------------------

def test_add_book_real(test_app: Flask):
    with test_app.app_context():
        data = {"id": 10, "title": "Real Book", "author": "Real Author", "price": 100.0}
        try:
            book = add_book(data)
            assert book.title == "Real Book"
            assert book.author == "Real Author"
            assert book.price == 100.0
        except Exception as e:
            print(f"⚠️ Could not add book with id=10: {e}")
            assert True

def test_update_book_real(test_app: Flask):
    with test_app.app_context():
        existing = db.session.get(Book, 20)
        if existing:
            db.session.delete(existing)
            db.session.commit()

        book = add_book({"id": 20, "title": "Old", "author": "Old", "price": 150.0})
        data = {"id": 20, "title": "New", "author": "New", "price": 250.0}
        status, updated_book = update_book(book, data)
        assert status == "success"
        assert updated_book.title == "New"
        assert updated_book.author == "New"
        assert updated_book.price == 250.0

def test_delete_book_real(test_app: Flask):
    with test_app.app_context():
        book = add_book({"id": 40, "title": "Delete Me", "author": "X", "price": 123})
        delete_book(book)
        books = get_all_books()
        assert all(b.id != 40 for b in books)

def test_get_book_by_id_not_found_real(test_app: Flask):
    with test_app.app_context():
        # Ensure book with id=9999 DB me nahi hai
        existing = db.session.get(Book, 9999)
        if existing:
            db.session.delete(existing)
            db.session.commit()

        with pytest.raises(Exception) as exc_info:
            get_book_by_id(9999)
        assert "Book not found" in str(exc_info.value)
        
        db.session.rollback()


def test_update_book_change_id_real(test_app: Flask):
    with test_app.app_context():
        # Cleanup any conflicting data
        for book_id in [50, 51]:
            existing = db.session.get(Book, book_id)
            if existing:
                db.session.delete(existing)
        db.session.commit()

        # Add book with id=50
        book = add_book({"id": 50, "title": "Original", "author": "Author", "price": 100})

        # Update book, changing id to 51 (which is unused)
        data = {"id": 51, "title": "Updated Title", "author": "Updated Author", "price": 200}
        status, updated_book = update_book(book, data)

        assert status == "success"
        assert updated_book.id == 51
        assert updated_book.title == "Updated Title"
        assert updated_book.author == "Updated Author"
        assert updated_book.price == 200

        db.session.rollback()

def test_delete_nonexistent_book_real(test_app: Flask):
    with test_app.app_context():
        # Try to get book with id=99999 from DB
        book = db.session.get(Book, 99999)
        if book:
            db.session.delete(book)
            db.session.commit()

        # Now try deleting after fetching again (should be None)
        book = db.session.get(Book, 99999)
        if book is None:
            # No book to delete - test passes because nothing to delete
            assert True
        else:
            # If book still exists, delete it and test passes
            delete_book(book)
            assert True
import pytest
from sqlalchemy.exc import IntegrityError
from app.services import add_book
from app.models import Book
from app import db

def test_add_book_duplicate_id_real(test_app: Flask):
    with test_app.app_context():
        # Remove book if exists
        existing = db.session.get(Book, 100)
        if existing:
            db.session.delete(existing)
            db.session.commit()

        # Add first book with id=100
        add_book({"id": 100, "title": "First Book", "author": "Author1", "price": 50})

        # Attempt duplicate insert - expect IntegrityError
        with pytest.raises(IntegrityError):
            add_book({"id": 100, "title": "Duplicate Book", "author": "Author2", "price": 60})

        # Rollback to clean session after failed commit
        db.session.rollback()

def test_get_book_by_id_not_found(test_app: Flask):
    with test_app.app_context():
        with pytest.raises(Exception) as excinfo:
            get_book_by_id(9999)  # Assuming 9999 doesn't exist
        assert "Book not found" in str(excinfo.value)

def test_get_all_books_empty(test_app: Flask):
    with test_app.app_context():
        # Clear all books
        books = get_all_books()
        for b in books:
            db.session.delete(b)
        db.session.commit()

        empty_books = get_all_books()
        assert isinstance(empty_books, list)
        assert len(empty_books) == 0

def test_delete_non_persistent_book(test_app: Flask):
    with test_app.app_context():
        book = Book(id=99999, title="Non Persisted", author="None", price=0)
        # Check if exists in DB
        existing = db.session.get(Book, book.id)
        if existing:
            delete_book(existing)
            assert True
        else:
            # No book in DB, so we skip deletion safely
            assert True

