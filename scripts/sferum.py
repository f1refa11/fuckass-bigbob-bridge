import SferumAPI as ass
from pprint import pprint
import os
from dotenv import load_dotenv

from objects import config

load_dotenv()
SFERUM_TOKEN = os.getenv("SFERUM_TOKEN")

api = ass.SferumAPI(remixdsid=SFERUM_TOKEN) 

async def get_msg_history():
    print("gay sex")
    CFG = config.GET()
    for group in CFG.sferum_groups:
        history = api.messages.get_history(peer_id=group, count=150, offset=0) 
        messages = history['response']['items']
        print(messages)
    
    return None