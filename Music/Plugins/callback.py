from pyrogram import Client, filters
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaPhoto,
    Message,
)
from asyncio import QueueEmpty
from pyrogram import Client, filters
from pytgcalls import StreamType
from pytgcalls.types.input_stream import InputAudioStream
from pytgcalls.types.input_stream import InputStream
from Music import app, BOT_USERNAME, dbb, SUDOERS
import os
import yt_dlp
from youtubesearchpython import VideosSearch
from Music.config import LOG_GROUP_ID
from Music.MusicUtilities.tgcallsrun import ASS_ACC
from os import path
import random
import time as sedtime 
import asyncio
import shutil
from time import time
from Music import converter
import aiohttp
from aiohttp import ClientResponseError, ServerTimeoutError, TooManyRedirects
from Music import dbb, app, BOT_USERNAME, BOT_ID, ASSID, ASSNAME, ASSUSERNAME, ASSMENTION
from Music.MusicUtilities.tgcallsrun import (music, convert, download, clear, get, is_empty, put, task_done, smexy)
from Music.MusicUtilities.helpers.decorators import errors
from Music.MusicUtilities.helpers.filters import command, other_filters
from Music.MusicUtilities.helpers.paste import paste
from Music.MusicUtilities.tgcallsrun import (music, clear, get, is_empty, put, task_done)
from Music.MusicUtilities.database.queue import (is_active_chat, add_active_chat, remove_active_chat, music_on, is_music_playing, music_off)
from Music.MusicUtilities.database.playlist import (get_playlist_count, _get_playlists, get_note_names, get_playlist, save_playlist, delete_playlist)
from Music.MusicUtilities.database.assistant import (_get_assistant, get_assistant, save_assistant)
from Music.MusicUtilities.helpers.inline import (play_keyboard, search_markup, play_markup, playlist_markup, audio_markup)
from Music.MusicUtilities.helpers.inline import play_keyboard, confirm_keyboard, play_list_keyboard, close_keyboard, confirm_group_keyboard
from Music.MusicUtilities.tgcallsrun import (music, convert, download, clear, get, is_empty, put, task_done, smexy)
from Music.MusicUtilities.database.queue import (is_active_chat, add_active_chat, remove_active_chat, music_on, is_music_playing, music_off)
from Music.MusicUtilities.database.onoff import (is_on_off, add_on, add_off)
from Music.MusicUtilities.database.blacklistchat import (blacklisted_chats, blacklist_chat, whitelist_chat)
from Music.MusicUtilities.database.gbanned import (get_gbans_count, is_gbanned_user, add_gban_user, add_gban_user)
from Music.MusicUtilities.database.theme import (_get_theme, get_theme, save_theme)
from Music.MusicUtilities.database.assistant import (_get_assistant, get_assistant, save_assistant)
from Music.config import DURATION_LIMIT, ASS_ID
from Music.MusicUtilities.helpers.decorators import errors
from Music.MusicUtilities.helpers.filters import command
from Music.MusicUtilities.helpers.gets import (get_url, themes, random_assistant, ass_det)
from Music.MusicUtilities.helpers.thumbnails import gen_thumb
from Music.MusicUtilities.helpers.chattitle import CHAT_TITLE
from Music.MusicUtilities.helpers.ytdl import ytdl_opts 
from Music.MusicUtilities.helpers.inline import (play_keyboard, search_markup, play_markup, playlist_markup)
import requests
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaPhoto,
    Message,
)
import re
import aiofiles
from pykeyboard import InlineKeyboard
from pyrogram import filters
from Music import aiohttpsession as session

pattern = re.compile(r"^text/|json$|yaml$|xml$|toml$|x-sh$|x-shellscript$")

flex = {}


async def isPreviewUp(preview: str) -> bool:
    for _ in range(7):
        try:
            async with session.head(preview, timeout=2) as resp:
                status = resp.status
                size = resp.content_length
        except asyncio.exceptions.TimeoutError:
            return False
        if status == 404 or (status == 200 and size == 0):
            await asyncio.sleep(0.4)
        else:
            return True if status == 200 else False
    return False


