import aiogram.client.session.aiohttp
import aiogram.client.telegram
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

import os
from dotenv import load_dotenv

# get TG bot token from .env
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

session = aiogram.client.session.aiohttp.AiohttpSession(
    api= aiogram.client.telegram.TelegramAPIServer.from_base('http://localhost:8081')
)

# main Bot instance
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML), session=session)

dp = Dispatcher(storage=MemoryStorage())