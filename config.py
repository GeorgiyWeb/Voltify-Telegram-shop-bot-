import os 
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))


if not BOT_TOKEN:
    raise ValueError("Error! BOT_TOKEN was not found in the .env file!")

if not ADMIN_ID:
    raise ValueError("Error! ADMIN_ID was not found in the .env file!")
