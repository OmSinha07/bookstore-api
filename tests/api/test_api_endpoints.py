import pytest
from unittest.mock import patch
from app import create_app, db

@pytest.fixture(scope="module")
def client():
    app = create_app(testing=True)
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.session.remove()

# -------------------------
# ✅ BASIC CRUD WORKFLOW
# -------------------------

book_id = None  # Global to share book ID between tests

def test_create_book(client):
    global book_id
    response = client.post("/books", json={
        "title": "API Book",
        "author": "Author A",
        "price": 199.99
    })
    assert response.status_code == 201
    assert response.json["message"] == "Book added"
    book_id = response.json["id"]

def test_get_all_books(client):
    global book_id
    response = client.get("/books")
    assert response.status_code == 200
    assert isinstance(response.json, list)
    assert any(book["id"] == book_id for book in response.json)

def test_get_book_by_id(client):
    global book_id
    response = client.get(f"/books/{book_id}")
    assert response.status_code == 200
    assert response.json["title"] == "API Book"

def test_update_book(client):
    global book_id
    response = client.put(f"/books/{book_id}", json={
        "id": book_id,
        "title": "Updated Book",
        "author": "Author Updated",
        "price": 299.99
    })
    assert response.status_code == 200
    assert response.json["book"]["title"] == "Updated Book"

def test_delete_book(client):
    global book_id
    response = client.delete(f"/books/{book_id}")
    assert response.status_code == 200
    assert response.json["message"] == "Book deleted"

# -------------------------
# ✅ EDGE CASES
# -------------------------

def test_get_invalid_book(client):
    response = client.get("/books/999999")
    assert response.status_code == 404
    assert response.json["error"] == "Book not found"

def test_update_book_not_found(client):
    response = client.put("/books/999999", json={
        "id": 999999,
        "title": "Ghost Book",
        "author": "Nobody",
        "price": 10.99
    })
    assert response.status_code == 404
    assert response.json["error"] == "Book not found"

# -------------------------
# ✅ VALIDATION & BAD INPUTS
# -------------------------

def test_create_book_success(client):
    response = client.post("/books", json={
        "title": "Test Driven Book",
        "author": "Author One",
        "price": 149.99
    })
    assert response.status_code == 201
    assert response.json["message"] == "Book added"
    assert "id" in response.json

def test_create_book_empty_json(client):
    response = client.post('/books', json={})
    assert response.status_code == 400
    assert "Missing required fields" in response.json['error']

def test_create_book_missing_title(client):
    response = client.post('/books', json={"author": "X", "price": 123})
    assert response.status_code == 400
    assert "Missing required fields" in response.json['error']

def test_create_book_missing_author(client):
    response = client.post('/books', json={"title": "Test", "price": 123})
    assert response.status_code == 400
    assert "Missing required fields" in response.json['error']

def test_create_book_missing_price(client):
    response = client.post('/books', json={"title": "Test", "author": "X"})
    assert response.status_code == 400
    assert "Missing required fields" in response.json['error']


def test_create_book_invalid_price_type(client):
    response = client.post('/books', json={"title": "A", "author": "B", "price": "free"})
    assert response.status_code == 400
    assert "error" in response.json

def test_create_book_non_json(client):
    response = client.post('/books', data="title=Raw&author=Bad", content_type='text/plain')
    assert response.status_code == 415  # Correct status for unsupported media type




