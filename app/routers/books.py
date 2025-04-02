from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ..database import get_db
import app.schemas as schemas
import app.models as models

router = APIRouter(prefix="/books", tags=["Books"])

@router.get("/", response_model=list[schemas.BookResponse])
def get_books(
    db: Session = Depends(get_db),
    limit: int = Query(10, ge=1, le=100, description="Кількість книг на сторінці"),
    offset: int = Query(0, ge=0, description="Зміщення для пагінації"),
    sort_by: str = Query("title", regex="^(title|author|published_year)$", description="Поле для сортування"),
    order: str = Query("asc", regex="^(asc|desc)$", description="Порядок сортування (asc/desc)")
):
    sort_field = {
        "title": models.Book.title,
        "author": models.Author.name,
        "published_year": models.Book.published_year
    }[sort_by]

    if order == "desc":
        sort_field = sort_field.desc()

    books = (
        db.query(models.Book)
        .join(models.Author)
        .order_by(sort_field)
        .offset(offset)
        .limit(limit)
        .all()
    )

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

@router.post("/", response_model=schemas.BookResponse)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    author = db.query(models.Author).filter(models.Author.name == book.author_name).first()
    if not author:
        author = models.Author(name=book.author_name)
        db.add(author)
        db.commit()
        db.refresh(author)

    genre = db.query(models.Genre).filter(models.Genre.name == book.genre_name).first()
    if not genre:
        genre = models.Genre(name=book.genre_name)
        db.add(genre)
        db.commit()
        db.refresh(genre)

    publisher = db.query(models.Publisher).filter(models.Publisher.name == book.publisher_name).first()
    if not publisher:
        publisher = models.Publisher(name=book.publisher_name)
        db.add(publisher)
        db.commit()
        db.refresh(publisher)

    db_book = models.Book(
        title=book.title,
        isbn=book.isbn,
        published_year=book.published_year,
        author_id=author.id,
        genre_id=genre.id,
        publisher_id=publisher.id
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return schemas.BookResponse(
        id=db_book.id,
        title=db_book.title,
        isbn=db_book.isbn,
        published_year=db_book.published_year,
        author_name=author.name,
        genre_name=genre.name,
        publisher_name=publisher.name
    )


@router.get("/{book_id}", response_model=schemas.BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Книга не знайдена")
    return schemas.BookResponse(
        id=book.id,
        title=book.title,
        isbn=book.isbn,
        published_year=book.published_year,
        author_name=book.author.name,
        genre_name=book.genre.name,
        publisher_name=book.publisher.name
    )


@router.delete("/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Книга не знайдена")
    db.delete(book)
    db.commit()
    return {"message": "Книга успішно видалена"}


@router.get("/books/{book_id}/history", response_model=list[schemas.BorrowingHistoryResponse])
def get_history_of_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Книга не знайдена")
    

    history = (
        db.query(models.BorrowingHistory, models.Borrower.name, models.Borrower.email)
        .join(models.Borrower, models.BorrowingHistory.borrower_id == models.Borrower.id)
        .filter(models.BorrowingHistory.book_id == book_id)
        .all()
    )
    
    
    return [
        schemas.BorrowingHistoryResponse(
            id=record.BorrowingHistory.id,
            book_id=record.BorrowingHistory.book_id,
            borrower_id=record.BorrowingHistory.borrower_id,
            borrower_name=record.name,
            borrower_email=record.email,  
            borrowed_at=record.BorrowingHistory.borrowed_at,
            returned_at=record.BorrowingHistory.returned_at
        )
        for record in history
    ]