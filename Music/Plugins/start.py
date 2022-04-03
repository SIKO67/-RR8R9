import asyncio
import yt_dlp
import psutil

from Music.config import GROUP, CHANNEL
from Music import (
    ASSID,
    BOT_ID,
    BOT_NAME,
    BOT_USERNAME,
    OWNER,
    SUDOERS,
    app,
)
from Music.MusicUtilities.database.chats import is_served_chat
from Music.MusicUtilities.database.queue import remove_active_chat
from Music.MusicUtilities.database.sudo import get_sudoers
from Music.MusicUtilities.database.assistant import (_get_assistant, get_as_names, get_assistant,
                        save_assistant)
from Music.MusicUtilities.database.auth import (_get_authusers, add_nonadmin_chat, delete_authuser,
                   get_authuser, get_authuser_count, get_authuser_names,
                   is_nonadmin_chat, remove_nonadmin_chat, save_authuser)
from Music.MusicUtilities.database.blacklistchat import blacklist_chat, blacklisted_chats, whitelist_chat
from Music.MusicUtilities.helpers.admins import ActualAdminCB
from Music.MusicUtilities.helpers.inline import personal_markup, setting_markup
from Music.MusicUtilities.helpers.inline import (custommarkup, dashmarkup, setting_markup,
                          start_pannel, usermarkup, volmarkup)
from Music.MusicUtilities.helpers.thumbnails import down_thumb
from Music.MusicUtilities.helpers.ytdl import ytdl_opts
from Music.MusicUtilities.tgcallsrun.music import pytgcalls
from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)


def start_pannel():
    buttons = [
        [
            InlineKeyboardButton(text="S᥆ᥙrᥴᥱ​", url=f"https://t.me/{GROUP}"),
            InlineKeyboardButton(text="قناެة اެلمَطۅࢪ", url=f"https://t.me/{CHANNEL}"),
        ],
        [
            InlineKeyboardButton("ძᥱ᥎ᥱᥣ᥆ρᥱr", url="https://telegra.ph/ҡʏʏ-ᴍᴇᴍ-ᴇx-01-21-2"),
        ],
        [
            InlineKeyboardButton("اެلمَطۅࢪ", url="https://github.com/muhammadrizky16/KyyMusic"),
        ],
    ]
    return (
        "🧑‍💻 **{BOT_NAME} اެطݪق بَۅت مَمكَن تشِۅٛفة بَاެݪتݪيجَࢪاެمَ ):**",
        buttons,
    )


pstart_markup = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                "➕ اެضِفَنِيَ اެݪىِ مَجَمَۅٛعَتَكَ ➕", url=f"https://t.me/{BOT_USERNAME}?startgroup=true"),
        ],
        [
            InlineKeyboardButton(text="ძᥱ᥎ᥱᥣ᥆ρᥱr​", url=f"https://t.me/{GROUP}"),
            InlineKeyboardButton("اެلمَطۅࢪ", url=f"https://t.me/{CHANNEL}"),
        ],
       
    ]
)
welcome_captcha_group = 2


@app.on_message(filters.new_chat_members, group=welcome_captcha_group)
async def welcome(_, message: Message):
    chat_id = message.chat.id
    for member in message.new_chat_members:
        try:
            if member.id in OWNER:
                return await message.reply_text(
                    f"💡 Pemilik Bot [{member.mention}] baru saja bergabung di grup ini."
                )
            if member.id in SUDOERS:
                return await message.reply_text(
                    f"💡 Admin Bot [{member.mention}] baru saja bergabung di grup ini."
                )
            if member.id == ASSID:
                await remove_active_chat(chat_id)
            if member.id == BOT_ID:
                out = start_pannel()
                await message.reply_text(
                    f"""
❤️‍🔥 **مَاެطۅݪ ضِفتني ، ݪتَنسىِ تَࢪفعَني حَبي**

❤️‍🔥 **بَعد ماެࢪفعَتنِي ، تَستَطيعَ اެسِتخداެمي عَن طَࢪيَق اݪاࢪ࣪اެࢪ اެدَنا**
""",
                    reply_markup=InlineKeyboardMarkup(out[1]),
                    disable_web_page_preview=True
                )
                return
        except BaseException:
            return


@Client.on_message(
    filters.group
    & filters.command(
        ["start", "help", f"start@{BOT_USERNAME}", f"help@{BOT_USERNAME}"]
    )
)
async def start(_, message: Message):
    chat_id = message.chat.id
    out = start_pannel()
    await message.reply_text(
        f"""
Terima kasih telah memasukkan saya di {message.chat.title}.
Musik itu hidup.

Untuk bantuan silahkan klik tombol dibawah.
""",
        reply_markup=InlineKeyboardMarkup(out[1]),
        disable_web_page_preview=True
    )
    return


