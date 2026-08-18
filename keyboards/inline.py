from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

categories_kb = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(
                text = "🔋 Portable Chargers",
                callback_data = "cat_powerbanks"
            )
        ],
        [
            InlineKeyboardButton(
                text = "🎧 Headphones",
                callback_data = "cat_headphones"
            )
        ],
        [
            InlineKeyboardButton(
                text = "🔌 Cables & Chargers",
                callback_data = "cat_cables"
            )
        ],
        [
            InlineKeyboardButton(
                text = "⌚ Smartwatches",
                callback_data = "cat_smartwatches"
            )
        ]
    ]
)




main_menu_kb = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(
                text = "🛍️ Product Catalog",
                callback_data = "open_catalog"
            )
        ]
    ]
)


def get_product_kb(product_id : int, page : int, total : int) -> InlineKeyboardMarkup:
    buttons = []
    
    nav_row = []
    
    if page > 0:
        nav_row.append(InlineKeyboardButton(text = "◀️", callback_data = f"page_{page - 1}"))
        
    nav_row.append(InlineKeyboardButton(text = "🛒 Order", callback_data = f"buy_{product_id}"))
    
    if page < total - 1:
        nav_row.append(InlineKeyboardButton(text = "▶️", callback_data = f"page_{page + 1}"))
        
    buttons.append(nav_row)
    
    buttons.append([InlineKeyboardButton(text = "↩️", callback_data = "open_catalog")])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)    