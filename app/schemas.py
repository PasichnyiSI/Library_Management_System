from pydantic import BaseModel, PastDate, EmailStr, Field
from pydantic_extra_types.isbn import ISBN
from datetime import datetime

class BookBase(BaseModel):
    title: str
    isbn: ISBN
    published_year: int = Field(ge=1440, le=datetime.today().year)

class BookCreate(BookBase):
    author_name: str
    genre_name: str
    publisher_name: str

class BookResponse(BookBase):
    id: int
    author_name: str
    genre_name: str
    publisher_name: str

    class Config:
        from_attributes = True


class AuthorBase(BaseModel):
    name: str
    birthdate: PastDate | None

class AuthorCreate(AuthorBase):
    pass

class AuthorResponse(AuthorBase):
    id: int

    class Config:
        from_attributes = True


class GenreBase(BaseModel):
    name: str

class GenreCreate(GenreBase):
    pass

class GenreResponse(GenreBase):
    id: int

    class Config:
        from_attributes = True


class PublisherBase(BaseModel):
    name: str
    established_date: PastDate | None

class PublisherCreate(PublisherBase):
    pass

class PublisherResponse(PublisherBase):
    id: int

    class Config:
        from_attributes = True


class BorrowerBase(BaseModel):
    name: str
    email: EmailStr

class BorrowerCreate(BorrowerBase):
    pass

class BorrowerResponse(BorrowerBase):
    id: int

    class Config:
        from_attributes = True


class BorrowingHistoryBase(BaseModel):
    book_id: int
    borrower_id: int

class BorrowingHistoryCreate(BorrowingHistoryBase):
    pass

class BorrowingHistoryResponse(BorrowingHistoryBase):
    id: int
    borrower_name: str
    borrower_email: str
    borrowed_at: datetime
    returned_at: datetime | None

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str