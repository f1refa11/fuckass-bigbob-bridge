import logging
from pprint import pformat
import requests

import SferumAPI as ass
from pprint import pprint
import os
from dotenv import load_dotenv

from objects import config, database

# load Sferum user token from .env
load_dotenv()
SFERUM_TOKEN = os.getenv("SFERUM_TOKEN")

# SferumAPI yuppie
api = ass.SferumAPI(remixdsid=SFERUM_TOKEN)

FETCH_HEADERS = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"

async def get_last_messages():
    logging.info("Fetching all group messages")
    
    # fetch config and DB data
    CFG = config.GET()
    DB = database.GET()
    
    return_data = []
    
    for group in CFG.sferum_groups:
        logging.info(f"Sferum group ID: {group}")
        
        # fetch last 200 messages(should be enough)
        # TODO: `count` argument value as a config/const
        history = api.messages.get_history(peer_id=group, count=200, offset=0)
        
        logging.info(f"Sferum group name: {history["response"]["conversations"][0]["chat_settings"]["title"]}")
        
        # group chat PARTICIPANTS
        users_origin = history['response']['profiles']
        users = {user["id"]: f"{user['last_name']} {user['first_name']}" for user in users_origin}
        logging.debug(f"Users: {pformat(users)}")
        
        # group chat HISTORY
        messages = history['response']['items']
        messages.reverse()
        # TODO: messages count `200` as a config/const
        logging.debug(f"Found last {len(messages)}/200 messages")
        
        # checking for new messages
        # we check if the ID of the last message is the same after some delay, and if it's not, process new messages
        last_message = DB[str(group)] if str(group) in DB.keys() else 0
        if messages[-1]["conversation_message_id"] > last_message:
            logging.info("Detected new messages")
            
            for_send = messages[last_message:]
            covered_msg = []
            for msg in for_send:
                if msg["from_send"] > 0:
                    subMsg = {
                            "msg_id": msg["conversation_message_id"],
                            "text": msg["text"],
                            "author": users[msg["from_id"]]
                    }
                    
                    logging.debug(f"Message ID {subMsg['msg_id']} by user {subMsg['author']}: \"{subMsg['text']}\"")
                    
                    # working with ATTACHMENTS
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
                    
                    logging.debug(f"Attachments: {pformat(attachments)}")
                    subMsg["attachments"] = attachments
                    covered_msg.append(subMsg)
            return_data.append({
                "group_id": group,
                "group_name": history["response"]["conversations"][0]["chat_settings"]["title"],
                "messages":covered_msg
            })
            DB[str(group)] = messages[-1]["conversation_message_id"]
            logging.info(f"Last message ID is now: {DB[str(group)]}")
            database.SAVE(DB)
            logging.debug("Database saved.")
        else:
            logging.info("No new messages.")
    
    return return_data