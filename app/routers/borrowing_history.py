from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
import app.schemas as schemas
import app.models as models
from datetime import datetime, timezone, date

router = APIRouter(prefix="/borrowing_history", tags=["Borrowing History"])


@router.get("/", response_model=list[schemas.BorrowingHistoryResponse])
def get_borrowing_history(db: Session = Depends(get_db)):
    return db.query(models.BorrowingHistory).all()


@router.post("/", response_model=schemas.BorrowingHistoryResponse)
def create_borrowing_record(record: schemas.BorrowingHistoryCreate, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == record.book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Книга не знайдена")

    if not book.is_available:
        raise HTTPException(status_code=400, detail="Книга вже в оренді")
    
    db_record = models.BorrowingHistory(
        book_id=record.book_id,
        borrower_id=record.borrower_id,
        borrowed_at=datetime.now(timezone.utc),
        returned_at=None
    )
    db.add(db_record)
    book.is_available = False
    db.commit()
    db.refresh(db_record)
    return db_record


@router.get("/{record_id}", response_model=schemas.BorrowingHistoryResponse)
def get_borrowing_record(record_id: int, db: Session = Depends(get_db)):
    record = db.query(models.BorrowingHistory).filter(models.BorrowingHistory.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Запис не знайдено")
    return record


@router.delete("/{record_id}")
def delete_borrowing_record(record_id: int, db: Session = Depends(get_db)):
    record = db.query(models.BorrowingHistory).filter(models.BorrowingHistory.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Запис не знайдено")
    if record.returned_at is None:
        raise HTTPException(status_code=400, detail="Книгу ще не повернули!")

    db.delete(record)
    db.commit()
    return {"message": "Запис успішно видалено"}


@router.put("/{borrowing_id}/return", response_model=schemas.BorrowingHistoryResponse)
def return_borrowing_record(borrowing_id: int, db: Session = Depends(get_db)):
    borrowing = db.query(models.BorrowingHistory).filter(models.BorrowingHistory.id == borrowing_id).first()

    if not borrowing:
        raise HTTPException(status_code=404, detail="Запис оренди не знайдено")

    if borrowing.returned_at is not None:
        raise HTTPException(status_code=400, detail="Книга вже повернена")

    borrowing.returned_at = datetime.now(timezone.utc)

    book = db.query(models.Book).filter(models.Book.id == borrowing.book_id).first()
    if book:
        book.is_available = True

    db.commit()
    db.refresh(borrowing)

    return borrowing
