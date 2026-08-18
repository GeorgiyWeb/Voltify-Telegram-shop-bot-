from sqlalchemy import BigInteger, String, Float 
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

engine = create_async_engine(url="sqlite+aiosqlite:///shop.db", echo=True)

async_session = async_sessionmaker(engine, expire_on_commit=False)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class Product(Base):
    __tablename__ = "products"
    
    id : Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str] = mapped_column(String(100))
    category : Mapped[str] = mapped_column(String(50))
    description : Mapped[str] = mapped_column(String(500))
    price : Mapped[float] = mapped_column(Float)
    photo_id : Mapped[str] = mapped_column(String(255))
    
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)