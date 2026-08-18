from database.models import async_session, Product
from sqlalchemy import select


async def add_product_db(name : str, category : str, description, price : float, photo_id : str):
    async with async_session() as session:
        product = Product(
            name = name,
            category = category,
            description = description,
            price = price,
            photo_id = photo_id
        )
        session.add(product)
        await session.commit()
        

async def get_products_by_category(category_name : str):
    async with async_session() as session:
        stmt = select(Product).where(Product.category == category_name)
        result = await session.scalars(stmt)
        return result.all()