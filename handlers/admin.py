from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from config import ADMIN_ID
from states.shop_states import AddProduct
from keyboards.inline import categories_kb
from database.requests import add_product_db

admin_router = Router()



#start command

@admin_router.message(Command("start"), F.from_user.id == ADMIN_ID)
async def admin_start(message: types.Message, state: FSMContext):
    await state.clear()
    await state.set_state(AddProduct.photo)
    await message.answer("🧑‍💻 Admin Panel\n\nTo add a new gadget, please send its photo:")
    
    
#photo
@admin_router.message(AddProduct.photo, F.photo)
async def process_photo(message:types.Message, state:FSMContext):
    await state.update_data(photo_id=message.photo[-1].file_id)
    await state.set_state(AddProduct.name)
    await message.answer("✨ Perfect! Now enter the item name (for example, Portable Charger Anker 20000 mAh): ")
    
#name
@admin_router.message(AddProduct.name, F.text)
async def process_name(message:types.Message, state:FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(AddProduct.category)
    await message.answer("📖 Select the product category: ", reply_markup=categories_kb)
    
# category
@admin_router.callback_query(AddProduct.category, F.data.startswith("cat_"))
async def process_category(callback:types.CallbackQuery, state:FSMContext):
    category = callback.data.split("_")[1]
    await state.update_data(category=category)
    await state.set_state(AddProduct.description)
    await callback.message.answer("📝 Provide the description and technical specifications for the item: ")
    
# description
@admin_router.message(AddProduct.description, F.text)
async def process_description(message:types.Message, state:FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(AddProduct.price)
    await message.answer("💵 Set the item price in USD: ")

# price
@admin_router.message(AddProduct.price, F.text)
async def process_price(message:types.Message, state:FSMContext):
    try:
        price = float(message.text.replace(",", "."))
    
    except ValueError:
        await message.answer("❌ Invalid input. Please enter a numeric value for the price (e.g., 19.99).")
        return
    
    data = await state.get_data()
    
    await add_product_db(
        name = data["name"],
        category = data["category"],
        description = data["description"],
        price = price,
        photo_id = data["photo_id"]
    )
    
    await state.clear()
    await message.answer("🎉 Done! Product successfully added to the database.")
        
    

