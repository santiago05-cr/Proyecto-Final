from typing import Optional
from sqlmodel import SQLModel, Field


class MentalHealth(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    age: int = Field(..., ge=10, le=100)
    gender: str = Field(..., min_length=1, max_length=30)
    feel_after: str = Field(..., min_length=1, max_length=50)
    mental_harm: str = Field(..., regex="^(Yes|No)$")


# Entrada (crear)
class MentalHealthCreate(SQLModel):
    age: int = Field(..., ge=10, le=100)
    gender: str = Field(..., min_length=1, max_length=30)
    feel_after: str = Field(..., min_length=1, max_length=50)
    mental_harm: str = Field(..., regex="^(Yes|No)$")


# Actualización parcial
class MentalHealthUpdate(SQLModel):
    age: Optional[int] = Field(None, ge=10, le=100)
    gender: Optional[str] = Field(None, min_length=1, max_length=30)
    feel_after: Optional[str] = Field(None, min_length=1, max_length=50)
    mental_harm: Optional[str] = Field(None, regex="^(Yes|No)$")


# Respuesta (output)
class MentalHealthResponse(SQLModel):
    id: int
    age: int
    gender: str
    mental_harm: str
