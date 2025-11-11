from fastapi import FastAPI, HTTPException, Depends, Request, Form, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import List
from sqlmodel import Session, select
from utils.connection_db import *
from mental_health_models import *
from videogame_models import *
from mental_health_operations import MentalHealthOperations
from videogame_operations import VideogameOperations
from datetime import datetime
import os

# ---------------- CONFIGURACIÓN ----------------
app = FastAPI(
    title="Impacto De Los Videojuegos En La Salud Mental",
    description="API entrega de tercer corte de la materia de desarrollo de software 7-9.",
    version="1.0.0"
)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join("static", "img", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def home():
    """Redirige automáticamente al formulario de login"""
    return RedirectResponse(url="/login")


# ---------------- FUNCIONES AUXILIARES ----------------
async def save_image_locally(file: UploadFile) -> str:
    """Guarda una imagen localmente en static/img/uploads/"""
    if file.content_type not in ["image/png", "image/jpeg"]:
        raise HTTPException(status_code=400, detail="Solo se permiten imágenes PNG o JPG")

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    extension = ".png" if file.content_type == "image/png" else ".jpg"
    filename = f"{timestamp}_{file.filename}"
    filepath = os.path.join(UPLOAD_DIR, filename)

    content = await file.read()
    with open(filepath, "wb") as f:
        f.write(content)

    return f"/static/img/uploads/{filename}"


@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

@app.get("/mental_health/by_age", response_model=List[MentalHealthResponse], tags=["Salud Mental"])
async def search_by_age(age: int, session: AsyncSession = Depends(get_session)):
    results = await MentalHealthOperations.search_mental_health_by_age(session, age)
    if not results:
        raise HTTPException(status_code=404, detail="No se encontraron registros con ese edad")
    return results

@app.get("/mental_health/search_mental_health_by_field", response_model=List[MentalHealthResponse],
         tags=["Salud Mental"])
async def search_cosmetic_by_field(
        field: str,
        value: str,
        session: AsyncSession = Depends(get_session)
):
    """
    Busca registros de salud mental por cualquier campo especificado.
    Campos disponibles: id,age,gender,feel_after,mental_harm,image_url.
    """
    results = await MentalHealthOperations.search_mental_health_by_field(session, field, value)
    if not results:
        raise HTTPException(
            status_code=404,
            detail=f"No se encontraron registros con {field} que contenga '{value}'"
        )
    return results

@app.get("/videogames/search_by_field", response_model=List[VideogameResponse], tags=["Videojuegos"])
async def search_videogame_by_field(
        field: str,
        value: str,
        session: AsyncSession = Depends(get_session)
):
    """
    Busca colaboraciones de videojuegos por cualquier campo especificado.
    Campos disponibles: id,age,gender,playing_hours,productive_time,image_url
    """
    results = await VideogameOperations.search_videogame_by_field(session, field, value)
    if not results:
        raise HTTPException(
            status_code=404,
            detail=f"No se encontraron registros con {field} que contenga '{value}'"
        )
    return results

@app.get("/mental_health", response_class=HTMLResponse, tags=["Salud Mental"])
async def get_mental_health(request: Request, session: AsyncSession = Depends(get_session)):
    records = await MentalHealthOperations.get_all_mental_health(session)
    return templates.TemplateResponse(
        "records.html",
        {
            "request": request,
            "records": records,
            "tipo": "mental_health"
        }
    )

@app.get("/mental_health/by_age", response_model=List[MentalHealthResponse], tags=["Salud Mental"])
async def filter_mental_health_by_age(session: AsyncSession = Depends(get_session)):
    return await MentalHealthOperations.filter_mental_health_by_age(session)



@app.put("/mental_health/{mental_health_id}", response_model=MentalHealthResponse, tags=["Salud Mental"])
async def update_mental_health_endpoint(
        mental_health_id: int,
        age: str = Form(None),
        gender: str = Form(None),
        feel_after: str = Form(None),
        mental_harm: str = Form(None),
        image_file: UploadFile = None,
        session: AsyncSession = Depends(get_session)
):
    """
    Actualiza un registro de salud mental.
    Solo los campos enviados en la solicitud serán actualizados.
    """
    update_data = {}

    # Recopilar campos no nulos
    if age:
        try:
            age = int(age)
        except ValueError:
            raise HTTPException(status_code=400, detail="La edad debe ser un número entero.")
        update_data["age"] = age
    if gender: update_data["gender"] = gender
    if feel_after: update_data["feel_after"] = feel_after
    if mental_harm: update_data["mental_harm"] = mental_harm

    # Si hay una nueva imagen, procesarla
    if image_file and image_file.filename:
        image_url = await save_image_locally(image_file)
        if isinstance(image_url, dict) and "error" in image_url:
            raise HTTPException(status_code=400, detail=image_url["error"])
        update_data["image_url"] = image_url

    updated = await MentalHealthOperations.update_mental_health(session, mental_health_id, update_data)
    if not updated:
        raise HTTPException(status_code=404, detail="El registro no fue actualizado")
    return updated

@app.post("/mental_health/delete/{mental_health_id}", tags=["Salud Mental"])
async def delete_mental_health_by_id(
        mental_health_id: int,
        session: AsyncSession = Depends(get_session)
):
    """Elimina un registro de salud mental y lo mueve a la tabla de eliminados"""
    try:
        # Obtener el registro antes de eliminarlo
        record = await MentalHealthOperations.get_mental_health_by_id(session, mental_health_id)
        if not record:
            raise HTTPException(status_code=404, detail="Registro no encontrado")

        # Crear entrada en la tabla de eliminados
        deleted_record = DeletedMentalHealth(**record.dict())
        session.add(deleted_record)

        # Eliminar el registro original
        await session.delete(record)
        await session.commit()

        return {"message": "Registro eliminado y movido a la tabla de eliminados"}
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=str(e))



