import json
import logging
import os.path
import pprint
import random
import re
import string

import aiogram.types
import aiogram.utils.media_group
import requests
import yt_dlp
import glob

import requests
import shutil

def download_file(url, local_filename):
    # local_filename = url.split('/')[-1]
    with requests.get(url, stream=True) as r:
        with open(local_filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

    return local_filename

from objects import bot, config

async def sferum_messages(data: list):
    for iteral in data:
        for msg in iteral["messages"]:
            text = f'''
<b>Новое сообщение📩</b>
Группа "{iteral['group_name']}" от {msg["author"]}
---
{msg['text']}
---
'''
            
            CFG = config.GET()

            if msg["attachments"]:
                logging.info("We have attachments")
                media_group = aiogram.utils.media_group.MediaGroupBuilder(caption = text)
                doc_media_group = aiogram.utils.media_group.MediaGroupBuilder(caption = text)
                has_link_media = False
                we_have_documents = False
                we_have_media = False
                for attachment in msg["attachments"]:
                    logging.info(pprint.pformat(attachment))
                    match attachment["type"]:
                        case "photo":
                            we_have_media = True
                            randchars = string.ascii_letters + string.digits
                            artid = ''.join(random.choice(randchars) for _ in range(6))
                            media_group.add_photo(aiogram.types.URLInputFile(attachment["url"], filename=artid+".jpg"))
                        case "video":
                            we_have_media = True
                            randchars = string.ascii_letters + string.digits
                            artid = ''.join(random.choice(randchars) for _ in range(12))
                            if not os.path.exists("temp_video"):
                                os.mkdir("temp_video")
                            yt_dlp.std_headers["User-Agent"] = requests.utils.default_headers()["User-Agent"]
                            with yt_dlp.YoutubeDL({"outtmpl": f"temp_video/{artid}.%(ext)s", "http_headers": yt_dlp.std_headers}) as ydl:
                                info = ydl.download(attachment["url"])
                            media_group.add_video(aiogram.types.FSInputFile(f"temp_video/{artid}.mp4", filename = f"{artid}.mp4"))
                        case "doc":
                            we_have_documents = True
                            response = requests.get(attachment["url"])
                            # randchars = string.ascii_letters + string.digits
                            # filename = ''.join(random.choice(randchars) for _ in range(6))
                            # if 'content-disposition' in response.headers:
                            #     disposition = response.headers['content-disposition']
                            #     filenameRaw = re.findall("filename=(.+)", disposition)
                            #
                            #     # If filename was found, print it; otherwise, print a default.
                            #     if filenameRaw:
                            #         filename = filenameRaw[0]
                            filename = attachment["filename"]
                            if not "text/html" in response.headers["Content-type"]:
                                doc_media_group.add_document(aiogram.types.URLInputFile(attachment["url"], filename=filename))
                            else:
                                logging.info("Got HTML, regex-searching the URL...")
                                doc_link = re.search(r'href=\"https://(.*?)\"', response.text).group(1)
                                logging.info(f"The URL: {doc_link}")
                                # file_response = requests.get("https://"+doc_link)
                                if not os.path.exists("temp_doc"):
                                    os.mkdir("temp_doc")
                                # with open("temp_doc/"+filename, "wb") as f:
                                #     f.write(file_response.content)
                                logging.info(f"downloading https://{doc_link} as temp_doc/{filename}")
                                download_file("https://"+doc_link, f"temp_doc/{filename}")
                                doc_media_group.add_document(
                                    aiogram.types.FSInputFile("temp_doc/"+filename, filename = filename))
                print(we_have_media, we_have_documents)
                if we_have_media and not we_have_documents:
                    await bot.bot.send_media_group(chat_id = CFG.tg_chat_id, media = media_group.build())
                elif we_have_documents and not we_have_media:
                    await bot.bot.send_media_group(chat_id = CFG.tg_chat_id, media = doc_media_group.build())
                elif we_have_documents and we_have_media:
                    logging.debug("bober")
                    doc_media_group.caption = "Прикреплённые документы"
                    mediaID = await bot.bot.send_media_group(chat_id = CFG.tg_chat_id, media = media_group.build())
                    await bot.bot.send_media_group(chat_id = CFG.tg_chat_id, media = doc_media_group.build(), reply_to_message_id = mediaID[0].message_id)
                    for video in glob.glob("temp_video/*.mp4"):
                        logging.info(f"Deleting already uploaded video: {video}")
                        os.remove(video)
                    for file in glob.glob("temp_doc/*"):
                        logging.info(f"Deleting already uploaded file: {file}")
                        os.remove(file)
            else:
                await bot.bot.send_message(chat_id = CFG.tg_chat_id, text = text)
