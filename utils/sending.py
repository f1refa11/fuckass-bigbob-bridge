
from objects import bot, config

async def sferum_messages(data: dict):
    print("gay anal")
    print(data)
    for iteral in data:
        print("l")
        for msg in iteral["messages"]:
            print("m")
            text = f'''
Новое сообщение📩
Группа "{iteral['group_name']}" от {msg["author"]}
{msg['text']}
'''
            await send_message(text)
            
async def send_message(text: str):
    print('goofy ahh')
    CFG = config.GET()
    print(CFG)
    await bot.bot.send_message(chat_id=CFG.tg_chat_id, text=text)