@Client.on_message(filters.private & filters.incoming & filters.command("start"))
async def play(_, message: Message):
    if len(message.command) == 1:
        user_id = message.from_user.id
        user_name = message.from_user.first_name
        rpk = "[" + user_name + "](tg://user?id=" + str(user_id) + ")"
        await app.send_message(
            message.chat.id,
            text=f"""
**❤️‍🔥 هَݪاެ حَبَ {rpk}!

❤️‍🔥 اެطَݪق بَۅت مَمكَن تَشِۅفَة بَاެݪتݪيجَراެم ):

-› MᥲᎥꪀƚᥲᎥꪀᥱძ ხy -› ძᥱ᥎ᥱᥣ᥆ρᥱr 

""",
            parse_mode="markdown",
            reply_markup=pstart_markup,
            reply_to_message_id=message.message_id,
        )
    elif len(message.command) == 2:
        query = message.text.split(None, 1)[1]
        f1 = query[0]
        f2 = query[1]
        f3 = query[2]
        finxx = f"{f1}{f2}{f3}"
        if str(finxx) == "inf":
            query = (str(query)).replace("info_", "", 1)
            query = f"https://www.youtube.com/watch?v={query}"
            with yt_dlp.YoutubeDL(ytdl_opts) as ytdl:
                x = ytdl.extract_info(query, download=False)
            thumbnail = x["thumbnail"]
            searched_text = f"""
🔍 **Video Track Information**

❇️**Judul:** {x["title"]}

⏳ **Durasi:** {round(x["duration"] / 60)} Mins
👀 **Ditonton:** `{x["view_count"]}`
👍 **Suka:** `{x["like_count"]}`
👎 **Tidak suka:** `{x["dislike_count"]}`
⭐️ **Peringkat Rata-rata:** {x["average_rating"]}
🎥 **Nama channel:** {x["uploader"]}
📎 **Channel Link:** [Kunjungi Dari Sini]({x["channel_url"]})
🔗 **Link:** [Link]({x["webpage_url"]})
"""
            link = x["webpage_url"]
            buttons = personal_markup(link)
            userid = message.from_user.id
            thumb = await down_thumb(thumbnail, userid)
            await app.send_photo(
                message.chat.id,
                photo=thumb,
                caption=searched_text,
                parse_mode="markdown",
                reply_markup=InlineKeyboardMarkup(buttons),
            )
        if str(finxx) == "sud":
            sudoers = await get_sudoers()
            text = "**🧑‍💻 قِائمة اެݪمطۅࢪيَن .**\n\n"
            for count, user_id in enumerate(sudoers, 1):
                try:
                    user = await app.get_users(user_id)
                    user = user.first_name if not user.mention else user.mention
                except Exception:
                    continue
                text += f"- {user}\n"
            if not text:
                await message.reply_text("لايوجد مطورين عزيزي🧑‍💻")
            else:
                await message.reply_text(text)


@app.on_message(filters.command("الاعدادات") & filters.group)
async def settings(_, message: Message):
    c_id = message.chat.id
    _check = await get_assistant(c_id, "assistant")
    if not _check:
        assis = {
            "volume": 100,
        }
        await save_assistant(c_id, "assistant", assis)
        volume = 100
    else:
        volume = _check["volume"]
    text, buttons = setting_markup()
    await asyncio.gather(
        message.delete(),
        message.reply_text(f"{text}\n\n**الكروب:** {message.chat.title}\n**ايدي الكروب:** {message.chat.id}\n**مستوى الصوت:** {volume}%", reply_markup=InlineKeyboardMarkup(buttons)),
    )

@app.on_callback_query(filters.regex("okaybhai"))
async def okaybhai(_, CallbackQuery):
    await CallbackQuery.answer("العودة ...")
    out = start_pannel()
    await CallbackQuery.edit_message_text(
        text=f"شكرا شكرا لإضافتي {CallbackQuery.message.chat.title}.\n{BOT_NAME} متصل بالفعل.\n\nاذا تريد مساعدة راسل المطور.",
        reply_markup=InlineKeyboardMarkup(out[1]),
    )

