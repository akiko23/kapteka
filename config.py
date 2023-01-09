from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from db import Database


BOT_TOKEN = "5971566944:AAEDyMrxplUhQkbl_-BG5Q5AW-i_l1uWkM0"
DB_FILE = 'db.sqlite3'

bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot=bot, storage=MemoryStorage())
db = Database(DB_FILE)


forbidden_chars = ['_', '@', '/', "\\", '-', '+']