@Client.on_callback_query(filters.regex(pattern=r"ppcl"))
async def closesmex(_, CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    CallbackQuery.message.chat.id
    callback_request = callback_data.split(None, 1)[1]
    CallbackQuery.from_user.id
    try:
        smex, user_id = callback_request.split("|")
    except Exception as e:
        await CallbackQuery.message.edit(
            f"""
Terjadi kesalahan
Kemungkinan alasannya bisa** :{e}
"""
        )
        return
    if CallbackQuery.from_user.id != int(user_id):
        await CallbackQuery.answer(
            "متكدر تسوي هاي وخر؟", show_alert=True
        )
        return
    await CallbackQuery.message.delete()
    await CallbackQuery.answer()


@Client.on_callback_query(filters.regex("pausevc"))
async def pausevc(_, CallbackQuery):
    a = await app.get_chat_member(
        CallbackQuery.message.chat.id, CallbackQuery.from_user.id
    )
    if not a.can_manage_voice_chats:
        return await CallbackQuery.answer(
            "لازم عندك هاي الصلاحية حتى تكدر تستخدمها.\n• ❤️‍🔥 إدارة المحادثات الصوتية",
            show_alert=True,
        )
    CallbackQuery.from_user.first_name
    chat_id = CallbackQuery.message.chat.id
    if await is_active_chat(chat_id):
        if await is_music_playing(chat_id):
            await music.pytgcalls.pause_stream(chat_id)
            await music_off(chat_id)
            await CallbackQuery.answer("Voicechat Paused", show_alert=True)
            user_id = CallbackQuery.from_user.id
            user_name = CallbackQuery.from_user.first_name
            rpk = "[" + user_name + "](tg://user?id=" + str(user_id) + ")"
            await CallbackQuery.message.reply(
                f"🎧 تم إيقاف الأغنية مؤقتًا {rpk}!", reply_markup=play_keyboard
            )
            await CallbackQuery.message.delete()
        else:
            await CallbackQuery.answer(f"ماكو شي مشتغل!", show_alert=True)
            return
    else:
        await CallbackQuery.answer(f"ماكو شي مشتغل!", show_alert=True)


@Client.on_callback_query(filters.regex("اوكف"))
async def resumevc(_, CallbackQuery):
    a = await app.get_chat_member(
        CallbackQuery.message.chat.id, CallbackQuery.from_user.id
    )
    if not a.can_manage_voice_chats:
        return await CallbackQuery.answer(
            """
لازم عندك هاي الصلاحية حتى تكدر تستخدمها.

• ❤️‍🔥 إدارة المحادثات الصوتية
""",
            show_alert=True,
        )
    CallbackQuery.from_user.first_name
    chat_id = CallbackQuery.message.chat.id
    if await is_active_chat(chat_id):
        if await is_music_playing(chat_id):
            await CallbackQuery.answer(
                "ماكو شي مشتغل ،",
                show_alert=True,
            )
            return
        else:
            await music_on(chat_id)
            await music.pytgcalls.resume_stream(chat_id)
            await CallbackQuery.answer("Dilanjutkan", show_alert=True)
            user_id = CallbackQuery.from_user.id
            user_name = CallbackQuery.from_user.first_name
            rpk = "[" + user_name + "](tg://user?id=" + str(user_id) + ")"
            await CallbackQuery.message.reply(
                f"🎧 تم الاستمرار بواسطة {rpk}!", reply_markup=play_keyboard
            )
            await CallbackQuery.message.delete()
    else:
        await CallbackQuery.answer(f"ماكو شي مشتغل!", show_alert=True)


@Client.on_callback_query(filters.regex("تخ"))
async def skipvc(_, CallbackQuery):
    a = await app.get_chat_member(
        CallbackQuery.message.chat.id, CallbackQuery.from_user.id
    )
    if not a.can_manage_voice_chats:
        return await CallbackQuery.answer(
            """
لازم عندك هاي الصلاحية حتى تكدر تستخدمها

• ❤️‍🔥 إدارة المحادثات الصوتية
""",
            show_alert=True,
        )
    CallbackQuery.from_user.first_name
    chat_id = CallbackQuery.message.chat.id
    chat_title = CallbackQuery.message.chat.title
    if await is_active_chat(chat_id):
        task_done(chat_id)
        if is_empty(chat_id):
            user_id = CallbackQuery.from_user.id
            await remove_active_chat(chat_id)
            user_name = CallbackQuery.from_user.first_name
            rpk = "[" + user_name + "](tg://user?id=" + str(user_id) + ")"
            await remove_active_chat(chat_id)
            await CallbackQuery.answer()
            await CallbackQuery.message.reply(
                f"""
**زر التخطي المستخدم من قبل** {rpk}

لا مزيد من الأغاني في قائمة الانتظار

مغادرة الدردشة الصوتية
"""
            )
            await music.pytgcalls.leave_group_call(chat_id)
            return
        else:
            await CallbackQuery.answer("تخطي الدردشة الصوتية", show_alert=True)
            afk = get(chat_id)["file"]
            f1 = afk[0]
            f2 = afk[1]
            f3 = afk[2]
            finxx = f"{f1}{f2}{f3}"
            if str(finxx) != "raw":
                mystic = await CallbackQuery.message.reply(
                    """
يتم تشغيل الموسيقى في قائمة التشغيل ........

تنزيل الموسيقى التالية من قائمة التشغيل....
"""
                )
                url = f"https://www.youtube.com/watch?v={afk}"
                try:
                    with yt_dlp.YoutubeDL(ytdl_opts) as ytdl:
                        x = ytdl.extract_info(url, download=False)
                except Exception as e:
                    return await mystic.edit(
                        f"""
Gagal mengunduh video ini.

**Alasan**:{e}
"""
                    )
                title = x["title"]
                videoid = afk

                def my_hook(d):
                    if d["status"] == "downloading":
                        percentage = d["_percent_str"]
                        per = (str(percentage)).replace(".", "", 1).replace("%", "", 1)
                        per = int(per)
                        eta = d["eta"]
                        speed = d["_speed_str"]
                        size = d["_total_bytes_str"]
                        bytesx = d["total_bytes"]
                        if str(bytesx) in flex:
                            pass
                        else:
                            flex[str(bytesx)] = 1
                        if flex[str(bytesx)] == 1:
                            flex[str(bytesx)] += 1
                            sedtime.sleep(1)
                            mystic.edit(
                                f"تحميل {title[:50]}\n\n**حجم الملف:** {size}\n**تحميل:** {percentage}\n**السرعة:** {speed}\n**و:** {eta} ثانية"
                            )
                        if per > 500:
                            if flex[str(bytesx)] == 2:
                                flex[str(bytesx)] += 1
                                sedtime.sleep(0.5)
                                mystic.edit(
                                    f"تحميل {title[:50]}...\n\n**حجم الملف:** {size}\n**تحميل:** {percentage}\n**السرعة:** {speed}\n**و:** {eta} ثانية"
                                )
                                print(
                                    f"[{videoid}] تحميل {percentage} بسرعة {speed} في {chat_title} | و: {eta} ثواني"
                                )
                        if per > 800:
                            if flex[str(bytesx)] == 3:
                                flex[str(bytesx)] += 1
                                sedtime.sleep(0.5)
                                mystic.edit(
                                    f"تحميل {title[:50]}....\n\n**حجم الملف:** {size}\n**تحميل:** {percentage}\n**السرعة:** {speed}\n**و:** {eta} ثانية"
                                )
                                print(
                                    f"[{videoid}] تحميل {percentage} بسرعة {speed} في {chat_title} | و: {eta} ثواني"
                                )
                        if per == 1000:
                            if flex[str(bytesx)] == 4:
                                flex[str(bytesx)] = 1
                                sedtime.sleep(0.5)
                                mystic.edit(
                                    f"تحميل {title[:50]}.....\n\n**حجم الملف:** {size}\n**تحميل:** {percentage}\n**السرعة:** {speed}\n**و:** {eta} ثانية"
                                )
                                print(
                                    f"[{videoid}] تحميل {percentage} بسرعة {speed} في {chat_title} | و: {eta} ثواني"
                                )

                loop = asyncio.get_event_loop()
                xx = await loop.run_in_executor(None, download, url, my_hook)
                file = await convert(xx)
                await music.pytgcalls.change_stream(
                    chat_id,
                    InputStream(
                        InputAudioStream(
                            file,
                        ),
                    ),
                )
                thumbnail = x["thumbnail"]
                duration = x["duration"]
                duration = round(x["duration"] / 60)
                theme = random.choice(themes)
                ctitle = (await app.get_chat(chat_id)).title
                ctitle = await CHAT_TITLE(ctitle)
                f2 = open(f"search/{afk}id.txt", "r")
                userid = f2.read()
                thumb = await gen_thumb(thumbnail, title, userid, theme, ctitle)
                user_id = userid
                buttons = play_markup(videoid, user_id)
                await mystic.delete()
                semx = await app.get_users(userid)
                user_id = CallbackQuery.from_user.id
                user_name = CallbackQuery.from_user.first_name
                rpk = "[" + user_name + "](tg://user?id=" + str(user_id) + ")"
                await CallbackQuery.message.reply_photo(
                    photo=thumb,
                    reply_markup=InlineKeyboardMarkup(buttons),
                    caption=(
                        f"""
<b>⏭️ تخطي طلب الأغنية {rpk}</b>

<b>❤️‍🔥 الاسم: </b>[{title[:25]}]({url})
<b>❤️‍🔥 المدة: :</b> {duration}
<b>❤️‍🔥 طلب من:</b> {semx.mention}
"""
                    ),
                )
                os.remove(thumb)
            else:
                await music.pytgcalls.change_stream(
                    chat_id,
                    InputStream(
                        InputAudioStream(
                            afk,
                        ),
                    ),
                )
                _chat_ = (
                    (str(afk))
                    .replace("_", "", 1)
                    .replace("/", "", 1)
                    .replace(".", "", 1)
                )
                f2 = open(f"search/{_chat_}title.txt", "r")
                title = f2.read()
                f3 = open(f"search/{_chat_}duration.txt", "r")
                duration = f3.read()
                f4 = open(f"search/{_chat_}username.txt", "r")
                username = f4.read()
                f4 = open(f"search/{_chat_}videoid.txt", "r")
                videoid = f4.read()
                user_id = 1
                videoid = str(videoid)
                if videoid == "smex1":
                    buttons = audio_markup(videoid, user_id)
                else:
                    buttons = play_markup(videoid, user_id)
                user_id = CallbackQuery.from_user.id
                user_name = CallbackQuery.from_user.first_name
                rpk = "[" + user_name + "](tg://user?id=" + str(user_id) + ")"
                await CallbackQuery.message.reply_photo(
                    photo=f"downloads/{_chat_}final.png",
                    reply_markup=InlineKeyboardMarkup(buttons),
                    caption=f"""
<b>⏭️ تخطي طلب الأغنية: {rpk}</b>

<b>❤️‍🔥 الاسم:</b> {title}
<b>❤️‍🔥 المدة</b> {duration}
<b>❤️‍🔥 طلب من:</b> {username}
""",
                )
                return


@Client.on_callback_query(filters.regex("اوكف"))
async def stopvc(_, CallbackQuery):
    a = await app.get_chat_member(
        CallbackQuery.message.chat.id, CallbackQuery.from_user.id
    )
    if not a.can_manage_voice_chats:
        return await CallbackQuery.answer(
            "You don't have the required permission to perform this action.\nPermission: MANAGE VOICE CHATS",
            show_alert=True,
        )
    CallbackQuery.from_user.first_name
    chat_id = CallbackQuery.message.chat.id
    if await is_active_chat(chat_id):
        try:
            clear(chat_id)
        except QueueEmpty:
            pass
        try:
            await music.pytgcalls.leave_group_call(chat_id)
        except Exception:
            pass
        await remove_active_chat(chat_id)
        await CallbackQuery.answer("Dihentikan", show_alert=True)
        user_id = CallbackQuery.from_user.id
        user_name = CallbackQuery.from_user.first_name
        rpk = "[" + user_name + "](tg://user?id=" + str(user_id) + ")"
        await CallbackQuery.message.reply(f"🎧 تم الإيقاف بواسطة {rpk}!")
    else:
        await CallbackQuery.answer(f"ماكو شي مشتغل!", show_alert=True)

        
@Client.on_callback_query(filters.regex("play_playlist"))
async def play_playlist(_,CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    chat_id = CallbackQuery.message.chat.id
    callback_request = callback_data.split(None, 1)[1]
    userid = CallbackQuery.from_user.id 
    try:
        user_id,smex = callback_request.split("|") 
    except Exception as e:
        await CallbackQuery.answer()
        return await CallbackQuery.message.edit(f"Error Occured\n**Possible reason could be**:{e}")
    Name = CallbackQuery.from_user.first_name
    chat_title = CallbackQuery.message.chat.title
    if str(smex) == "personal":
        if CallbackQuery.from_user.id != int(user_id):
            return await CallbackQuery.answer("هذا ليس لك!  تشغيل غبي قائمة التشغيل الخاصة بك!", show_alert=True)
        _playlist = await get_note_names(userid)
        if not _playlist:
            return await CallbackQuery.answer(f"ليس لديك قائمة تشغيل على الخوادم.", show_alert=True)
        else:
            await CallbackQuery.message.delete()
            logger_text=f"""بدء قائمة التشغيل

الكروب :- {chat_title}
طلب من :- {Name}

تشغيل قائمة التشغيل الشخصية."""
            await ASS_ACC.send_message(LOG_GROUP_ID, f"{logger_text}", disable_web_page_preview=True)
            mystic = await CallbackQuery.message.reply_text(f"بدءا {Name}قائمة التشغيل الشخصية.\n\nطلب من:- {CallbackQuery.from_user.first_name}")   
            checking = f"[{CallbackQuery.from_user.first_name}](tg://user?id={userid})"
            msg = f"قائمة التشغيل في قائمة الانتظار:\n\n"
            j = 0
            for note in _playlist:
                _note = await get_playlist(CallbackQuery.from_user.id, note)
                title = _note["title"]
                videoid = _note["videoid"]
                url = (f"https://www.youtube.com/watch?v={videoid}")
                duration = _note["duration"]
                if await is_active_chat(chat_id):
                    position = await put(chat_id, file=videoid)
                    j += 1
                    msg += f"{j}- {title[:50]}\n"
                    msg += f"   Queued Position- {position}\n\n"
                    f20 = open(f'search/{videoid}id.txt', 'w')
                    f20.write(f"{user_id}") 
                    f20.close()
                else:
                    try:
                        with yt_dlp.YoutubeDL(ytdl_opts) as ytdl:
                            x = ytdl.extract_info(url, download=False)
                    except Exception as e:
                        return await mystic.edit(f"Failed to download this video.\n\n**Reason**:{e}") 
                    title = (x["title"])
                    thumbnail = (x["thumbnail"])
                    def my_hook(d): 
                        if d['status'] == 'downloading':
                            percentage = d['_percent_str']
                            per = (str(percentage)).replace(".","", 1).replace("%","", 1)
                            per = int(per)
                            eta = d['eta']
                            speed = d['_speed_str']
                            size = d['_total_bytes_str']
                            bytesx = d['total_bytes']
                            if str(bytesx) in flex:
                                pass
                            else:
                                flex[str(bytesx)] = 1
                            if flex[str(bytesx)] == 1:
                                flex[str(bytesx)] += 1
                                try:
                                    if eta > 2:
                                        mystic.edit(f"تحميل {title[:50]}\n\n**حجم الملف:** {size}\n**تحميل:** {percentage}\n**السرعة:** {speed}\n**و:** {eta} ثانية")
                                except Exception as e:
                                    pass
                            if per > 250:    
                                if flex[str(bytesx)] == 2:
                                    flex[str(bytesx)] += 1
                                    if eta > 2:     
                                        mystic.edit(f"تحميل {title[:50]}..\n\n**حجم الملف:** {size}\n**تحميل:** {percentage}\n**السرعة:** {speed}\n**و:** {eta} ثانية")
                                    print(f"[{videoid}] تحميل {percentage} بسرعة {speed} | ETA: {eta} ثواني")
                            if per > 500:    
                                if flex[str(bytesx)] == 3:
                                    flex[str(bytesx)] += 1
                                    if eta > 2:     
                                        mystic.edit(f"تحميل {title[:50]}...\n\n**FileSize:** {size}\n**تحميل:** {percentage}\n**السرعة:** {speed}\n**و:** {eta} ثانية")
                                    print(f"[{videoid}] تحميل {percentage} بسرعة {speed} | و: {eta} ثواني")
                            if per > 800:    
                                if flex[str(bytesx)] == 4:
                                    flex[str(bytesx)] += 1
                                    if eta > 2:    
                                        mystic.edit(f"تحميل {title[:50]}....\n\n**FileSize:** {size}\n**تحميل:** {percentage}\n**السرعة:** {speed}\n**و:** {eta} ثانية")
                                    print(f"[{videoid}] تحميل {percentage} بسرعة {speed} | و: {eta} ثواني")
                        if d['status'] == 'finished': 
                            try:
                                taken = d['_elapsed_str']
                            except Exception as e:
                                taken = "00:00"
                            size = d['_total_bytes_str']
                            mystic.edit(f"**تحميل {title[:50]}.....**\n\n**حجم الملف:** {size}\n**الوقت المستغرق:** {taken} ثانية\n\n**تحويل الملف**[__جاري المعالجة__]")
                            print(f"[{videoid}] تحميل| اكتمل: {taken} ثواني")  
                    loop = asyncio.get_event_loop()
                    xx = await loop.run_in_executor(None, download, url, my_hook)
                    file = await convert(xx)
                    await music_on(chat_id)
                    await add_active_chat(chat_id)
                    await music.pytgcalls.join_group_call(
                        chat_id, 
                        InputStream(
                            InputAudioStream(
                                file,
                            ),
                        ),
                        stream_type=StreamType().local_stream,
                    )
                    theme = random.choice(themes)
                    ctitle = CallbackQuery.message.chat.title
                    ctitle = await CHAT_TITLE(ctitle)
                    thumb = await gen_thumb(thumbnail, title, userid, theme, ctitle)  
                    buttons = play_markup(videoid, user_id)
                    m = await CallbackQuery.message.reply_photo(
                    photo=thumb,
                    reply_markup=InlineKeyboardMarkup(buttons),    
                    caption=(f"🎥<b>__تم التشغيل:__ </b>[{title[:25]}]({url}) \n❤️‍🔥<b>__المدة:__</b> {duration} \n❤️‍🔥<b>__معلومات:__</b> [انقر هنا](https://t.me/{BOT_USERNAME}?start=info_{videoid})\n❤️‍🔥**__طلب من:__** {checking}")
                )   
                    os.remove(thumb)
                    await CallbackQuery.message.delete()
        await mystic.delete()
        m = await CallbackQuery.message.reply_text("لصق قائمة التشغيل في سلة المهملات")
        link = await paste(msg)
        preview = link + "/preview.png"
        urlxp = link + "/index.txt"
        a1 = InlineKeyboardButton(text=f"تسجيل الخروج قائمة التشغيل", url=urlxp)
        key = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="▷", callback_data=f'resumevc2'),
                    InlineKeyboardButton(text="II", callback_data=f'pausevc2'),
                    InlineKeyboardButton(text="‣‣I", callback_data=f'skipvc2'),
                    InlineKeyboardButton(text="▢", callback_data=f'stopvc2')
                ],
                [
                    a1,
                ],
                [
                    InlineKeyboardButton(text="مسح​", callback_data=f'close2')
                ]    
            ]
        )
        if await isPreviewUp(preview):
            try:
                await CallbackQuery.message.reply_photo(
                    photo=preview, caption=f"هذه قائمة تشغيل في قائمة الانتظار لـ {Name}.\n\nإذا كنت تريد حذف أي موسيقى من استخدام قائمة التشغيل : /ماسح", quote=False, reply_markup=key
                )
                await m.delete()
            except Exception:
                pass
        else:
            await CallbackQuery.message.reply_text(
                    text=msg, reply_markup=key
                )
            await m.delete()
    if str(smex) == "group":
        _playlist = await get_note_names(CallbackQuery.message.chat.id)
        if not _playlist:
            return await CallbackQuery.answer(f"لا تحتوي مجموعتك على قائمة تشغيل على الخوادم.  حاول إضافة موسيقى في قائمة التشغيل.", show_alert=True)
        else:
            await CallbackQuery.message.delete()
            logger_text=f"""بدء قائمة التشغيل

الكروب :- {chat_title}
طلب من :- {Name}

Group Playlist Playing."""
            await ASS_ACC.send_message(LOG_GROUP_ID, f"{logger_text}", disable_web_page_preview=True)
            mystic = await CallbackQuery.message.reply_text(f"بدء قائمة تشغيل المجموعات.\n\nطلب من:- {CallbackQuery.from_user.first_name}")   
            checking = f"[{CallbackQuery.from_user.first_name}](tg://user?id={userid})"
            msg = f"Queued Playlist:\n\n"
            j = 0
            for note in _playlist:
                _note = await get_playlist(CallbackQuery.message.chat.id, note)
                title = _note["title"]
                videoid = _note["videoid"]
                url = (f"https://www.youtube.com/watch?v={videoid}")
                duration = _note["duration"]
                if await is_active_chat(chat_id):
                    position = await put(chat_id, file=videoid)
                    j += 1
                    msg += f"{j}- {title[:50]}\n"
                    msg += f"   Queued Position- {position}\n\n"
                    f20 = open(f'search/{videoid}id.txt', 'w')
                    f20.write(f"{user_id}") 
                    f20.close()
                else:
                    try:
                        with yt_dlp.YoutubeDL(ytdl_opts) as ytdl:
                            x = ytdl.extract_info(url, download=False)
                    except Exception as e:
                        return await mystic.edit(f"Failed to download this video.\n\n**Reason**:{e}") 
                    title = (x["title"])
                    thumbnail = (x["thumbnail"])
                    def my_hook(d): 
                        if d['status'] == 'downloading':
                            percentage = d['_percent_str']
                            per = (str(percentage)).replace(".","", 1).replace("%","", 1)
                            per = int(per)
                            eta = d['eta']
                            speed = d['_speed_str']
                            size = d['_total_bytes_str']
                            bytesx = d['total_bytes']
                            if str(bytesx) in flex:
                                pass
                            else:
                                flex[str(bytesx)] = 1
                            if flex[str(bytesx)] == 1:
                                flex[str(bytesx)] += 1
                                try:
                                    if eta > 2:
                                        mystic.edit(f"تحميل {title[:50]}\n\n**حجم الملف:** {size}\n**تحميل:** {percentage}\n**سرعة:** {speed}\n**و:** {eta} ثانية")
                                except Exception as e:
                                    pass
                            if per > 250:    
                                if flex[str(bytesx)] == 2:
                                    flex[str(bytesx)] += 1
                                    if eta > 2:     
                                        mystic.edit(f"تحميل {title[:50]}..\n\n**حجم الملف:** {size}\n**تحميل:** {percentage}\n**سرعة:** {speed}\n**و:** {eta} ثانية")
                                    print(f"[{videoid}] تحميل {percentage} بسرعة {speed} | و: {eta} ثواني")
                            if per > 500:    
                                if flex[str(bytesx)] == 3:
                                    flex[str(bytesx)] += 1
                                    if eta > 2:     
                                        mystic.edit(f"تحميل {title[:50]}...\n\n**حجم الملف:** {size}\n**تحميل:** {percentage}\n**سرعة:** {speed}\n**و:** {eta} ثانية")
                                    print(f"[{videoid}] تحميل {percentage} بسرعة {speed} | و: {eta} ثواني")
                            if per > 800:    
                                if flex[str(bytesx)] == 4:
                                    flex[str(bytesx)] += 1
                                    if eta > 2:    
                                        mystic.edit(f"تحميل {title[:50]}....\n\n**حجم الملف:** {size}\n**تحميل:** {percentage}\n**سرعة:** {speed}\n**و:** {eta} ثانية")
                                    print(f"[{videoid}] تحميل {percentage} بسرعة {speed} | و: {eta} ثواني")
                        if d['status'] == 'finished': 
                            try:
                                taken = d['_elapsed_str']
                            except Exception as e:
                                taken = "00:00"
                            size = d['_total_bytes_str']
                            mystic.edit(f"**📥 تحميل {title[:50]}.....**\n\n**📚 حجم الملف:** {size}\n**⚡ الوقت المستغرق:** {taken} sec\n\n**📑 تحويل ملف النقرات**")
                            print(f"[{videoid}] تحميل| انقضى: {taken} ثواني")  
                    loop = asyncio.get_event_loop()
                    xx = await loop.run_in_executor(None, download, url, my_hook)
                    file = await convert(xx)
                    await music_on(chat_id)
                    await add_active_chat(chat_id)
                    await music.pytgcalls.join_group_call(
                        chat_id, 
                        InputStream(
                            InputAudioStream(
                                file,
                            ),
                        ),
                        stream_type=StreamType().local_stream,
                    )
                    theme = random.choice(themes)
                    ctitle = CallbackQuery.message.chat.title
                    ctitle = await CHAT_TITLE(ctitle)
                    thumb = await gen_thumb(thumbnail, title, userid, theme, ctitle)
                    buttons = play_markup(videoid, user_id)
                    m = await CallbackQuery.message.reply_photo(
                    photo=thumb,
                    reply_markup=InlineKeyboardMarkup(buttons),    
                    caption=(f"🎥<b>__تم التشغيل:__ </b>[{title[:25]}]({url}) \n❤️‍🔥<b>__المدة:__</b> {duration} \n❤️‍🔥<b>__معلومات:__</b> [ انقر هنا ](https://t.me/{BOT_USERNAME}?start=info_{videoid})\n❤️‍🔥**__طلب من:__** {checking}")
                )   
                    os.remove(thumb)
                    await CallbackQuery.message.delete()
        await asyncio.sleep(1)
        await mystic.delete()
        m = await CallbackQuery.message.reply_text("لصق قائمة التشغيل في سلة المهملات")
        link = await paste(msg)
        preview = link + "/preview.png"
        urlxp = link + "/index.txt"
        a1 = InlineKeyboardButton(text=f"تسجيل الخروج قائمة التشغيل", url=urlxp)
        key = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="▷", callback_data=f'resumevc2'),
                    InlineKeyboardButton(text="II", callback_data=f'pausevc2'),
                    InlineKeyboardButton(text="‣‣I", callback_data=f'skipvc2'),
                    InlineKeyboardButton(text="▢", callback_data=f'stopvc2')
                ],
                [
                    a1,
                ],
                [
                    InlineKeyboardButton(text="مسح​", callback_data=f'close2')
                ]    
            ]
        )
        if await isPreviewUp(preview):
            try:
                await CallbackQuery.message.reply_photo(
                    photo=preview, caption=f"هذه قائمة التشغيل الخاصة بمجموعتك في قائمة الانتظار.\n\nإذا كنت تريد حذف أي موسيقى من استخدام قائمة التشغيل : /ماسح", quote=False, reply_markup=key
                )
                await m.delete()
            except Exception:
                pass
        else:
            await CallbackQuery.message.reply_text(
                    text=msg, reply_markup=key
                )
            await m.delete()
 