@app.get("/videogames/by_gender", response_model=List[VideogameResponse], tags=["Videojuegos"])
async def search_by_gender(gender: str, session: AsyncSession = Depends(get_session)):
    results = await VideogameOperations.search_videogames_by_gender(session, gender)
    if not results:
        raise HTTPException(status_code=404, detail="No se encontraron videojuegos con ese género")
    return results

@app.get("/videogames/search_by_field", response_model=List[VideogameResponse], tags=["Videojuegos"])
async def search_videogame_by_field(
        field: str,
        value: str,
        session: AsyncSession = Depends(get_session)
):
    """
    Busca colaboraciones de videojuegos por cualquier campo especificado.
    Campos disponibles: id,age,gender,playing_hours,productive_time,image_url
    """
    results = await VideogameOperations.search_videogame_by_field(session, field, value)
    if not results:
        raise HTTPException(
            status_code=404,
            detail=f"No se encontraron registros con {field} que contenga '{value}'"
        )
    return results

@app.get("/videogames/by_age", response_model=List[VideogameResponse], tags=["Videojuegos"])
async def get_videogames_by_age(age: int, session: AsyncSession = Depends(get_session)):
    """Obtiene videojuegos filtrados por edad"""
    results = await VideogameOperations.filter_by_age(session, age)
    if not results:
        raise HTTPException(status_code=404, detail=f"No se encontraron registros para la edad {age}")
    return results

@app.get("/videogames/{videogame_id}", response_model=VideogameResponse, tags=["Videojuegos"])
async def get_videogame(videogame_id: int, session: AsyncSession = Depends(get_session)):
    videogame = await VideogameOperations.get_videogame_by_id(session, videogame_id)
    if not videogame:
        raise HTTPException(status_code=404, detail="registro de videojuegos no encontrado.")
    return videogame

@app.post("/videogames/delete/{videogame_id}", tags=["Videojuegos"])
async def delete_videogame_by_id(
        videogame_id: int,
        session: AsyncSession = Depends(get_session)
):
    """Elimina un videojuego y lo mueve a la tabla de eliminados"""
    try:
        # Obtener el registro antes de eliminarlo
        record = await VideogameOperations.get_videogame_by_id(session, videogame_id)
        if not record:
            raise HTTPException(status_code=404, detail="Registro no encontrado")

        # Crear entrada en la tabla de eliminados
        deleted_record = DeletedVideogame(**record.dict())
        session.add(deleted_record)

        # Eliminar el registro original
        await session.delete(record)
        await session.commit()

        return {"message": "Registro eliminado y movido a la tabla de eliminados"}
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=str(e))



