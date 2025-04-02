from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
import app.schemas as schemas
import app.models as models

router = APIRouter(prefix="/borrowers", tags=["Borrowers"])

@router.get("/", response_model=list[schemas.BorrowerResponse])
def get_borrowers(db: Session = Depends(get_db)):
    return db.query(models.Borrower).all()


@router.post("/", response_model=schemas.BorrowerResponse)
def create_borrower(borrower: schemas.BorrowerCreate, db: Session = Depends(get_db)):
    db_borrower = models.Borrower(name=borrower.name, email=borrower.email)
    db.add(db_borrower)
    db.commit()
    db.refresh(db_borrower)
    return db_borrower


@router.get("/{borrower_id}", response_model=schemas.BorrowerResponse)
def get_borrower(borrower_id: int, db: Session = Depends(get_db)):
    borrower = db.query(models.Borrower).filter(models.Borrower.id == borrower_id).first()
    if not borrower:
        raise HTTPException(status_code=404, detail="Читача не знайдено")
    return borrower


@router.delete("/{borrower_id}")
def delete_borrower(borrower_id: int, db: Session = Depends(get_db)):
    borrower = db.query(models.Borrower).filter(models.Borrower.id == borrower_id).first()
    if not borrower:
        raise HTTPException(status_code=404, detail="Читача не знайдено")
    db.delete(borrower)
    db.commit()
    return {"message": "Читач успішно видалений"}