@Client.on_callback_query(filters.regex("group_playlist"))
async def group_playlist(_,CallbackQuery):
    await CallbackQuery.answer()
    a = await app.get_chat_member(CallbackQuery.message.chat.id , CallbackQuery.from_user.id)
    if not a.can_manage_voice_chats:
        return await CallbackQuery.answer("ليس لديك الإذن المطلوب لتنفيذ هذا الإجراء.\nالاذن: دردشة الفيديو", show_alert=True)
    callback_data = CallbackQuery.data.strip()
    chat_id = CallbackQuery.message.chat.id
    callback_request = callback_data.split(None, 1)[1]
    userid = CallbackQuery.from_user.id 
    try:
        url,smex= callback_request.split("|") 
    except Exception as e:
        return await CallbackQuery.message.edit(f"Error Occured\n**Possible reason could be**: {e}")
    Name = CallbackQuery.from_user.first_name
    _count = await get_note_names(chat_id)
    count = 0
    if not _count:
        sex = await CallbackQuery.message.reply_text("مرحبًا بك في ميزة قائمة تشغيل الموسيقى.\n\nجاري إنشاء قائمة التشغيل الخاصة بمجموعتك في قاعدة البيانات ... الرجاء الانتظار.")
        await asyncio.sleep(2)
        await sex.delete()
    else:
        for smex in _count:
            count += 1   
    count = int(count)
    if count == 30:
        return await CallbackQuery.message.reply_text("آسف!  يمكن أن يكون لديك 30 موسيقى فقط في قائمة التشغيل الجماعية.")
    try:
        url = (f"https://www.youtube.com/watch?v={url}")
        results = VideosSearch(url, limit=1)
        for result in results.result()["result"]:
            title = (result["title"])
            duration = (result["duration"])
            videoid = (result["id"])
    except Exception as e:
            return await CallbackQuery.message.reply_text(f"Some Error Occured.\n**Possible Reason:** {e}") 
    _check = await get_playlist(chat_id, videoid)
    title = title[:50]
    if _check:
         return await CallbackQuery.message.reply_text(f"{Name}, إنه موجود بالفعل في قائمة التشغيل!")   
    assis = {
        "videoid": videoid,
        "title": title,
        "duration": duration,
    }
    await save_playlist(chat_id, videoid, assis)
    Name = CallbackQuery.from_user.first_name
    return await CallbackQuery.message.reply_text(f"تمت الإضافة إلى قائمة تشغيل المجموعة بواسطة {Name}")
  

