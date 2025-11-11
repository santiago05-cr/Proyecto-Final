from typing import List, Optional
from sqlmodel import select
from sqlalchemy import func
from sqlmodel.ext.asyncio.session import AsyncSession
from videogame_models import *


class VideogameOperations:

    @staticmethod
    async def get_all_videogames(session: AsyncSession) -> List[Videogame]:
        """Obtiene todos los registros de colaboraciones de videojuegos"""
        result = await session.execute(select(Videogame))
        return result.scalars().all()

    @staticmethod
    async def get_videogame_by_id(session: AsyncSession, entry_id: int) -> Optional[Videogame]:
        """Obtiene un registro por su ID"""
        result = await session.execute(
            select(Videogame).where(Videogame.id == entry_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def create_videogame(session: AsyncSession, data: dict) -> Videogame:
        """Crea un nuevo registro de colaboración de videojuegos"""
        new_entry = Videogame(**data)
        session.add(new_entry)
        await session.commit()
        await session.refresh(new_entry)
        return new_entry

    @staticmethod
    async def update_videogame(session: AsyncSession, entry_id: int, update_data: dict) -> Optional[Videogame]:
        """Modifica un registro existente, permitiendo cambios parciales o totales"""
        entry = await session.get(Videogame, entry_id)
        if not entry:
            return None

        for key, value in update_data.items():
            if hasattr(entry, key):
                # Solo actualiza si el valor no es None ni una cadena vacía
                if value not in (None, ""):
                    setattr(entry, key, value)

        await session.commit()
        await session.refresh(entry)
        return entry

    @staticmethod
    async def delete_videogame(session: AsyncSession, entry_id: int) -> Optional[Videogame]:
        """Elimina un registro por ID y lo guarda en deleted_videogame"""
        entry = await session.get(Videogame, entry_id)
        if not entry:
            return None

        # Validar los datos antes de crear la copia
        try:
            deleted_entry = DeletedVideogame(**entry.dict())
        except ValueError as e:
            # Manejar errores de validación
            raise ValueError(f"Error al validar los datos para la tabla de eliminados: {e}")

        session.add(deleted_entry)
        await session.delete(entry)
        await session.commit()
        return entry

    @staticmethod
    async def get_deleted_videogames(session: AsyncSession) -> List[DeletedVideogame]:
        """Obtiene todos los registros eliminados de videojuegos"""
        result = await session.execute(select(DeletedVideogame))
        return result.scalars().all()

    @staticmethod
    async def search_videogames_by_gender(session: AsyncSession, gender: str) -> List[Videogame]:
        """Busca registros por género"""
        result = await session.execute(
            select(Videogame).where(Videogame.videojuego.ilike(f"%{gender}%"))
        )
        return result.scalars().all()

    @staticmethod
    async def filter_by_age(session: AsyncSession, age: int) -> List[Videogame]:
        """Filtra videojuegos por edad específica"""
        try:
            result = await session.execute(
                select(Videogame).where(Videogame.age == age)
            )
            return result.scalars().all()
        except ValueError:
            return []

    @staticmethod
    async def search_videogame_by_field(session: AsyncSession, field: str, value: str) -> List[Videogame]:
        """Busca registros por cualquier campo especificado"""
        if not hasattr(Videogame, field):
            return []

        model_field = getattr(Videogame, field)

        try:
            if field in ['age', 'playing_hours', 'productive_time']:
                numeric_value = int(value)
                result = await session.execute(
                    select(Videogame).where(model_field == numeric_value)
                )
            else:
                # Búsqueda case-insensitive para campos de texto
                result = await session.execute(
                    select(Videogame).where(func.lower(model_field) == value.lower())
                )

            return result.scalars().all()
        except ValueError:
            return []