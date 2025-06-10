from typing import Optional
from sqlmodel import SQLModel, Field
from pydantic import validator

class VideogameBase(SQLModel):
    age: int = Field(..., ge=10, le=100)
    gender: str = Field(..., min_length=1, max_length=30)
    playing_hours: int = Field(..., ge=0, le=100)
    productive_time: int = Field(..., ge=0, le=100)
    image_url: str = Field(..., min_length=3, max_length=500)

class Videogame(VideogameBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class VideogameCreate(VideogameBase):
    pass

class VideogameRead(VideogameBase):
    id: int

class VideogameUpdate(SQLModel):
    age: Optional[int] = Field(..., ge=10, le=100)
    gender: Optional[str] = Field(..., min_length=1, max_length=30)
    playing_hours: Optional[int] = Field(..., ge=0, le=100)
    productive_time: Optional[int] = Field(..., ge=0, le=100)
    image_url: Optional[str] = Field(..., min_length=3, max_length=500)

    @validator('*', pre=True)
    def skip_blank_strings(cls, v):
        if v == "":
            return None
        return v

class VideogameResponse(SQLModel):
    id: int
    age: int
    gender: str
    playing_hours: int
    productive_time: int
    image_url: str

class DeletedVideogame(VideogameBase, table=True):
    __tablename__ = "deleted_videogame"
    id: Optional[int] = Field(default=None, primary_key=True)