@Client.on_callback_query(filters.regex("الانتظار"))
async def pla_playylistt(_,CallbackQuery):
    await CallbackQuery.answer()
    callback_data = CallbackQuery.data.strip()
    chat_id = CallbackQuery.message.chat.id
    callback_request = callback_data.split(None, 1)[1]
    userid = CallbackQuery.from_user.id 
    try:
        url,smex= callback_request.split("|") 
    except Exception as e:
        return await CallbackQuery.message.edit(f"Error Occured\n**Possible reason could be**:{e}")
    Name = CallbackQuery.from_user.first_name
    _count = await get_note_names(userid)
    count = 0
    if not _count:
        sex = await CallbackQuery.message.reply_text("**مرحبًا بك في ميزة قائمة تشغيل الموسيقى.**\n\n**جاري إنشاء قائمة التشغيل الخاصة بك في قاعدة البيانات ... الرجاء الانتظار.**")
        await asyncio.sleep(2)
        await sex.delete()
    else:
        for smex in _count:
            count += 1   
    count = int(count)
    if count == 30:
        if userid in SUDOERS:
            pass
        else:
            return await CallbackQuery.message.reply_text("آسف!  يمكن أن يكون لديك 30 موسيقى فقط في قائمة التشغيل الجماعية.")
    try:
        url = (f"https://www.youtube.com/watch?v={url}")
        results = VideosSearch(url, limit=1)
        for result in results.result()["result"]:
            title = (result["title"])
            duration = (result["duration"])
            videoid = (result["id"])
    except Exception as e:
            return await CallbackQuery.message.reply_text(f"Some Error Occured.\n**Possible Reason:**{e}") 
    _check = await get_playlist(userid, videoid)
    if _check:
         return await CallbackQuery.message.reply_text(f"{Name}, إنه موجود بالفعل في قائمة التشغيل!") 
    title = title[:50]    
    assis = {
        "videoid": videoid,
        "title": title,
        "duration": duration,
    }
    await save_playlist(userid, videoid, assis)
    return await CallbackQuery.message.reply_text(f"تم الاضافة {Name}الى الانتظار")   
    
    

