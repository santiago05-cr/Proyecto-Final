from typing import Optional
from sqlmodel import SQLModel, Field
from pydantic import validator
import hashlib

class MentalHealthBase(SQLModel):
    age: int = Field(..., ge=10, le=100)
    gender: str = Field(..., min_length=1, max_length=30)
    feel_after: str = Field(..., min_length=1, max_length=50)
    mental_harm: str = Field(..., regex=r"^(Yes|No)$")
    image_url: str = Field(..., min_length=3, max_length=500)

class MentalHealth(SQLModel, table=True):
    __tablename__ = "mental_health"  # Nombre real de la tabla en la BD
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    age: int = Field(..., ge=10, le=100, description="Edad del participante")
    gender: str = Field(..., min_length=1, max_length=30, description="Género del participante")
    feel_after: str = Field(..., min_length=1, max_length=50, description="Cómo se siente después del evento")
    mental_harm: str = Field(..., regex=r"^(Yes|No)$", description="Si hubo daño mental o no")
    image_url: str = Field(..., min_length=3, max_length=500, description="Ruta de la imagen asociada al registro")

class MentalHealthCreate(MentalHealthBase):
    pass

class MentalHealthRead(MentalHealthBase):
    id: int

class MentalHealthUpdate(SQLModel):
    age: Optional[int] = Field(..., ge=10, le=100)
    gender: Optional[str] = Field(..., min_length=1, max_length=30)
    feel_after: Optional[str] = Field(..., min_length=1, max_length=50)
    mental_harm: Optional[str] = Field(..., regex=r"^(Yes|No)$")
    image_url: Optional[str] = Field(..., min_length=3, max_length=500)

    @validator('*', pre=True)
    def skip_blank_strings(cls, v):
        if v == "":
            return None
        return v

class MentalHealthResponse(SQLModel):
    id: int
    age: int
    gender: str
    feel_after: str
    mental_harm: str
    image_url: str

class DeletedMentalHealth(MentalHealthBase, table=True):
    __tablename__ = "deleted_mental_health"
    id: Optional[int] = Field(default=None, primary_key=True)

class UserBase(SQLModel):
    username: str = Field(..., min_length=3, max_length=50, unique=True)
    email: str = Field(..., regex=r'^\S+@\S+\.\S+$')
    full_name: Optional[str] = Field(default=None, max_length=100)

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    password: str

class UserCreate(UserBase):
    password: str = Field(..., min_length=4, max_length=100)


class UserLogin(SQLModel):
    username: str
    password: str

class UserRead(UserBase):
    id: int

# Función para hashear contraseña
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode('utf-8')).hexdigest()