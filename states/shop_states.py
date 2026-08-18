from aiogram.fsm.state import State, StatesGroup

class AddProduct(StatesGroup):
    photo = State()
    name = State()
    category = State()
    description = State()
    price = State()
    

class OrderProduct(StatesGroup):
    waiting_for_phone = State()