@Client.on_callback_query(filters.regex("P_list"))
async def P_list(_,CallbackQuery):
    _playlist = await get_note_names(CallbackQuery.from_user.id)
    if not _playlist:
        return await CallbackQuery.answer(f"ليس لديك قائمة تشغيل شخصية على الخوادم.  حاول إضافة الموسيقى في قائمة التشغيل.", show_alert=True)
    else:
        j = 0
        await CallbackQuery.answer()
        msg = f"Personal Playlist:\n\n"
        for note in _playlist:
            j += 1
            _note = await get_playlist(CallbackQuery.from_user.id, note)
            title = _note["title"]
            duration = _note["duration"]
            msg += f"{j}- {title[:60]}\n"
            msg += f"    Duration- {duration} Min(s)\n\n"   
        await CallbackQuery.answer()
        await CallbackQuery.message.delete()     
        m = await CallbackQuery.message.reply_text("لصق قائمة التشغيل في سلة المهملات")
        link = await paste(msg)
        preview = link + "/preview.png"
        print(link)
        urlxp = link + "/index.txt"
        user_id = CallbackQuery.from_user.id
        user_name = CallbackQuery.from_user.first_name
        a2 = InlineKeyboardButton(text=f"لتشغيل {user_name[:17]}'في الانتضار", callback_data=f'play_playlist {user_id}|personal')
        a3 = InlineKeyboardButton(text=f"قائمة الانتضار", url=urlxp)
        key = InlineKeyboardMarkup(
            [
                [
                    a2,
                ],
                [
                    a3,
                    InlineKeyboardButton(text="قائمتي", callback_data=f'close2')
                ]    
            ]
        )
        if await isPreviewUp(preview):
            try:
                await CallbackQuery.message.reply_photo(
                    photo=preview, quote=False, reply_markup=key
                )
                await m.delete()
            except Exception as e :
                print(e)
                pass
        else:
            print("5")
            await CallbackQuery.message.reply_photo(
                    photo=link, quote=False, reply_markup=key
                )
            await m.delete()
    
    
