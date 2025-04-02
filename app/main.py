from fastapi import FastAPI
import app.routers.books as books
import app.routers.authors as authors
import app.routers.genres as genres
import app.routers.publishers as publishers
import app.routers.borrowers as borrowers
import app.routers.borrowing_history as borrowing_history
from .database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Library API")

app.include_router(books.router)
app.include_router(authors.router)
app.include_router(genres.router)
app.include_router(publishers.router)
app.include_router(borrowers.router)
app.include_router(borrowing_history.router)
