import asyncio
import logging

from aiogram.types import BotCommand
from commands import routers_pack

from objects.bot import bot, dp
from utils import sferum
import sys

from datetime import datetime

import warnings

async def main():
    warnings.simplefilter("always")
    
    print("=== === === BOT START === === ===")
    print(f"python version: {sys.version.split()[0]}")
    print(f"started at: {datetime.now()}")
    for rt in routers_pack():
        dp.include_router(rt)
    
    commands = [BotCommand(command="start", description='Перезагрузить бота')]
    
    botmy = await bot.get_me()
    print(f"bot username: {botmy.username}")

    sferum.check_groups()

    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands=commands)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == "__main__":
    logging.basicConfig(level=logging.ERROR)
    asyncio.run(main())