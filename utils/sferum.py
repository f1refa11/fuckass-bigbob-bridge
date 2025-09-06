import SferumAPI as ass
from pprint import pprint
import os
from dotenv import load_dotenv

from objects import config, database
from utils import sending

load_dotenv()
SFERUM_TOKEN = os.getenv("SFERUM_TOKEN")

api = ass.SferumAPI(remixdsid=SFERUM_TOKEN) 

async def get_last_messages():
    print("gay sex")
    CFG = config.GET()
    DB = database.GET()
    
    return_data = []
    
    for group in CFG.sferum_groups:
        history = api.messages.get_history(peer_id=group, count=200, offset=0) 
        users_origin = history['response']['profiles']
        users = {uo["id"]: f"{uo['last_name']} {uo['first_name']}" for uo in users_origin}
        messages = history['response']['items']
        messages.reverse()
        sended_messages = DB[str(group)] if str(group) in DB.keys() else []
        smsg_set = set(sended_messages)
        filtered_msg = [msg for msg in messages if msg["conversation_message_id"] not in smsg_set and msg["from_id"] > 0]
        if len(filtered_msg) == 0:
            print("nothing")
            pass
        covered_messages = []
        for msg in filtered_msg:
            covered_messages.append({"msg_id": msg["conversation_message_id"], "text": msg["text"], "attachments": msg["attachments"], "author": users[msg["from_id"]]})
            sended_messages.append(msg["conversation_message_id"])   
        return_data.append({"group_id": group, "group_name": history["response"]["conversations"][0]["chat_settings"]["title"], "messages":covered_messages})
        DB[str(group)] = sended_messages
        database.SAVE(DB)

    await sending.sferum_messages(return_data)
    
async def get_last_message_id():
    return