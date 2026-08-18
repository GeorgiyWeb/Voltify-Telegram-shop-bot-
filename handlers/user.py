from aiogram import Router, F, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from config import ADMIN_ID
from states.shop_states import OrderProduct
from keyboards.inline import main_menu_kb, categories_kb, get_product_kb
from database.requests import get_products_by_category

user_router = Router()

user_pages = {}


# start
@user_router.message(CommandStart())
async def start_cmd(message:types.Message):
    await message.answer(f"👋 Hi, {message.from_user.first_name}!\nWelcome to Voltify – your ultimate gadget & electronics shop. 🔋", reply_markup=main_menu_kb)
    

#catalog
@user_router.callback_query(F.data == "open_catalog") 
async def show_categories(callback: types.CallbackQuery):
    await callback.message.answer("Choose category: ", reply_markup = categories_kb)
    await callback.answer()

# Choosing category and showing the product
@user_router.callback_query(F.data.startswith("cat_"))
async def show_category_products(callback: types.CallbackQuery):
    category = callback.data.split("_")[1]
    products = await get_products_by_category(category)
    
    if not products:
        await callback.message.answer("📦 No products found in this category.")
        await callback.answer()
        return
    
    user_pages[callback.from_user.id] = {"category" : category, "page" : 0}
    await send_product_card(callback.message, products, 0)
    await callback.answer()
    
    
# pagination
@user_router.callback_query(F.data.startswith("page_"))
async def process_pagination(callback: types.CallbackQuery):
    page = int(callback.data.split("_")[1])
    user_data = user_pages.get(callback.from_user.id)

    if not user_data:
        await callback.message.answer("⏱️ Session expired. Please restart the catalog.")
        await callback.answer()
        return

    products = await get_products_by_category(user_data["category"])
    user_pages[callback.from_user.id]["page"] = page

    
    await callback.message.delete()
    await send_product_card(callback.message, products, page)
    await callback.answer()


async def send_product_card(message: types.Message, products: list, page: int):
    product = products[page]
    caption = (
        f"🎧 {product.name}\n\n"
        f"{product.description}\n\n"
        f"💵 Цена: {product.price} AZN"
    )
    kb = get_product_kb(product.id, page, len(products))
    await message.answer_photo(photo=product.photo_id, caption=caption, reply_markup=kb)

# ordering
@user_router.callback_query(F.data.startswith("buy_"))
async def start_order(callback: types.CallbackQuery, state: FSMContext):
    product_id = int(callback.data.split("_")[1])
    await state.update_data(product_id=product_id)
    await state.set_state(OrderProduct.waiting_for_phone)
    
    await callback.message.answer("📲 Please provide your phone number or Telegram @username (e.g., @username or +123456789):")
    await callback.answer()

# getting the nummber and sending the request to admin
@user_router.message(OrderProduct.waiting_for_phone, F.text)
async def process_phone(message: types.Message, state: FSMContext):
    phone = message.text
    data = await state.get_data()
    
    
    admin_text = (
        f"🚨 NEW ORDER! \n\n"
        f"👤 Customer: @{message.from_user.username or 'without_username'}\n"
        f"📞 Contact: {phone}\n"
        f"🆔 Product ID: {data.get('product_id')}"
    )
    
    await message.bot.send_message(chat_id=ADMIN_ID, text=admin_text)
    await state.clear()
    await message.answer("🎉 Order Placed! Thank you for your purchase. A manager will get in touch with you very soon.")