@Client.on_callback_query(filters.regex("G_list"))
async def G_list(_,CallbackQuery):
    user_id = CallbackQuery.from_user.id
    _playlist = await get_note_names(CallbackQuery.message.chat.id)
    if not _playlist:
        return await CallbackQuery.answer(f"ليس لديك قائمة تشغيل جماعية على الخوادم.  حاول إضافة الموسيقى في قائمة التشغيل.", show_alert=True)
    else:
        await CallbackQuery.answer()
        j = 0
        msg = f"Group Playlist:\n\n"
        for note in _playlist:
            j += 1
            _note = await get_playlist(CallbackQuery.message.chat.id, note)
            title = _note["title"]
            duration = _note["duration"]
            msg += f"{j}- {title[:60]}\n"
            msg += f"    Duration- {duration} Min(s)\n\n"
        await CallbackQuery.answer()
        await CallbackQuery.message.delete()
        m = await CallbackQuery.message.reply_text("لصق قائمة التشغيل في سلة المهملات")
        link = await paste(msg)
        preview = link + "/preview.png"
        urlxp = link + "/index.txt"
        user_id = CallbackQuery.from_user.id
        user_name = CallbackQuery.from_user.first_name
        a1 = InlineKeyboardButton(text=f"قائمة تشغيل المجموعة", callback_data=f'play_playlist {user_id}|group')
        a3 = InlineKeyboardButton(text=f"قائمة الانتضار", url=urlxp)
        key = InlineKeyboardMarkup(
            [
                [
                    a1,
                ],
                [
                    a3,
                    InlineKeyboardButton(text="مسح", callback_data=f'close2')
                ]    
            ]
        )
        if await isPreviewUp(preview):
            try:
                await CallbackQuery.message.reply_photo(
                    photo=preview, quote=False, reply_markup=key
                )
                await m.delete()
            except Exception:
                pass
        else:
            await CallbackQuery.message.reply_photo(
                    photo=link, quote=False, reply_markup=key
                )
            await m.delete()
                       
        
