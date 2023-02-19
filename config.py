from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from db import Database


BOT_TOKEN = os.environment.get("BOT_TOKEN")
DB_FILE = 'db.sqlite3'

bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot=bot, storage=MemoryStorage())
db = Database(DB_FILE)


forbidden_chars = ['_', '@', '/', "\\", '-', '+']
