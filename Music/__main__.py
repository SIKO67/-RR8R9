import asyncio
import time
import uvloop
import importlib
from pyrogram import Client
from Music.config import API_ID, API_HASH, BOT_TOKEN, MONGO_DB_URI, SUDO_USERS, LOG_GROUP_ID
from Music import BOT_NAME, ASSNAME, app, client
from Music.MusicUtilities.database.functions import clean_restart_stage
from Music.MusicUtilities.database.queue import (get_active_chats, remove_active_chat)
from Music.MusicUtilities.tgcallsrun import run
from pytgcalls import idle
from motor.motor_asyncio import AsyncIOMotorClient as MongoClient
import time

Client(
    ':Music:',
    API_ID,
    API_HASH,
    bot_token=BOT_TOKEN,
    plugins={'root': 'Music.Plugins'},
).start()


print(f"[INFO]: بواسطة مطور سورس فريدوم البوت يعمل {BOT_NAME}!")
print(f"[INFO]: بواسطة مطور سورس فريدوم المساعد يعمل {ASSNAME}!")



async def load_start():
    restart_data = await clean_restart_stage()
    if restart_data:
        print("[INFO]: إرسال حالة إعادة التشغيل")
        try:
            await app.edit_message_text(
                restart_data["chat_id"],
                restart_data["message_id"],
                "**🧑‍💻تم تحديث البوت بنجاح.**",
            )
        except Exception:
            pass
    served_chats = []
    try:
        chats = await get_active_chats()
        for chat in chats:
            served_chats.append(int(chat["chat_id"]))
    except Exception as e:
        print("Error came while clearing db")
    for served_chat in served_chats:
        try:
            await remove_active_chat(served_chat)                                         
        except Exception as e:
            print("Error came while clearing db")
            pass     
    await app.send_message(LOG_GROUP_ID, "🧑‍💻بواسطة المطور @rr8r9 البوت يعمل")
    await client.send_message(LOG_GROUP_ID, "🧑‍💻بواسطة المطور @rr8r9 البوت يعمل")
    #Kalau clone atau fork jangan di hapus ya tolol
    await client.join_chat("xl444")
    await client.join_chat("RR3R2")
    print("[INFO]: بدء البوت")
    
   
loop = asyncio.get_event_loop()
loop.run_until_complete(load_start())

run()
idle()
loop.close()

print("[LOG] بوت الإغلاق")
