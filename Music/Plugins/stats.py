import asyncio
import json
import logging
import platform
import re
import socket
import time
import uuid
from datetime import datetime
from sys import version as pyver

import psutil
from pyrogram import Client
from pyrogram import __version__ as pyrover
from pyrogram import filters
from pyrogram.types import Message
from pytgcalls import __version__ as pytover

from Music import (BOT_ID, BOT_NAME, SUDOERS, app, boottime)
from Music import client as userbot
from Music.MusicUtilities.database.gbanned import get_gbans_count
from Music.MusicUtilities.database.chats import get_served_chats
from Music.MusicUtilities.database.sudo import get_sudoers
from Music.MusicUtilities.helpers.inline import (stats1, stats2, stats3, stats4, stats5,
                          stats6)

from Music.MusicUtilities.database.ping import get_readable_time


async def bot_sys_stats():
    bot_uptime = int(time.time() - boottime)
    cpu = psutil.cpu_percent(interval=0.5)
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    stats = f"""
**مدة التشغيل:** {get_readable_time((bot_uptime))}
**وحدة المعالجة المركزية:** {cpu}%
**الرام:** {mem}%
**القرص: **{disk}%"""
    return stats


@app.on_message(filters.command("الاحصائيات") & ~filters.edited)
async def gstats(_, message):
    start = datetime.now()
    try:
        await message.delete()
    except:
        pass
    uptime = await bot_sys_stats()
    response = await message.reply_text("الحصول على الإحصائيات!"
    )
    end = datetime.now()
    resp = (end - start).microseconds / 1000
    smex = f"""
[•]<u>**احصائيات عامة**</u>

تم برمجة كل هذه العمل بواسطة سيدي @rr8r9
    
البنك: `⚡{resp} ميلي ثانية`
{uptime}
    """
    await response.edit_text(smex, reply_markup=stats1)
    return


@app.on_callback_query(
    filters.regex(
        pattern=r"^(sys_stats|sto_stats|bot_stats|Dashboard|mongo_stats|gen_stats|assis_stats|wait_stats)$"
    )
)
async def stats_markup(_, CallbackQuery):
    command = CallbackQuery.matches[0].group(1)
    if command == "sys_stats":
        await CallbackQuery.answer("الحصول على احصائيات النظام...", show_alert=True)
        sc = platform.system()
        arch = platform.machine()
        ram = (
            str(round(psutil.virtual_memory().total / (1024.0 ** 3))) + " GB"
        )
        bot_uptime = int(time.time() - boottime)
        uptime = f"{get_readable_time((bot_uptime))}"
        smex = f"""
[•]<u>**احصائيات النظام**</u>

**مدة التشغيل:** {uptime}
**نظام Proc:** Online
**برنامج:** {sc}
**البنية:** {arch}
**الرام:** {ram}
**نسخة السورس:** {pytover.__version__}
**عرض بايثون:** {pyver.split()[0]}
**عرض بيروجرام:** {pyrover}"""
        await CallbackQuery.edit_message_text(smex, reply_markup=stats2)
    if command == "sto_stats":
        await CallbackQuery.answer(
            "الحصول على إحصائيات التخزين...", show_alert=True
        )
        hdd = psutil.disk_usage("/")
        total = hdd.total / (1024.0 ** 3)
        total = str(total)
        used = hdd.used / (1024.0 ** 3)
        used = str(used)
        free = hdd.free / (1024.0 ** 3)
        free = str(free)
        smex = f"""
[•]<u>**احصائيات التخزين**</u>

**توفر التخزين:** {total[:4]} GiB 
**التخزين المستخدم:** {used[:4]} GiB
**التخزين المتبقي:** {free[:4]} GiB"""
        await CallbackQuery.edit_message_text(smex, reply_markup=stats3)
    if command == "bot_stats":
        await CallbackQuery.answer("الحصول على إحصائيات البوت...", show_alert=True)
        served_chats = []
        chats = await get_served_chats()
        for chat in chats:
            served_chats.append(int(chat["chat_id"]))
        blocked = await get_gbans_count()
        sudoers = await get_sudoers()
        modules_loaded = "20"
        j = 0
        for count, user_id in enumerate(sudoers, 0):
            try:
                user = await app.get_users(user_id)
                j += 1
            except Exception:
                continue
        smex = f"""
[•]<u>**احصائيات البوت**</u>

**الوحدات المحملة:** {modules_loaded}
**عدد المحظورين:** {blocked}
**عدد المطورين:** {j}
**عدد الكروبات:** {len(served_chats)}"""
        await CallbackQuery.edit_message_text(smex, reply_markup=stats4)
    if command == "assis_stats":
        await CallbackQuery.answer(
            "الحصول على إحصائيات المساعد...", show_alert=True
        )
        await CallbackQuery.edit_message_text(
            "الحصول على إحصائيات المساعد ...", reply_markup=stats6
        )
        groups_ub = channels_ub = bots_ub = privates_ub = total_ub = 0
        async for i in userbot.iter_dialogs():
            t = i.chat.type
            total_ub += 1
            if t in ["supergroup", "group"]:
                groups_ub += 1
            elif t == "channel":
                channels_ub += 1
            elif t == "bot":
                bots_ub += 1
            elif t == "private":
                privates_ub += 1

        smex = f"""
[•]<u>احصائيات المساعد</u>

**الحوارات:** {total_ub}
**الكروبات:** {groups_ub} 
**القنوات:** {channels_ub} 
**البوتات:** {bots_ub}
**المستخدمين:** {privates_ub}"""
        await CallbackQuery.edit_message_text(smex, reply_markup=stats5)
    if command == "gen_stats":
        start = datetime.now()
        uptime = await bot_sys_stats()
        await CallbackQuery.answer(
            "الحصول على الإحصائيات العامة...", show_alert=True
        )
        end = datetime.now()
        resp = (end - start).microseconds / 1000
        smex = f"""
[•]<u>احصائيات عامة</u>

**البنك:** `⚡{resp} ملي ثانية`
{uptime}"""
        await CallbackQuery.edit_message_text(smex, reply_markup=stats1)
    if command == "wait_stats":
        await CallbackQuery.answer()
