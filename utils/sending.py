
from objects import bot, config

async def sferum_messages(data: dict):
    print("gay anal")
    print(data)
    for iteral in data:
        for msg in iteral["messages"]:
            text = f'''
<b>Новое сообщение📩</b>
Группа "{iteral['group_name']}" от {msg["author"]}
<=>
{msg['text']}
<=>
'''
            await send_message(text)
            
async def send_message(text: str):
    CFG = config.GET()
    await bot.bot.send_message(chat_id=CFG.tg_chat_id, text=text)

