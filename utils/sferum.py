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
    for group in CFG.sferum_groups:
        history = api.messages.get_history(peer_id=group, count=150, offset=0) 
        users_origin = history['response']['profiles']
        pprint(users_origin)
        users = {uo["id"]: f"{uo['last_name']} {uo['first_name']}" for uo in users_origin}
        messages = history['response']['items']
        messages.reverse()
        last_message = DB[str(group)] if str(group) in DB.keys() else 0
        if messages[-1]["conversation_message_id"] > last_message:
            for_send = messages[last_message:]
            pprint(for_send)
            covered_msg = [{"msg_id": msg["conversation_message_id"], "text": msg["text"], "attachments": msg["attachments"], "author": users[msg["from_id"]]} for msg in for_send]
            pprint(covered_msg)
    return None