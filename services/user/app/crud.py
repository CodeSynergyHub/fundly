from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User
from app.auth import get_password_hash


async def get_user_by_username(db: AsyncSession, username: str):
    return await db.execute(
        select(User).filter(User.username == username)
    ).scalar_one_or_none()


async def create_user(db: AsyncSession, user_create):
    hashed_password = get_password_hash(user_create.password)
    user = User(
        username=user_create.username,
        email=user_create.email,
        hashed_password=hashed_password,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user
