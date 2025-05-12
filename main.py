from fastapi import FastAPI, HTTPException
from fastapi.params import Depends
from starlette.responses import JSONResponse
from typing import List
from contextlib import asynccontextmanager
from sqlmodel.ext.asyncio.session import AsyncSession

from connection_db import get_session
# Importar modelos
from mental_health import MentalHealth, MentalHealthCreate, MentalHealthUpdate, MentalHealthResponse
from videogame import Videogame, VideogameCreate, VideogameUpdate, VideogameResponse

# Importar operaciones
from mental_health_operations import MentalHealthOperations
from videogame_operations import VideogameOperations

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
def root():
    return {"message": "Mental Health & Video Games API"}

# =====================================================
# Endpoints para registros de salud mental
# =====================================================

@app.get("/mental_health", response_model=List[MentalHealthResponse])
async def get_all_mental_health():
    async for session in get_session():
        return await MentalHealthOperations.get_all(session)

@app.get("/mental_health/{entry_id}", response_model=MentalHealthResponse)
async def get_mental_health(entry_id: int):
    async for session in get_session():
        entry = await MentalHealthOperations.get_by_id(session, entry_id)
        if not entry:
            raise HTTPException(status_code=404, detail="Registro de salud mental no encontrado")
        return entry

@app.post("/mental_health", response_model=MentalHealthResponse)
async def create_mental_health(entry: MentalHealthCreate):
    async for session in get_session():
        try:
            return await MentalHealthOperations.create(session, entry.dict())
        except Exception as e:
            await session.rollback()
            raise HTTPException(status_code=400, detail=str(e))

@app.put("/mental_health/{entry_id}", response_model=MentalHealthResponse)
async def update_mental_health(entry_id: int, update_data: MentalHealthUpdate):
    async for session in get_session():
        updated = await MentalHealthOperations.update(session, entry_id, update_data.dict(exclude_unset=True))
        if not updated:
            raise HTTPException(status_code=404, detail="El registro de salud mental no fue actualizado")
        return updated

@app.delete("/mental_health/{entry_id}", response_model=MentalHealthResponse)
async def delete_mental_health(entry_id: int):
    async for session in get_session():
        deleted = await MentalHealthOperations.delete(session, entry_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="El registro de salud mental no fue eliminado")
        return deleted

@app.get("/mental_health/search_by_age/", response_model=List[MentalHealthResponse])
async def search_by_age(age: int):
    async for session in get_session():
        results = await MentalHealthOperations.search_by_age(session, age)
        if not results:
            raise HTTPException(status_code=404, detail=f"No records found for age: {age}")
        return results

@app.get("/mental_health/filter_by_mental_harm/", response_model=List[MentalHealthResponse])
async def filter_by_mental_harm():
    async for session in get_session():
        results = await MentalHealthOperations.filter_by_mental_harm(session)
        if not results:
            raise HTTPException(status_code=404, detail="No records found for mental harm")
        return results

# =====================================================
# Endpoints para registros de videojuegos
# =====================================================

@app.get("/videogame", response_model=List[VideogameResponse])
async def get_all_videogame():
    async for session in get_session():
        return await VideogameOperations.get_all(session)

@app.get("/videogame/{entry_id}", response_model=VideogameResponse)
async def get_videogame(entry_id: int):
    async for session in get_session():
        entry = await VideogameOperations.get_by_id(session, entry_id)
        if not entry:
            raise HTTPException(status_code=404, detail="Registro de videojuego no encontrado")
        return entry

@app.post("/videogame", response_model=VideogameResponse)
async def create_videogame(entry: VideogameCreate):
    async for session in get_session():
        try:
            return await VideogameOperations.create(session, entry.dict())
        except Exception as e:
            await session.rollback()
            raise HTTPException(status_code=400, detail=str(e))

@app.put("/videogame/{entry_id}", response_model=VideogameResponse)
async def update_videogame(entry_id: int, update_data: VideogameUpdate):
    async for session in get_session():
        updated = await VideogameOperations.update(session, entry_id, update_data.dict(exclude_unset=True))
        if not updated:
            raise HTTPException(status_code=404, detail="El registro de videojuego no fue actualizado")
        return updated

@app.delete("/videogame/{entry_id}", response_model=VideogameResponse)
async def delete_videogame(entry_id: int):
    async for session in get_session():
        deleted = await VideogameOperations.delete(session, entry_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="El registro de videojuego no fue eliminado")
        return deleted

@app.get("/videogame/search_by_age/", response_model=List[VideogameResponse])
async def search_videogame_by_age_endpoint(age: int):
    async for session in get_session():
        results = await VideogameOperations.search_by_age(session, age)
        if not results:
            raise HTTPException(status_code=404, detail=f"No records found for age: {age}")
        return results

@app.get("/videogame/filter_by_playing_hours/", response_model=List[VideogameResponse])
async def filter_videogame_by_playing_hours_endpoint():
    async for session in get_session():
        results = await VideogameOperations.filter_by_playing_hours(session)
        if not results:
            raise HTTPException(status_code=404, detail="No videogames found with specified playing hours")
        return results

# =====================================================
# Manejo personalizado de errores
# =====================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "msg": "¡Ha ocurrido un error!",
            "detail": exc.detail,
            "path": str(request.url)
        }
    )

@app.get("/error")
def raise_exception():
    raise HTTPException(status_code=400)


# --- Endpoints básicos ---
@app.get("/")
async def root():
    return {"message": "Mental Health & Video Games API"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hola {name}, bienvenido al sistema de gestión"}