@app.on_callback_query(filters.regex("settingm"))
async def settingm(_, CallbackQuery):
    await CallbackQuery.answer("اعدادات البوت ...")
    text, buttons = setting_markup()
    c_title = CallbackQuery.message.chat.title
    c_id = CallbackQuery.message.chat.id
    chat_id = CallbackQuery.message.chat.id
    _check = await get_assistant(c_id, "assistant")
    if not _check:
        assis = {
            "volume": 100,
        }
        await save_assistant(c_id, "assistant", assis)
        volume = 100
    else:
        volume = _check["volume"]
    await CallbackQuery.edit_message_text(
        text=f"{text}\n\n**الكروب:** {c_title}\n**ايدي الكروب:** {c_id}\n**مستوى الصوت:** {volume}%",
        reply_markup=InlineKeyboardMarkup(buttons),
    )

@app.on_callback_query(filters.regex("EVE"))
@ActualAdminCB
async def EVE(_, CallbackQuery):
    checking = CallbackQuery.from_user.username
    text, buttons = usermarkup()
    chat_id = CallbackQuery.message.chat.id
    is_non_admin = await is_nonadmin_chat(chat_id)
    if not is_non_admin:
        await CallbackQuery.answer("تم حفظ التغييرات")
        await add_nonadmin_chat(chat_id)
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\nيقوم المسؤولون بوضع الأوامر إلى **الجميع**\n\nالآن يمكن لأي شخص موجود في هذه المجموعة تخطي الموسيقى وإيقافها مؤقتًا واستئنافها وإيقافها.\n\nالتغييرات التي تم إجراؤها بواسطة @{checking}",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    else:
        await CallbackQuery.answer(
            "Commands Mode is Already Set To EVERYONE", show_alert=True
        )

@app.on_callback_query(filters.regex("AMS"))
@ActualAdminCB
async def AMS(_, CallbackQuery):
    checking = CallbackQuery.from_user.username
    text, buttons = usermarkup()
    chat_id = CallbackQuery.message.chat.id
    is_non_admin = await is_nonadmin_chat(chat_id)
    if not is_non_admin:
        await CallbackQuery.answer(
            "تم بالفعل تعيين وضع الأوامر على ادمنية فقط", show_alert=True
        )
    else:
        await CallbackQuery.answer("تم حفظ التغييرات")
        await remove_nonadmin_chat(chat_id)
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\nاضبط وضع الأوامر على **المشرفين**\n\nالآن يمكن للمشرفين الموجودين في هذه المجموعة فقط تخطي الموسيقى وإيقافها مؤقتًا واستئنافها وإيقافها.\n\nالتغييرات التي تم إجراؤها بواسطة @{checking}",
            reply_markup=InlineKeyboardMarkup(buttons),
        )


