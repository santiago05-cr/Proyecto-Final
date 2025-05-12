from typing import List, Optional
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from videogame import Videogame  # Asegúrate de que este modelo esté definido correctamente

class VideogameOperations:

    @staticmethod
    async def get_all(session: AsyncSession) -> List[Videogame]:
        result = await session.execute(select(Videogame))
        return result.scalars().all()

    @staticmethod
    async def get_by_id(session: AsyncSession, entry_id: int) -> Optional[Videogame]:
        return await session.get(Videogame, entry_id)

    @staticmethod
    async def create(session: AsyncSession, data: dict) -> Videogame:
        new_entry = Videogame(**data)
        session.add(new_entry)
        await session.commit()
        await session.refresh(new_entry)
        return new_entry

    @staticmethod
    async def update(session: AsyncSession, entry_id: int, update_data: dict) -> Optional[Videogame]:
        entry = await session.get(Videogame, entry_id)
        if not entry:
            return None
        for key, value in update_data.items():
            if hasattr(entry, key) and value is not None:
                setattr(entry, key, value)
        await session.commit()
        await session.refresh(entry)
        return entry

    @staticmethod
    async def delete(session: AsyncSession, entry_id: int) -> Optional[Videogame]:
        entry = await session.get(Videogame, entry_id)
        if not entry:
            return None
        await session.delete(entry)
        await session.commit()
        return entry

    @staticmethod
    async def search_by_age(session: AsyncSession, age: int) -> List[Videogame]:
        result = await session.execute(select(Videogame).where(Videogame.age == age))
        return result.scalars().all()

    @staticmethod
    async def filter_by_playing_hours(session: AsyncSession) -> List[Videogame]:
        result = await session.execute(select(Videogame))
        entries = result.scalars().all()
        return sorted(entries, key=lambda x: x.playing_hours)
