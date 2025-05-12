from typing import Optional
from sqlmodel import SQLModel, Field

class Videogame(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    age: int = Field(..., ge=10, le=100)
    gender: str = Field(..., min_length=1, max_length=30)
    playing_hours: int = Field(..., ge=0)
    productive_time: int = Field(..., ge=0)


# Modelo para creación (sin ID)
class VideogameCreate(SQLModel):
    age: int = Field(..., ge=10, le=100)
    gender: str = Field(..., min_length=1, max_length=30)
    playing_hours: int = Field(..., ge=0)
    productive_time: int = Field(..., ge=0)


# Modelo para actualización (todos los campos opcionales)
class VideogameUpdate(SQLModel):
    age: Optional[int] = Field(None, ge=10, le=100)
    gender: Optional[str] = Field(None, min_length=1, max_length=30)
    playing_hours: Optional[int] = Field(None, ge=0)
    productive_time: Optional[int] = Field(None, ge=0)


# Modelo para respuesta (con ID)
class VideogameResponse(SQLModel):
    id: int
    age: int
    gender: str
    playing_hours: int
    productive_time: int
