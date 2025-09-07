import logging

import aiogram.filters
import aiogram.types
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

from utils import sferum
from objects.bot import dp

router = Router()

@router.message(CommandStart())
async def start_handler(msg: Message):
    logging.info("Command: start")
    await msg.answer("go fuck yourself")
    await sferum.get_last_messages()
    
@dp.message(aiogram.filters.Command("reset"))
async def reser_queue(query: aiogram.types.CallbackQuery):
    logging.info("Command: reset")
    result = sferum.reset_queue()
    await query.answer(result)