from pydantic import BaseModel, PastDate, EmailStr, Field, ConfigDict
from pydantic_extra_types.isbn import ISBN
from datetime import datetime

class BookBase(BaseModel):
    title: str = Field(..., min_length=1)
    isbn: ISBN
    published_year: int = Field(..., ge=1440, le=datetime.today().year)
    

class BookCreate(BookBase):
    author_name: str = Field(..., min_length=1)
    genre_name: str = Field(..., min_length=1)
    publisher_name: str = Field(..., min_length=1)

class BookResponse(BookBase):
    id: int
    author_name: str
    genre_name: str
    publisher_name: str
    
class AuthorBase(BaseModel):
    name: str = Field(..., min_length=1)
    birthdate: PastDate | None
    model_config = ConfigDict(from_attributes = True)

class AuthorCreate(AuthorBase):
    pass

class AuthorResponse(AuthorBase):
    id: int

class GenreBase(BaseModel):
    name: str = Field(..., min_length=1)
    model_config = ConfigDict(from_attributes = True)

class GenreCreate(GenreBase):
    pass

class GenreResponse(GenreBase):
    id: int


class PublisherBase(BaseModel):
    name: str = Field(..., min_length=1)
    established_date: PastDate | None
    model_config = ConfigDict(from_attributes = True)

class PublisherCreate(PublisherBase):
    pass

class PublisherResponse(PublisherBase):
    id: int


class BorrowerBase(BaseModel):
    name: str = Field(..., min_length=1)
    email: EmailStr
    model_config = ConfigDict(from_attributes = True)

class BorrowerCreate(BorrowerBase):
    pass

class BorrowerResponse(BorrowerBase):
    id: int


class BorrowingHistoryBase(BaseModel):
    book_id: int
    borrower_id: int
    model_config = ConfigDict(from_attributes = True)

class BorrowingHistoryCreate(BorrowingHistoryBase):
    pass

class BorrowingHistoryResponse(BorrowingHistoryBase):
    id: int
    borrower_name: str 
    borrower_email: str
    borrowed_at: datetime
    returned_at: datetime | None


class UserBase(BaseModel):
    username: str = Field(..., min_length=1)
    email: EmailStr
    model_config = ConfigDict(from_attributes = True)


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class User(UserBase):
    id: int

class Token(BaseModel):
    access_token: str
    token_type: str