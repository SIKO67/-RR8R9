import asyncio
import os
import shutil
import subprocess
from sys import version as pyver

from Music.config import get_queue
from pyrogram import Client, filters
from pyrogram.types import Message

from Music import SUDOERS, app, db_mem, userbot
from Music.MusicUtilities.database import get_active_chats, is_active_chat
from Music.MusicUtilities.helpers.checker import checker, checkerCB

from pyrogram.types import (InlineKeyboardMarkup, InputMediaPhoto, Message,
                            Voice)

loop = asyncio.get_event_loop()

____ = "اوامر المغادرة والانضمام"
__مساعدة__ = """
**ملحوظة:**
اوامر المطور فقط
/انضم مع ايدي الكروب]
- سينضم حساب المساعد للمجموعة.
/ترك مع ايدي الكروب
- المساعد سيترك المجموعة المعينة.
/اترك مع ايدي الكروب
- لمغادرة البوت من مجموعة معينة.
"""

@app.on_message(filters.command("queue"))
async def activevc(_, message: Message):
    global get_queue
    if await is_active_chat(message.chat.id):
        mystic = await message.reply_text("الرجاء الانتظار ... جاري الحصول على قائمة الانتظار..")
        dur_left = db_mem[message.chat.id]["left"]
        duration_min = db_mem[message.chat.id]["total"]
        got_queue = get_queue.get(message.chat.id)
        if not got_queue:
            await mystic.edit(f"لا شيء في قائمة الانتظار")
        fetched = []
        for get in got_queue:
            fetched.append(get)

        ### Results
        current_playing = fetched[0][0]
        user_name = fetched[0][1]

        msg = "**قائمة الانتظار**\n\n"
        msg += "**يشغل حاليا:**"
        msg += "\n▶️" + current_playing[:30]
        msg += f"\n   ╚طلب من:- {user_name}"
        msg += f"\n   ╚المدة:- متبقي `{dur_left}` بعيدا عن المكان `{duration_min}` دقيقة."
        fetched.pop(0)
        if fetched:
            msg += "\n\n"
            msg += "**التالي في قائمة الانتظار:**"
            for song in fetched:
                name = song[0][:30]
                usr = song[1]
                dur = song[2]
                msg += f"\n⏸️{name}"
                msg += f"\n   ╠المدة : {dur}"
                msg += f"\n   ╚طلب من : {usr}\n"
        if len(msg) > 4096:
            await mystic.delete()
            filename = "queue.txt"
            with open(filename, "w+", encoding="utf8") as out_file:
                out_file.write(str(msg.strip()))
            await message.reply_document(
                document=filename,
                caption=f"**انتاج:**\n\n`قائمة الانتظار`",
                quote=False,
            )
            os.remove(filename)
        else:
            await mystic.edit(msg)
    else:
        await message.reply_text(f"ليس في قائمة الانتظار")


@app.on_message(filters.command("المكالمات") & filters.user(SUDOERS))
async def activevc(_, message: Message):
    served_chats = []
    try:
        chats = await get_active_chats()
        for chat in chats:
            served_chats.append(int(chat["chat_id"]))
    except Exception as e:
        await message.reply_text(f"**Error:-** {e}")
    text = ""
    j = 0
    for x in served_chats:
        try:
            title = (await app.get_chat(x)).title
        except Exception:
            title = "Private Group"
        if (await app.get_chat(x)).username:
            user = (await app.get_chat(x)).username
            text += (
                f"<b>{j + 1}.</b>  [{title}](https://t.me/{user})[`{x}`]\n"
            )
        else:
            text += f"<b>{j + 1}. {title}</b> [`{x}`]\n"
        j += 1
    if not text:
        await message.reply_text("عزيزي المطور لاتوجد مكالمات نشطة🧑‍💻")
    else:
        await message.reply_text(
            f"**Active Voice Chats:-**\n\n{text}",
            disable_web_page_preview=True,
        )


@app.on_message(filters.command("انضم") & filters.user(SUDOERS))
async def basffy(_, message):
    if len(message.command) != 2:
        await message.reply_text(
            "**الاستخدام:**\n/انضم معرف الكروب او ايدي الكروب ، سينضم للدردشة"
        )
        return
    chat = message.text.split(None, 2)[1]
    try:
        await userbot.join_chat(chat)
    except Exception as e:
        await message.reply_text(f"Gagal\n**Kemungkinan alasannya bisa**:{e}")
        return
    await message.reply_text("ينضم.")


@app.on_message(filters.command("اترك") & filters.user(SUDOERS))
async def baaaf(_, message):
    if len(message.command) != 2:
        await message.reply_text(
            "**الاستخدام:**\n/اترك مع ايدي الدردشة لمغادرة البوت فقط"
        )
        return
    chat = message.text.split(None, 2)[1]
    try:
        await app.leave_chat(chat)
    except Exception as e:
        await message.reply_text(f"Gagal\n**Kemungkinan alasannya bisa**:{e}")
        print(e)
        return
    await message.reply_text("غادر الروبوت الدردشة بنجاح🧑‍💻")


@app.on_message(filters.command("ترك") & filters.user(SUDOERS))
async def baujaf(_, message):
    if len(message.command) != 2:
        await message.reply_text(
            "**الاستخدام:**\n/ترك مع ايدي الكروب"
        )
        return
    chat = message.text.split(None, 2)[1]
    try:
        await userbot.leave_chat(chat)
    except Exception as e:
        await message.reply_text(f"Gagal\n**Kemungkinan alasannya bisa**:{e}")
        return
    await message.reply_text("Keluar.")
