from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, models
from datetime import date

router = APIRouter(prefix="/authors", tags=["Authors"])

@router.get("/", response_model=list[schemas.AuthorResponse])
def get_authors(db: Session = Depends(get_db)):
    return db.query(models.Author).all()


@router.post("/", response_model=schemas.AuthorResponse)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):

    if author.birthdate and author.birthdate > date.today():
        raise HTTPException(status_code=400, detail="Дата народження не може бути в майбутньому!")
    
    db_author = models.Author(name=author.name, birthdate=author.birthdate)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


@router.get("/{author_id}", response_model=schemas.AuthorResponse)
def get_author(author_id: int, db: Session = Depends(get_db)):
    author = db.query(models.Author).filter(models.Author.id == author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Автор не знайдений")
    return author


@router.delete("/{author_id}")
def delete_author(author_id: int, db: Session = Depends(get_db)):
    author = db.query(models.Author).filter(models.Author.id == author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Автор не знайдений")
    db.delete(author)
    db.commit()
    return {"message": "Автор успішно видалений"}

@router.get("/{author_id}/books", response_model=list[schemas.BookResponse])
def get_books_by_author(author_id: int, db: Session = Depends(get_db)):
    author = db.query(models.Author).filter(models.Author.id == author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Автор не знайдений")
    
    books = db.query(models.Book).filter(models.Book.author_id == author_id).all()

    return [
        schemas.BookResponse(
            id=book.id,
            title=book.title,
            isbn=book.isbn,
            published_year=book.published_year,
            author_name=book.author.name,
            genre_name=book.genre.name,
            publisher_name=book.publisher.name
        ) for book in books
    ]