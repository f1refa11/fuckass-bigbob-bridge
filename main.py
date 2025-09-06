import asyncio
import logging

from aiogram.types import BotCommand
from commands import routers_pack

from objects.bot import bot, dp
import sys

from datetime import datetime

async def main():
    print("=== === === BOT START === === ===")
    print(f"python version: {sys.version.split()[0]}")
    print(f"started at: {datetime.now()}")
    
    # command routers
    for rt in routers_pack():
        dp.include_router(rt)
    
    # commands list
    commands = [BotCommand(command="start", description='Перезагрузить бота')]
    
    # bot info
    botmy = await bot.get_me()
    print(f"bot username: {botmy.username}")
    
    await bot.delete_webhook(drop_pending_updates=True)
    
    # set commands from the list
    await bot.set_my_commands(commands=commands)
    
    # start the bot logic
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    logging.info("working!")

if __name__ == "__main__":
    # logging
    logging.basicConfig(level=logging.ERROR)
    
    asyncio.run(main())