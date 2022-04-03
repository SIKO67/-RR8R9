from youtubesearchpython import VideosSearch
import os
from os import path
import random
import asyncio
import shutil
from time import time
import yt_dlp
from Music import converter
from pyrogram import Client
from pyrogram.types import Message
from pyrogram.types import Voice
from Music import (
    app, BOT_USERNAME,
    BOT_ID,
)
from Music.MusicUtilities.tgcallsrun import (
    music,
    convert,
    download,
    clear,
    get,
    is_empty,
    put,
    task_done,
    smexy,
)
from Music.MusicUtilities.database.queue import (
    is_active_chat,
    add_active_chat,
    remove_active_chat,
    music_on,
    is_music_playing,
    music_off,
)
from Music.MusicUtilities.database.onoff import (is_on_off, add_on, add_off)
from Music.MusicUtilities.database.blacklistchat import (
    blacklisted_chats,
    blacklist_chat,
    whitelist_chat,
)
from Music.MusicUtilities.database.gbanned import (
    get_gbans_count,
    is_gbanned_user,
    add_gban_user,
    add_gban_user,
)
from Music.MusicUtilities.database.playlist import (
    get_playlist_count,
    _get_playlists,
    get_note_names,
    get_playlist,
    save_playlist,
    delete_playlist,
)
from Music.MusicUtilities.helpers.inline import (
    play_keyboard,
    confirm_keyboard,
    play_list_keyboard,
    close_keyboard,
    confirm_group_keyboard,
)
from Music.MusicUtilities.database.theme import (
    _get_theme,
    get_theme,
    save_theme,
)
from Music.MusicUtilities.database.assistant import (
    _get_assistant,
    get_assistant,
    save_assistant,
)
from Music.config import DURATION_LIMIT, ASS_ID
from Music.MusicUtilities.helpers.decorators import errors
from Music.MusicUtilities.helpers.filters import command
from Music.MusicUtilities.helpers.gets import (
    get_url,
    themes,
    random_assistant,
)
from Music.MusicUtilities.helpers.thumbnails import gen_thumb
from Music.MusicUtilities.helpers.chattitle import CHAT_TITLE
from Music.MusicUtilities.helpers.ytdl import ytdl_opts 
from Music.MusicUtilities.helpers.inline import (
    play_keyboard,
    search_markup,
    play_markup,
    playlist_markup,
)
from pyrogram import filters
from typing import Union
from youtubesearchpython import VideosSearch
from pyrogram.types import Message, Audio, Voice
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaPhoto,
    Message,
)


options = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "all","16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30",]   


@app.on_message(filters.command("الانتضار"))
async def pause_cmd(_, message):
    thumb ="cache/IMG_20211230_211509_034.jpg"
    await message.reply_photo(
    photo=thumb, 
    caption=("**__ميزة قائمة تشغيل الاغاني__**\n\nحدد قائمة التشغيل, تريد التحقق!"),    
    reply_markup=play_list_keyboard) 
    return 


@app.on_message(filters.command("حذف الانتضار"))
async def pause_cmd(_, message):
    usage = ("الاستخدام:\n\n/حذف الانتضار [أرقام بين 1-30] ( لحذف موسيقى معينة في قائمة التشغيل )\n\nاو\n\n /حذف الانتضار الكل ( لحذف موسيقى معينة في قائمة التشغيل )")
    if len(message.command) < 2:
        return await message.reply_text(usage)
    name = message.text.split(None, 1)[1].strip()
    if not name:
        return await message.reply_text(usage)
    if name not in options:
        return await message.reply_text(usage)
    if len(message.text) == 18:
        return await message.reply_text(f"تأكيد!!\nأنت متأكد أنك تريد حذف قائمة التشغيل بأكملها?", reply_markup=confirm_keyboard)
    else:
         _playlist = await get_note_names(message.from_user.id)
    if not _playlist:
        await message.reply_text("ليس لديك قائمة تشغيل على خادم الاغاني")
    else:
        titlex = []
        j = 0
        count = int(name)
        for note in _playlist:
            j += 1
            _note = await get_playlist(message.from_user.id, note)
            if j == count:
                deleted = await delete_playlist(message.from_user.id, note)
                if deleted:
                    return await message.reply_text(f"**تم حذف ملف {count} تم حذف ملف**")
                else:
                    return await message.reply_text(f"**لا توجد مثل هذه الموسيقى المحفوظة في قائمة التشغيل.**")                                
        await message.reply_text("ليس لديك مثل هذه الموسيقى في قائمة التشغيل.")                             

        
@app.on_message(filters.command("delgroupplaylist"))
async def delgroupplaylist(_, message):
    a = await app.get_chat_member(message.chat.id , message.from_user.id)
    if not a.can_manage_voice_chats:
        return await message.reply_text("ليس لدي الإذن المطلوب لتنفيذ هذا الإجراء.\n**الاذن:** __دردشة الفيديو__")
    usage = ("الاستخدام:\n\n//ماسح [أرقام بين 1-30] ( لحذف موسيقى معينة في قائمة التشغيل )\n\nor\n\n /ماسح  ( لحذف قائمة التشغيل بأكملها )")
    if len(message.command) < 2:
        return await message.reply_text(usage)
    name = message.text.split(None, 1)[1].strip()
    if not name:
        return await message.reply_text(usage)
    if name not in options:
        return await message.reply_text(usage)
    if len(message.text) == 21:
        return await message.reply_text(f"تأكيد!!\nأنت متأكد أنك تريد حذف قائمة التشغيل بأكملها?", reply_markup=confirm_group_keyboard)
    else:
         _playlist = await get_note_names(message.chat.id)
    if not _playlist:
        await message.reply_text("لا تحتوي المجموعة على قائمة تشغيل على خادم الاغاني")
    else:
        titlex = []
        j = 0
        count = int(name)
        for note in _playlist:
            j += 1
            _note = await get_playlist(message.chat.id, note)
            if j == count:
                deleted = await delete_playlist(message.chat.id, note)
                if deleted:
                    return await message.reply_text(f"**تم حذف {count} من الاغاني**")
                else:
                    return await message.reply_text(f"**لا توجد مثل هذه الموسيقى المحفوظة في قائمة التشغيل الجماعية.**")                                
        await message.reply_text("ليس لديك مثل هذه الموسيقى في قائمة التشغيل الجماعية.")
