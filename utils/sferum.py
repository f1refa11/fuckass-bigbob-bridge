import logging
from pprint import pformat
import requests

import SferumAPI as ass
from pprint import pprint
import os
from dotenv import load_dotenv

from objects import config, database
from utils import sending

# load Sferum user token from .env
load_dotenv()
SFERUM_TOKEN = os.getenv("SFERUM_TOKEN")

# SferumAPI yuppie
api = ass.SferumAPI(remixdsid=SFERUM_TOKEN)

FETCH_HEADERS = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"

def check_groups():
    CFG = config.GET()
    if CFG.existing_groups != CFG.sferum_groups:
        differ = [gid for gid in CFG.sferum_groups if gid not in CFG.existing_groups]
        for gid in differ:
            reset_queue(gid)
            CFG.existing_groups.append(gid)
    config.SAVE(CFG)

async def get_last_messages():
    logging.info("Fetching all group messages")
    
    # fetch config and DB data
    CFG = config.GET()
    DB = database.GET()
    
    return_data = []
    
    for group in CFG.sferum_groups:
        # fetch last 200 messages(should be enough) bruh it maximum
        # TODO: `count` argument value as a config/const
        history = api.messages.get_history(peer_id=group, count=200, offset=0)
        
        try:
            logging.info(f"Sferum group ID: {group}")
            logging.info(f"Sferum group name: {history["response"]["conversations"][0]["chat_settings"]["title"]}")
        except KeyError:
            logging.error(f"Abnormal response from the server: {pformat(history)}")
            return
        
        # group chat PARTICIPANTS
        users_origin = history['response']['profiles']
        users = {user["id"]: f"{user['last_name']} {user['first_name']}" for user in users_origin}
        logging.debug(f"Users: {pformat(users)}")
        
        # group chat HISTORY
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
            
            attachmentsRaw = msg["attachments"] # bloated
            attachments = []
            for attachment in attachmentsRaw:
                match attachment["type"]:
                    case "photo":
                        # because we need to somehow insert the actual images, not URLs, we save them as temporary
                        # TODO: maybe make it as a separate module, like `tmpfiles.py`
                        # response = requests.get(
                        #     attachment["photo"]["orig_photo"]["url"], headers = {"user-agent": FETCH_HEADERS}
                        # )
                        #
                        #
                        # if response.status_code == 200:
                        #     with open("", 'wb') as f:
                        #         f.write(response.content)
                        attachments.append({
                            "type": "photo",
                            "url": attachment["photo"]["orig_photo"]["url"],
                        })
                    case "video":
                        attachments.append({
                            "type": "video",
                            "url_share": attachment["video"]["share_url"],
                            "url_player": attachment["video"]["player"],
                        })
                    case "doc":
                        attachments.append({
                            "type": "doc",
                            "url": attachment["doc"]["url"],
                            "url_private": attachment["doc"]["private_url"],
                        })
                    case "poll":
                        attachments.append({
                            "type": "poll",
                            "question": attachment["poll"]["question"],
                            "answers": [answer["text"] for answer in attachment["poll"]["answers"]],
                            "end_date": attachment["poll"]["end_date"]
                        })
                attachments.append(attachment)
            
            covered_messages.append({"msg_id": msg["conversation_message_id"], "text": msg["text"], "attachments": attachments, "author": users[msg["from_id"]]})
            sended_messages.append(msg["conversation_message_id"])   
        return_data.append({"group_id": group, "group_name": history["response"]["conversations"][0]["chat_settings"]["title"], "messages":covered_messages})
        DB[str(group)] = sended_messages
        database.SAVE(DB)

    await sending.sferum_messages(return_data)
    
def reset_queue(group_id: int = None):
    CFG = config.GET()
    DB = database.GET()
    
    if group_id:
        history = api.messages.get_history(peer_id=group_id, count=200, offset=0) 
        messages = history['response']['items']
        DB[str(group_id)] = list(range(messages[0]["conversation_message_id"]+1))
    else:
        for group in CFG.sferum_groups:
            history = api.messages.get_history(peer_id=group, count=200, offset=0) 
            messages = history['response']['items']
            DB[str(group)] = list(range(messages[0]["conversation_message_id"]+1))
            
    database.SAVE(DB)
    return "al gud"