@Client.on_callback_query(filters.regex("cbgroupdel"))
async def cbgroupdel(_,CallbackQuery):  
    a = await app.get_chat_member(CallbackQuery.message.chat.id , CallbackQuery.from_user.id)
    if not a.can_manage_voice_chats:
        return await CallbackQuery.answer("ماعندك هاي الصلاحية حتى تكدر تطفيها.\الصلاحية: المكالمات", show_alert=True)
    await CallbackQuery.message.delete() 
    await CallbackQuery.answer()
    _playlist = await get_note_names(CallbackQuery.message.chat.id)                                    
    if not _playlist:
        return await CallbackQuery.message.reply_text("لا تحتوي المجموعة على قائمة تشغيل على خادم الموسيقى")
    else:
        titlex = []
        for note in _playlist:
            await delete_playlist(CallbackQuery.message.chat.id, note)
    await CallbackQuery.message.reply_text("تم حذف قائمة التشغيل بأكملها الخاصة بمجموعتك بنجاح")  
    
    
@Client.on_callback_query(filters.regex("cbdel"))
async def delplcb(_,CallbackQuery): 
    await CallbackQuery.answer()
    await CallbackQuery.message.delete() 
    _playlist = await get_note_names(CallbackQuery.from_user.id)                                    
    if not _playlist:
        return await CallbackQuery.message.reply_text("ليس لديك قائمة تشغيل على خادم الموسيقى")
    else:
        titlex = []
        for note in _playlist:
            await delete_playlist(CallbackQuery.from_user.id, note)
    await CallbackQuery.message.reply_text("تم حذف قائمة التشغيل بالكامل بنجاح")