@app.on_callback_query(
    filters.regex(
        pattern=r"^(AQ|AV|AU|Dashboard|HV|LV|MV|HV|VAM|Custommarkup|PTEN|MTEN|PTF|MTF|PFZ|MFZ|USERLIST|UPT|CPT|RAT|DIT)$"
    )
)
async def start_markup_check(_, CallbackQuery):
    command = CallbackQuery.matches[0].group(1)
    c_title = CallbackQuery.message.chat.title
    c_id = CallbackQuery.message.chat.id
    chat_id = CallbackQuery.message.chat.id
    if command == "AQ":
        await CallbackQuery.answer("بالفعل في أفضل جودة", show_alert=True)
    if command == "AV":
        await CallbackQuery.answer("اعدادات البوت ...")
        text, buttons = volmarkup()
        _check = await get_assistant(c_id, "assistant")
        volume = _check["volume"]
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**الكروب:** {c_title}\n**ايدي الكروب:** {c_id}\n**مستوى الصوت:** {volume}%\n**جودة الصوت:** أفضل الافتراضي",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "AU":
        await CallbackQuery.answer("اعدادات البوت ...")
        text, buttons = usermarkup()
        is_non_admin = await is_nonadmin_chat(chat_id)
        if not is_non_admin:
            current = "المشرفون فقط"
        else:
            current = "Everyone"
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**الكروب:** {c_title}\n\nحاليًا من يمكنه الاستخدام {BOT_NAME}:- **{current}**\n\n** ما هذا?**\n\n**👥 الجميع :-**يمكن لأي شخص استخدامها {BOT_NAME}أوامر  (تخطي ، إيقاف مؤقت ، استئناف ، إلخ) الموجودة في هذه المجموعة.\n\n**🙍 المشرفون فقط :-**  يمكن فقط للمسؤولين والمستخدمين المعتمدين استخدام جميع أوامر {BOT_NAME}.",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "Dashboard":
        await CallbackQuery.answer("لوحة القيادة...")
        text, buttons = dashmarkup()
        _check = await get_assistant(c_id, "assistant")
        volume = _check["volume"]
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**الكروب:** {c_title}\n**ايدي الكروب:** {c_id}\n**مستوى الصوت:** {volume}%\n\nيفحص {BOT_NAME}'إحصائيات النظام في لوحة القيادة هنا!  سيتم إضافة المزيد من الوظائف قريبًا جدًا!  استمر في التحقق من قناة المطور.",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "Custommarkup":
        await CallbackQuery.answer("اعدادات البوت ...")
        text, buttons = custommarkup()
        _check = await get_assistant(c_id, "assistant")
        volume = _check["volume"]
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**الكروب:** {c_title}\n**ايدي الكروب:** {c_id}\n**مستوى الصوت:** {volume}%\n**جودة الصوت:** أفضل الافتراضي",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "LV":
        assis = {
            "volume": 25,
        }
        volume = 25
        try:
            await pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("ضبط تغييرات الصوت ...")
        except:
            return await CallbackQuery.answer("لا توجد مكالمة جماعية نشطة...")
        await save_assistant(c_id, "assistant", assis)
        text, buttons = volmarkup()
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**الكروب:** {c_title}\n**ايدي الكروب:** {c_id}\n**مستوى الصوت:** {volume}%\n**جودة الصوت:** أفضل الافتراضي",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "MV":
        assis = {
            "volume": 50,
        }
        volume = 50
        try:
            await pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("ضبط تغييرات الصوت ...")
        except:
            return await CallbackQuery.answer("لا توجد مكالمة جماعية نشطة...")
        await save_assistant(c_id, "assistant", assis)
        text, buttons = volmarkup()
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**الكروب:** {c_title}\n**ايدي الكروب:** {c_id}\n**مستوى الصوت:** {volume}%\n**جودة الصوت:** أفضل الافتراضي",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "HV":
        assis = {
            "volume": 100,
        }
        volume = 100
        try:
            await pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("ضبط تغييرات الصوت ...")
        except:
            return await CallbackQuery.answer("لا توجد مكالمة جماعية نشطة...")
        await save_assistant(c_id, "assistant", assis)
        text, buttons = volmarkup()
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**الكروب:** {c_title}\n**ايدي الكروب:** {c_id}\n**مستوى الصوت:** {volume}%\n**جودة الصوت:** أفضل الافتراضي",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    if command == "VAM":
        assis = {
            "volume": 200,
        }
        volume = 200
        try:
            await pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("ضبط تغييرات الصوت ...")
        except:
            return await CallbackQuery.answer("لا توجد مكالمة جماعية نشطة...")
        await save_assistant(c_id, "assistant", assis)
        text, buttons = volmarkup()
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**الكروب:** {c_title}\n**ايدي الكروب:** {c_id}\n**مستوى الصوت:** {volume}%\n**جودة الصوت:** أفضل الافتراضي",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "PTEN":
        _check = await get_assistant(c_id, "assistant")
        volume = _check["volume"]
        volume = volume + 10
        if int(volume) > 200:
            volume = 200
        if int(volume) < 10:
            volume = 10
        assis = {
            "volume": volume,
        }
        try:
            await pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("ضبط تغييرات الصوت ...")
        except:
            return await CallbackQuery.answer("لا توجد مكالمة جماعية نشطة...")
        await save_assistant(c_id, "assistant", assis)
        text, buttons = custommarkup()
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**الكروب:** {c_title}\n**ايدي الكروب:** {c_id}\n**مستوى الصوت:** {volume}%\n**جودة الصوت:** أفضل الافتراضي",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "MTEN":
        _check = await get_assistant(c_id, "assistant")
        volume = _check["volume"]
        volume = volume - 10
        if int(volume) > 200:
            volume = 200
        if int(volume) < 10:
            volume = 10
        assis = {
            "volume": volume,
        }
        try:
            await pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("ضبط تغييرات الصوت ...")
        except:
            return await CallbackQuery.answer("لا توجد مكالمة جماعية نشطة...")
        await save_assistant(c_id, "assistant", assis)
        text, buttons = custommarkup()
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**الكروب:** {c_title}\n**ايدي الكروب:** {c_id}\n**مستوى الصوت:** {volume}%\n**جودة الصوت:** أفضل الافتراضي",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "PTF":
        _check = await get_assistant(c_id, "assistant")
        volume = _check["volume"]
        volume = volume + 25
        if int(volume) > 200:
            volume = 200
        if int(volume) < 10:
            volume = 10
        assis = {
            "volume": volume,
        }
        try:
            await pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("ضبط تغييرات الصوت ...")
        except:
            return await CallbackQuery.answer("لا توجد مكالمة جماعية نشطة...")
        await save_assistant(c_id, "assistant", assis)
        text, buttons = custommarkup()
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**الكروب:** {c_title}\n**ايدي الكروب:** {c_id}\n**مستوى الصوت:** {volume}%\n**جودة الصوت:** أفضل الافتراضي",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "MTF":
        _check = await get_assistant(c_id, "assistant")
        volume = _check["volume"]
        volume = volume - 25
        if int(volume) > 200:
            volume = 200
        if int(volume) < 10:
            volume = 10
        assis = {
            "volume": volume,
        }
        try:
            await pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("ضبط تغييرات الصوت ...")
        except:
            return await CallbackQuery.answer("لا توجد مكالمة جماعية نشطة🧑‍💻...")
        await save_assistant(c_id, "assistant", assis)
        text, buttons = custommarkup()
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**الكروب:** {c_title}\n**ايدي الكروب:** {c_id}\n**مستوى الصوت:** {volume}%\n**جودة الصوت:** أفضل الافتراضي",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "PFZ":
        _check = await get_assistant(c_id, "assistant")
        volume = _check["volume"]
        volume = volume + 50
        if int(volume) > 200:
            volume = 200
        if int(volume) < 10:
            volume = 10
        assis = {
            "volume": volume,
        }
        try:
            await pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("Setting Audio Changes ...")
        except:
            return await CallbackQuery.answer("لا توجد مكالمة جماعية نشطة🧑‍💻...")
        await save_assistant(c_id, "assistant", assis)
        text, buttons = custommarkup()
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**الكروب:** {c_title}\n**ايدي الكروب:** {c_id}\n**مستوى الصوت:** {volume}%\n**جودة الصوت:** أفضل الافتراضي",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "MFZ":
        _check = await get_assistant(c_id, "assistant")
        volume = _check["volume"]
        volume = volume - 50
        if int(volume) > 200:
            volume = 200
        if int(volume) < 10:
            volume = 10
        assis = {
            "volume": volume,
        }
        try:
            await pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("ضبط تغييرات الصوت ...")
        except:
            return await CallbackQuery.answer("لا توجد مكالمة جماعية نشطة🧑‍💻...")
        await save_assistant(c_id, "assistant", assis)
        text, buttons = custommarkup()
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**الكروب:** {c_title}\n**ايدي الكروب:** {c_id}\n**مستوى الصوت:** {volume}%\n**افصل افتراضي:** جودة الصوت",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "USERLIST":
        await CallbackQuery.answer("المستخدمون المصدقون!")
        text, buttons = usermarkup()
        _playlist = await get_authuser_names(CallbackQuery.message.chat.id)
        if not _playlist:
            return await CallbackQuery.edit_message_text(
                text=f"{text}\n\nNo Authorized Users Found\n\nYou can allow any non-admin to use my admin commands by /auth and delete by using /unauth",
                reply_markup=InlineKeyboardMarkup(buttons),
            )
        else:
            j = 0
            await CallbackQuery.edit_message_text(
                "إحضار المستخدمين المصرح لهم ... الرجاء الانتظار"
            )
            msg = f"**قائمة المستخدمين المعتمدين[AUL]:**\n\n"
            for note in _playlist:
                _note = await get_authuser(
                    CallbackQuery.message.chat.id, note
                )
                user_id = _note["auth_user_id"]
                user_name = _note["auth_name"]
                admin_id = _note["admin_id"]
                admin_name = _note["admin_name"]
                try:
                    user = await app.get_users(user_id)
                    user = user.first_name
                    j += 1
                except Exception:
                    continue
                msg += f"{j}➤ {user}[`{user_id}`]\n"
                msg += f"    ┗ أضيفت من قبل:- {admin_name}[`{admin_id}`]\n\n"
            await CallbackQuery.edit_message_text(
                msg, reply_markup=InlineKeyboardMarkup(buttons)
            )
    if command == "UPT":
        bot_uptimee = int(time.time() - bot_start_time)
        Uptimeee = f"{get_readable_time((bot_uptimee))}"
        await CallbackQuery.answer(
            f"Bot's Uptime: {Uptimeee}", show_alert=True
        )
    if command == "CPT":
        cpue = psutil.cpu_percent(interval=0.5)
        await CallbackQuery.answer(
            f"استخدام وحدة المعالجة المركزية في Bot: {cpue}%", show_alert=True
        )
    if command == "RAT":
        meme = psutil.virtual_memory().percent
        await CallbackQuery.answer(
            f"استخدام ذاكرة الروبوت: {meme}%", show_alert=True
        )
    if command == "DIT":
        diske = psutil.disk_usage("/").percent
        await CallbackQuery.answer(
            f"إستخدام القرص: {diske}%", show_alert=True
        )
