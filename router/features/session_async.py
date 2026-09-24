from sqlalchemy import Column, Integer

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import sessionmaker,declarative_base,DeclarativeBase

from fastapi import APIRouter, Depends
from debug.orm_app.sqlalchemy_full_app import User


route = APIRouter(prefix="/session",tags=["session"])

db_url = "mysql+aiomysql://geeker:geeker@localhost:3306/fastapi_tutor?charset=utf8mb4"

engine = create_async_engine(db_url)
async_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session


@route.get("/")
async def index(session: AsyncSession = Depends(get_db)):
    u1 = User(username='test session')
    session.add(u1)
    await session.commit()

