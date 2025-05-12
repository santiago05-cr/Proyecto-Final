from typing import List, Optional
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from mental_health import MentalHealth

class MentalHealthOperations:

    @staticmethod
    async def get_all(session: AsyncSession) -> List[MentalHealth]:
        result = await session.execute(select(MentalHealth))
        return result.scalars().all()

    @staticmethod
    async def get_by_id(session: AsyncSession, entry_id: int) -> Optional[MentalHealth]:
        return await session.get(MentalHealth, entry_id)

    @staticmethod
    async def create(session: AsyncSession, data: dict) -> MentalHealth:
        new_entry = MentalHealth(**data)
        session.add(new_entry)
        await session.commit()
        await session.refresh(new_entry)
        return new_entry

    @staticmethod
    async def update(session: AsyncSession, entry_id: int, update_data: dict) -> Optional[MentalHealth]:
        entry = await session.get(MentalHealth, entry_id)
        if not entry:
            return None
        for key, value in update_data.items():
            if hasattr(entry, key) and value is not None:
                setattr(entry, key, value)
        await session.commit()
        await session.refresh(entry)
        return entry

    @staticmethod
    async def delete(session: AsyncSession, entry_id: int) -> Optional[MentalHealth]:
        entry = await session.get(MentalHealth, entry_id)
        if not entry:
            return None
        await session.delete(entry)
        await session.commit()
        return entry

    @staticmethod
    async def search_by_age(session: AsyncSession, age: int) -> List[MentalHealth]:
        result = await session.execute(select(MentalHealth).where(MentalHealth.age == age))
        return result.scalars().all()

    @staticmethod
    async def filter_by_mental_harm(session: AsyncSession) -> List[MentalHealth]:
        result = await session.execute(
            select(MentalHealth).where(MentalHealth.mental_harm.ilike("yes"))
        )
        return result.scalars().all()
