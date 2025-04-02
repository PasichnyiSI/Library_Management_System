from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
import app.schemas as schemas
import app.models as models

router = APIRouter(prefix="/genres", tags=["Genres"])

@router.get("/", response_model=list[schemas.GenreResponse])
def get_genres(db: Session = Depends(get_db)):
    return db.query(models.Genre).all()


@router.post("/", response_model=schemas.GenreResponse)
def create_genre(genre: schemas.GenreCreate, db: Session = Depends(get_db)):
    db_genre = models.Genre(name=genre.name)
    db.add(db_genre)
    db.commit()
    db.refresh(db_genre)
    return db_genre


@router.get("/{genre_id}", response_model=schemas.GenreResponse)
def get_genre(genre_id: int, db: Session = Depends(get_db)):
    genre = db.query(models.Genre).filter(models.Genre.id == genre_id).first()
    if not genre:
        raise HTTPException(status_code=404, detail="Жанр не знайдений")
    return genre


@router.delete("/{genre_id}")
def delete_genre(genre_id: int, db: Session = Depends(get_db)):
    genre = db.query(models.Genre).filter(models.Genre.id == genre_id).first()
    if not genre:
        raise HTTPException(status_code=404, detail="Жанр не знайдений")
    db.delete(genre)
    db.commit()
    return {"message": "Жанр успішно видалений"}