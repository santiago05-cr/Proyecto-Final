from typing import Optional
from sqlmodel import SQLModel, Field
from pydantic import validator

class MentalHealthBase(SQLModel):
    age: int = Field(..., ge=10, le=100)
    gender: str = Field(..., min_length=1, max_length=30)
    feel_after: str = Field(..., min_length=1, max_length=50)
    mental_harm: str = Field(..., regex=r"^(Yes|No)$")
    image_url: str = Field(..., min_length=3, max_length=500)

class MentalHealth(MentalHealthBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

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