from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
import app.schemas as schemas
import app.models as models
from datetime import date

router = APIRouter(prefix="/publishers", tags=["Publishers"])

@router.get("/", response_model=list[schemas.PublisherResponse])
def get_publishers(db: Session = Depends(get_db)):
    return db.query(models.Publisher).all()


@router.post("/", response_model=schemas.PublisherResponse)
def create_publisher(publisher: schemas.PublisherCreate, db: Session = Depends(get_db)):

    if publisher.established_date and publisher.established_date > date.today():
        raise HTTPException(status_code=400, detail="Дата видавництва не може бути в майбутньому!")

    db_publisher = models.Publisher(name=publisher.name, established_date=publisher.established_date)
    db.add(db_publisher)
    db.commit()
    db.refresh(db_publisher)
    return db_publisher


@router.get("/{publisher_id}", response_model=schemas.PublisherResponse)
def get_publisher(publisher_id: int, db: Session = Depends(get_db)):
    publisher = db.query(models.Publisher).filter(models.Publisher.id == publisher_id).first()
    if not publisher:
        raise HTTPException(status_code=404, detail="Видавця не знайдено")
    return publisher


@router.delete("/{publisher_id}")
def delete_publisher(publisher_id: int, db: Session = Depends(get_db)):
    publisher = db.query(models.Publisher).filter(models.Publisher.id == publisher_id).first()
    if not publisher:
        raise HTTPException(status_code=404, detail="Видавця не знайдено")
    db.delete(publisher)
    db.commit()
    return {"message": "Видавець успішно видалений"}