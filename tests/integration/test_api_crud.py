# ✅ tests/integration/test_api_crud.py
import pytest
from app import create_app, db

@pytest.fixture(scope="module")
def test_client():
    app = create_app(testing=False)  # Blueprint already registered inside
    with app.test_client() as testing_client:
        with app.app_context():
            db.create_all()
        yield testing_client
        with app.app_context():
            db.session.remove()

# ---------------------------
# ✅ INTEGRATION TESTS
# ---------------------------

def test_create_book(test_client):
    response = test_client.post('/books', 
        json={"id": 101, "title": "Test Book", "author": "Author X", "price": 299.99})
    assert response.status_code == 201
    assert response.json["message"] == "Book added"

def test_get_all_books(test_client):
    response = test_client.get('/books')
    assert response.status_code == 200
    assert isinstance(response.json, list)
    assert any(book['id'] == 101 for book in response.json)

def test_get_book_by_id(test_client):
    response = test_client.get('/books/101')
    assert response.status_code == 200
    assert response.json["title"] == "Test Book"

def test_update_book(test_client):
    response = test_client.put('/books/101', 
        json={"id": 101, "title": "Updated Book", "author": "Updated Author", "price": 199.99})
    assert response.status_code == 200
    assert response.json["book"]["title"] == "Updated Book"

def test_delete_book(test_client):
    response = test_client.delete('/books/101')
    assert response.status_code == 200
    assert response.json["message"] == "Book deleted"

def test_book_not_found(test_client):
    response = test_client.get('/books/9999')
    assert response.status_code == 404
