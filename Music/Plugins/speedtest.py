import os
import speedtest
import wget
from Music.MusicUtilities.helpers.gets import bytes
from Music import app, SUDOERS, BOT_ID
from pyrogram import filters, Client
from Music.MusicUtilities.database.onoff import (is_on_off, add_on, add_off)
from pyrogram.types import Message

@app.on_message(filters.command("السرعة") & ~filters.edited)
async def gstats(_, message):
    userid = message.from_user.id
    if await is_on_off(2):
        if userid in SUDOERS:
            pass
        else:
            return
    m = await message.reply_text("__بدء رفع ملفات السرعة 🧑‍💻__")
    try:
        test = speedtest.Speedtest()
        test.get_best_server()
        m = await m.edit("🧑‍💻 تحميل نتائج السرعة")
        test.download()
        m = await m.edit("🧑‍💻 تحميل ملفات السرعة")
        test.upload()
        test.results.share()
        result = test.results.dict()
    except Exception as e:
        await message.err(text=e)
        return 
    m = await m.edit("📲 ترتيب النتائج")
    path = wget.download(result["share"])
    output = f"""**📜 النتائج**
    
<u> **العميل:**</u>

**__مزود خدمة الإنترنت:__** {result['client']['isp']}
**__دولة:__** {result['client']['country']}
  
<u> **الخادم:**</u>

**__الاسم:__** {result['server']['name']}
**__دولة:__** {result['server']['country']}, {result['server']['cc']}
**__كفيل:__** {result['server']['sponsor']}
**__وقت الإستجابة:__** {result['server']['latency']}  

**__Ping:__** {result['ping']}"""
    msg = await app.send_photo(
        chat_id=message.chat.id, photo=path, caption=output
    )
    os.remove(path)
    await m.delete()
