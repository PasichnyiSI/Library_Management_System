from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Date
from datetime import datetime, timezone
from sqlalchemy.orm import relationship
from .database import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    isbn = Column(String, unique=True)
    published_year = Column(Integer)
    is_available = Column(Boolean, default=True)
    author_id = Column(Integer, ForeignKey("authors.id", ondelete="CASCADE"))
    genre_id = Column(Integer, ForeignKey("genres.id", ondelete="CASCADE"))
    publisher_id = Column(Integer, ForeignKey("publishers.id", ondelete="CASCADE"))

    author = relationship("Author", back_populates="books")
    genre = relationship("Genre", back_populates="books")
    publisher = relationship("Publisher", back_populates="books")
    borrow_history = relationship("BorrowingHistory", back_populates="book")
    

class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)
    birthdate = Column(Date, nullable=True)

    books = relationship("Book", back_populates="author")


class Genre(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)

    books = relationship("Book", back_populates="genre")


class Publisher(Base):
    __tablename__ = "publishers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    established_date = Column(Date, nullable=True)

    books = relationship("Book", back_populates="publisher")


class Borrower(Base):
    __tablename__ = "borrowers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True)

    borrow_history = relationship("BorrowingHistory", back_populates="borrower")


class BorrowingHistory(Base):
    __tablename__ = "borrowing_history"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False)
    borrower_id = Column(Integer, ForeignKey("borrowers.id", ondelete="CASCADE"), nullable=False)
    borrowed_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    returned_at = Column(DateTime, nullable=True)

    book = relationship("Book", back_populates="borrow_history")
    borrower = relationship("Borrower", back_populates="borrow_history")
    
