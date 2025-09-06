import SferumAPI as ass
from pprint import pprint
import os
from dotenv import load_dotenv

from objects import config, database

load_dotenv()
SFERUM_TOKEN = os.getenv("SFERUM_TOKEN")

api = ass.SferumAPI(remixdsid=SFERUM_TOKEN) 

async def get_last_messages():
    print("gay sex")
    CFG = config.GET()
    DB = database.GET()
    
    return_data = []
    
    for group in CFG.sferum_groups:
        print(group)
        history = api.messages.get_history(peer_id=group, count=200, offset=0) 
        users_origin = history['response']['profiles']
        users = {uo["id"]: f"{uo['last_name']} {uo['first_name']}" for uo in users_origin}
        messages = history['response']['items']
        messages.reverse()
        last_message = DB[str(group)] if str(group) in DB.keys() else 0
        if messages[-1]["conversation_message_id"] > last_message:
            for_send = messages[last_message:]
            covered_msg = [{"msg_id": msg["conversation_message_id"], "text": msg["text"], "attachments": msg["attachments"], "author": users[msg["from_id"]]} for msg in for_send if msg["from_id"] > 0 ]
            return_data.append({"group_id": group, "group_name": history["response"]["conversations"][0]["chat_settings"]["title"], "messages":covered_msg})
            DB[str(group)] = messages[-1]["conversation_message_id"]
            database.SAVE(DB)
        else: pass
        
    pprint(return_data)