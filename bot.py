    import asyncio
    import logging
    from aiogram import Bot, Dispatcher
    from config import BOT_TOKEN 
    from database.models import create_tables
    from handlers.admin import admin_router
    from handlers.user import user_router


    logging.basicConfig(level = logging.INFO)

    BOT = Bot(BOT_TOKEN)
    dp = Dispatcher()

    async def main():
        await create_tables()
        
        dp.include_router(admin_router)
        dp.include_router(user_router)
        
        print("The bot has been succefully launched and ready for operation.")
        await dp.start_polling(BOT)
        
    if __name__ == "__main__":
        try:
            asyncio.run(main())
        except KeyboardInterrupt:
            print("The bot is turned off.")