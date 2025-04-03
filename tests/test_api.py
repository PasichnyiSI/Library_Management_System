from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal, get_db
from app.models import Base 
import pytest

@pytest.fixture
def db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.rollback()  
        db.close()  

@pytest.fixture
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass 

    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)

def test_create_book_invalid_isbn(client):
    response = client.post("/books/", json={"title": "Test", "isbn": "111", "published_year": "2000", 
                                            "author_name": "author_name", "genre_name": "genre_name", 
                                            "publisher_name": "publisher_name"})
    assert response.status_code == 422
    assert "isbn" in response.json()["detail"][0]["loc"]

def test_create_book_invalid_date(client):
    response = client.post("/books/", json={"title": "Test", "isbn": "9786178426927", "published_year": "2222", 
                                            "author_name": "author_name", "genre_name": "genre_name", 
                                            "publisher_name": "publisher_name"})
    assert response.status_code == 422
    assert "published_year" in response.json()["detail"][0]["loc"]

def test_create_author_invalid_name(client):
    response = client.post("/authors/", json={"name": "", "birthdate": "1900-01-01"})
    assert response.status_code == 422  
    assert "name" in response.json()["detail"][0]["loc"]

def test_create_author_invalid_birthdate(client):
    response = client.post("/authors/", json={"name": "John Doe", "birthdate": "01-01-1900"})
    assert response.status_code == 422  
    assert "birthdate" in response.json()["detail"][0]["loc"]
