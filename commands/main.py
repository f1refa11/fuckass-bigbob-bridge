from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.filters import Command, CommandStart

from utils import sferum

router = Router()

@router.message(CommandStart())
async def start_handler(msg: Message):
    await msg.answer("go fuck yourself")
    await sferum.get_last_messages()
    