# ---------------- LOGIN Y REGISTRO ----------------
@app.get("/home", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Muestra el formulario de login"""
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
async def login_user(request: Request, username: str = Form(...), password: str = Form(...)):
    async with AsyncSession(engine) as session:
        result = await session.execute(
            select(User).where(User.username == username, User.password == password)
        )
        user = result.scalar_one_or_none()

        if not user:
            return templates.TemplateResponse("login.html", {"request": request, "error": "Usuario o contraseña incorrectos"})

        response = RedirectResponse(url="/home", status_code=302)
        response.set_cookie(key="username", value=username)
        return response



@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    """Muestra el formulario de registro"""
    return templates.TemplateResponse("register.html", {"request": request})


@app.post("/register")
async def register_user(request: Request, username: str = Form(...), password: str = Form(...)):
    async with AsyncSession(engine) as session:
        existing_user = await session.execute(select(User).where(User.username == username))
        existing_user = existing_user.scalar_one_or_none()

        if existing_user:
            return templates.TemplateResponse("register.html", {"request": request, "error": "El usuario ya existe"})

        new_user = User(username=username, password=password)
        session.add(new_user)
        await session.commit()  # ✅ Importante: usar await
        await session.refresh(new_user)

        return templates.TemplateResponse("login.html", {"request": request, "success": "Usuario registrado con éxito"})


# ---------------- ELIMINADOS ----------------
@app.get("/mental_health/deleted", response_model=List[DeletedMentalHealth], tags=["Eliminados"])
async def get_deleted_mental_health(session: AsyncSession = Depends(get_session)):
    return await MentalHealthOperations.get_deleted_mental_health(session)


@app.get("/videogame/deleted", response_model=List[DeletedVideogame], tags=["Eliminados"])
async def get_deleted_videogames(session: AsyncSession = Depends(get_session)):
    return await VideogameOperations.get_deleted_videogames(session)


@app.get("/deleted", response_class=HTMLResponse, tags=["Eliminados"])
async def view_deleted(request: Request, session: AsyncSession = Depends(get_session)):
    deleted_mental_health = await MentalHealthOperations.get_deleted_mental_health(session)
    deleted_videogame = await VideogameOperations.get_deleted_videogames(session)
    return templates.TemplateResponse(
        "deleted.html",
        {"request": request,
         "deleted_mental_health": deleted_mental_health,
         "deleted_videogame": deleted_videogame}
    )

@app.get("/delete", response_class=HTMLResponse, tags=["Eliminación"])
async def delete_page(request: Request):
    """Página para eliminar registros"""
    return templates.TemplateResponse("delete.html", {"request": request})


# ---------------- SALUD MENTAL ----------------

@app.get("/mental_health/by_age", response_model=List[MentalHealthResponse], tags=["Salud Mental"])
async def search_by_age(age: int, session: AsyncSession = Depends(get_session)):
    results = await MentalHealthOperations.search_mental_health_by_age(session, age)
    if not results:
        raise HTTPException(status_code=404, detail="No se encontraron registros con ese edad")
    return results

@app.get("/mental_health/{mental_health_id}", response_model=MentalHealthResponse, tags=["Salud Mental"])
async def get_mental_health(mental_health_id: int, session: AsyncSession = Depends(get_session)):
    mental_health = await MentalHealthOperations.get_mental_health_by_id(session, mental_health_id)
    if not mental_health:
        raise HTTPException(status_code=404, detail="Registro de salud mental no encontrado")
    return mental_health



@app.post("/mental_health/upload", tags=["Salud Mental"])
async def create_mental_health_with_image(
    age: int = Form(...),
    gender: str = Form(...),
    feel_after: str = Form(...),
    mental_harm: str = Form(...),
    image_file: UploadFile = Form(...),
    session: AsyncSession = Depends(get_session)
):
    image_url = await save_image_locally(image_file)
    new_data = MentalHealthCreate(
        age=age, gender=gender, feel_after=feel_after,
        mental_harm=mental_harm, image_url=image_url
    )
    new_entry = await MentalHealthOperations.create_mental_health(session, new_data.dict())
    return {"message": "Registro creado exitosamente", "id": new_entry.id}


@app.get("/videogames/{videogame_id}", response_model=VideogameResponse, tags=["Videojuegos"])
async def get_videogame(videogame_id: int, session: AsyncSession = Depends(get_session)):
    videogame = await VideogameOperations.get_videogame_by_id(session, videogame_id)
    if not videogame:
        raise HTTPException(status_code=404, detail="registro de videojuegos no encontrado.")
    return videogame

# ---------------- VIDEOJUEGOS ----------------
@app.get("/videogame", response_class=HTMLResponse, tags=["Videojuegos"])
async def get_videogames(request: Request, session: AsyncSession = Depends(get_session)):
    records = await VideogameOperations.get_all_videogames(session)
    return templates.TemplateResponse(
        "records.html",
        {"request": request, "records": records, "tipo": "videogame"}
    )


@app.post("/videogames/upload", tags=["Videojuegos"])
async def create_videogame_with_image(
    age: int = Form(...),
    gender: str = Form(...),
    playing_hours: int = Form(...),
    productive_time: int = Form(...),
    image_file: UploadFile = Form(...),
    session: AsyncSession = Depends(get_session)
):
    image_url = await save_image_locally(image_file)
    new_data = VideogameCreate(
        age=age, gender=gender,
        playing_hours=playing_hours, productive_time=productive_time,
        image_url=image_url
    )
    new_entry = await VideogameOperations.create_videogame(session, new_data.dict())
    return {"message": "Registro creado exitosamente", "id": new_entry.id}

@app.put("/videogames/{videogame_id}", response_model=VideogameResponse, tags=["Videojuegos"])
async def update_videogame_endpoint(
        videogame_id: int,
        age: str = Form(None),
        gender: str = Form(None),
        playing_hours: str = Form(None),
        productive_time: str = Form(None),
        image_file: UploadFile = None,
        session: AsyncSession = Depends(get_session)
):
    """
    Actualiza un registro de videojuegos.
    Solo los campos enviados en la solicitud serán actualizados.
    """
    update_data = {}

    # Recopilar campos no nulos
    if age:
        try:
            age = int(age)
        except ValueError:
            raise HTTPException(status_code=400, detail="La edad debe ser un número entero.")
        update_data["age"] = age
    if gender: update_data["gender"] = gender
    if playing_hours:
        try:
            playing_hours = int(playing_hours)
        except ValueError:
            raise HTTPException(status_code=400, detail="playing_hours debe ser un número entero.")
        update_data["playing_hours"] = playing_hours

    if productive_time:
        try:
            productive_time = int(productive_time)
        except ValueError:
            raise HTTPException(status_code=400, detail="productive_time debe ser un número entero.")
        update_data["productive_time"] = productive_time

    # Si hay una nueva imagen, procesarla
    if image_file and image_file.filename:
        image_url = await save_image_locally(image_file)
        if isinstance(image_url, dict) and "error" in image_url:
            raise HTTPException(status_code=400, detail=image_url["error"])
        update_data["image_url"] = image_url

    updated = await VideogameOperations.update_videogame(session, videogame_id, update_data)
    if not updated:
        raise HTTPException(status_code=404, detail="el registro no fue actualizado.")
    return updated


@app.get("/show", response_class=HTMLResponse, tags=["Registros"])
async def show_records(
        request: Request,
        session: AsyncSession = Depends(get_session)
):
    mental_health = await MentalHealthOperations.get_all_mental_health(session)
    videogame = await VideogameOperations.get_all_videogames(session)

    return templates.TemplateResponse(
        "show.html",
        {
            "request": request,
            "mental_health": mental_health,
            "videogame": videogame
        }
    )
# ---------------- OTRAS PÁGINAS ----------------
@app.get("/create", response_class=HTMLResponse)
async def create_page(request: Request):
    return templates.TemplateResponse("create.html", {"request": request})


@app.get("/update", response_class=HTMLResponse)
async def update_page(request: Request):
    return templates.TemplateResponse("update.html", {"request": request})


@app.get("/query", response_class=HTMLResponse)
async def query_page(request: Request):
    return templates.TemplateResponse("query.html", {"request": request})


@app.get("/developer", response_class=HTMLResponse)
async def developer_info(request: Request):
    return templates.TemplateResponse("developer.html", {"request": request})


@app.get("/goal", response_class=HTMLResponse)
async def objetivo_proyecto(request: Request):
    return templates.TemplateResponse("goal.html", {"request": request})


@app.get("/planning", response_class=HTMLResponse)
async def planeacion_proyecto(request: Request):
    return templates.TemplateResponse("planning.html", {"request": request})


@app.get("/design", response_class=HTMLResponse)
async def diseno_proyecto(request: Request):
    return templates.TemplateResponse("design.html", {"request": request})
