from typing import Optional
from sqlmodel import SQLModel, Field
from pydantic import validator

class VideogameBase(SQLModel):
    age: int = Field(..., ge=10, le=100)
    gender: str = Field(..., min_length=1, max_length=30)
    playing_hours: int = Field(..., ge=0, le=100)
    productive_time: int = Field(..., ge=0, le=100)
    image_url: str = Field(..., min_length=3, max_length=500)

class Videogame(SQLModel, table=True):
    """
    Representa la tabla 'videogames' en la base de datos.
    Guarda la información sobre la relación entre videojuegos y productividad.
    """
    __tablename__ = "videogames"

    id: Optional[int] = Field(default=None, primary_key=True)
    age: int = Field(..., ge=10, le=100, description="Edad del participante (10-100)")
    gender: str = Field(..., min_length=1, max_length=30, description="Género del participante")
    playing_hours: int = Field(..., ge=0, le=100, description="Horas dedicadas a videojuegos por día o semana")
    productive_time: int = Field(..., ge=0, le=100, description="Tiempo productivo del participante (porcentaje o valor)")
    image_url: str = Field(..., min_length=3, max_length=500, description="Ruta o URL de la imagen asociada")


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

class DeletedVideogame(SQLModel, table=True):
    """
    Tabla de respaldo para los registros eliminados de videojuegos.
    """
    __tablename__ = "deleted_videogames"

    id: Optional[int] = Field(default=None, primary_key=True)
    age: int = Field(..., ge=10, le=100)
    gender: str = Field(..., min_length=1, max_length=30)
    playing_hours: int = Field(..., ge=0, le=100)
    productive_time: int = Field(..., ge=0, le=100)
    image_url: str = Field(..., min_length=3, max_length=500)