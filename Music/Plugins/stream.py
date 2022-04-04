import asyncio
import os
from Music.MusicUtilities.tgcallsrun import ASS_ACC

from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant, UserNotParticipant
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pytgcalls import StreamType
from pytgcalls.types.input_stream import AudioVideoPiped
from pytgcalls.types.input_stream.quality import (
    HighQualityAudio,
    HighQualityVideo,
    LowQualityVideo,
    MediumQualityVideo,
)
from youtubesearchpython import VideosSearch
from Music.config import GROUP, CHANNEL
from Music import BOT_NAME, BOT_USERNAME, app
from Music.MusicUtilities.tgcallsrun.music import pytgcalls as call_py
from Music.MusicUtilities.helpers.filters import command
from Music.MusicUtilities.helpers.logger import LOG_CHAT
from Music.MusicUtilities.tgcallsrun.queues import (
    QUEUE,
    add_to_queue,
    clear_queue,
    get_queue,
)


def ytsearch(query):
    try:
        search = VideosSearch(query, limit=1).result()
        data = search["result"][0]
        songname = data["title"]
        url = data["link"]
        duration = data["duration"]
        thumbnail = f"https://i.ytimg.com/vi/{data['id']}/hqdefault.jpg"
        return [songname, url, duration, thumbnail]
    except Exception as e:
        print(e)
        return 0


async def ytdl(link):
    proc = await asyncio.create_subprocess_exec(
        "yt-dlp",
        "-g",
        "-f",
        "best[height<=?720][width<=?1280]",
        f"{link}",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    if stdout:
        return 1, stdout.decode().split("\n")[0]
    else:
        return 0, stderr.decode()



@app.on_message(command("فيديو") & filters.group)
async def vplay(c: Client, message: Message):
    replied = message.reply_to_message
    chat_id = message.chat.id
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    rpk = "[" + user_name + "](tg://user?id=" + str(user_id) + ")"
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("اغلاق", url=f"https://t.me/{GROUP}"),
                InlineKeyboardButton("القناة", url=f"https://t.me/{CHANNEL}"),
            ]
        ]
    )
    if message.sender_chat:
        return await message.reply_text(
            "Anda adalah **Admin Anonim!**\n\n» kembali ke akun pengguna dari hak admin."
        )
    try:
        aing = await c.get_me()
    except Exception as e:
        return await message.reply_text(f"error:\n\n{e}")
    a = await c.get_chat_member(chat_id, aing.id)
    if a.status != "administrator":
        await message.reply_text(
            f"""
🧑‍💻 ارفعني مشرف اول شي ، انطيني هذني الصلاحيات:

» 🧑‍💻 حذف رسائل
» 🧑‍💻 حظر المستخدمين
» 🧑‍💻 اضافة مستخدمين
» 🧑‍💻 إدارة الدردشة الصوتية

🧑‍💻 بواسطة المطور: [{BOT_NAME}](t.me/{BOT_USERNAME})
""",
            disable_web_page_preview=True,
        )
        return
    if not a.can_manage_voice_chats:
        await message.reply_text(
            f"""
🧑‍💻 انطيني هاي الصلاحية:

» 🧑‍💻 ادارة المكالمات

🧑‍💻 بواسطه المطور: [{BOT_NAME}](t.me/{BOT_USERNAME})
""",
            disable_web_page_preview=True,
        )
        return
    if not a.can_delete_messages:
        await message.reply_text(
            f"""
🧑‍💻 انطيني هاي الصلاحية:

» 🧑‍💻 حذف رسائل

🧑‍💻 بواسطة المطور: [{BOT_NAME}](t.me/{BOT_USERNAME})
""",
            disable_web_page_preview=True,
        )
        return
    if not a.can_invite_users:
        await message.reply_text(
            f"""
🧑‍💻 انطيني هاي الصلاحية:

» 🧑‍💻 أضافة مستخدمين

🧑‍💻 بواسطة المطور: [{BOT_NAME}](t.me/{BOT_USERNAME})
""",
            disable_web_page_preview=True,
        )
        return
    try:
        ubot = await ASS_ACC.get_me()
        b = await c.get_chat_member(chat_id, ubot.id)
        if b.status == "kicked":
            await message.reply_text(
                f"@{ubot.username} **محظور في المجموعة** {message.chat.title}\n\n» **إلغاء حظر المساعد أولاً إذا كنت تريد استخدام هذا البوت.**"
            )
            return
    except UserNotParticipant:
        if message.chat.username:
            try:
                await ASS_ACC.join_chat(message.chat.username)
            except Exception as e:
                await message.reply_text(
                    f"🧑‍💻 **@{ubot.username} فشل المساعد في الانضمام**\n\n**السبب**: `{e}`"
                )
                return
        else:
            try:
                invite_link = await message.chat.export_invite_link()
                if "+" in invite_link:
                    link_hash = (invite_link.replace("+", "")).split("t.me/")[1]
                await ASS_ACC.join_chat(f"https://t.me/joinchat/{link_hash}")
            except UserAlreadyParticipant:
                pass
            except Exception as e:
                return await message.reply_text(
                    f"🧑‍💻 **@{ubot.username} فشل المساعد في الانضمام**\n\n**السبب**: `{e}`"
                )

    if replied:
        if replied.video or replied.document:
            what = "Audio Searched"
            await LOG_CHAT(message, what)
            loser = await replied.reply(" **❤️‍🔥 يَتمَ اެݪتشغِيݪ اެلانِ...**")
            dl = await replied.download()
            link = replied.link
            if len(message.command) < 2:
                Q = 720
            else:
                pq = message.text.split(None, 1)[1]
                if pq == "720" or "480" or "360":
                    Q = int(pq)
                else:
                    Q = 720
                    await loser.edit(
                        "» **Hanya 720, 480, 360 yang diizinkan** \n💡 **Sekarang Streaming Video Dalam 720p**"
                    )
            try:
                if replied.video:
                    songname = replied.video.file_name[:70]
                elif replied.document:
                    songname = replied.document.file_name[:70]
            except BaseException:
                songname = "Video"

            if chat_id in QUEUE:
                pos = add_to_queue(chat_id, songname, dl, link, "Video", Q)
                await loser.delete()
                requester = f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
                await message.reply_photo(
                    photo="cache/IMG_20211230_211039_090.jpg",
                    caption=f"""
🧑‍💻 **تمت إضافة المسارات إلى قائمة الانتظار**

❤️‍🔥 **الاسم:** [{songname[:999]}]({link})
❤️‍🔥 **طلب من:** {requester}

#️⃣ **قائمة الانتضار** {pos}
""",
                    reply_markup=keyboard,
                )
            else:
                if Q == 720:
                    amaze = HighQualityVideo()
                elif Q == 480:
                    amaze = MediumQualityVideo()
                elif Q == 360:
                    amaze = LowQualityVideo()
                await call_py.join_group_call(
                    chat_id,
                    AudioVideoPiped(
                        dl,
                        HighQualityAudio(),
                        amaze,
                    ),
                    stream_type=StreamType().pulse_stream,
                )
                add_to_queue(chat_id, songname, dl, link, "Video", Q)
                await loser.delete()
                requester = f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
                await message.reply_photo(
                    photo="cache/IMG_20211230_211039_090.jpg",
                    caption=f"""
▶️ **تم التشغيل بنجاح**

❤️‍🔥 **الاسم:** [{songname[:999]}]({link})
❤️‍🔥 **طلب من:** {requester}

""",
                    reply_markup=keyboard,
                )

    else:
        if len(message.command) < 2:
            await message.reply(
                "» الرد على **مقطع فيديو** او **اعطاء اسم فيديو للبحث.**"
            )
        else:
            what = "Query Given"
            await LOG_CHAT(message, what)
            loser = await message.reply(" **❤️‍🔥 يَتمَ اެݪتشغِيݪ اެلانِ...**")
            query = message.text.split(None, 1)[1]
            search = ytsearch(query)
            Q = 480
            amaze = HighQualityVideo()
            if search == 0:
                await loser.edit("🧑‍💻 **بحثت ومالكيت شي.**")
            else:
                songname = search[0]
                url = search[1]
                duration = search[2]
                thumbnail = search[3]
                veez, ytlink = await ytdl(url)
                if veez == 0:
                    await loser.edit(f"❌ yt-dl masalah terdeteksi\n\n» `{ytlink}`")
                else:
                    if chat_id in QUEUE:
                        pos = add_to_queue(chat_id, songname, ytlink, url, "Video", Q)
                        await loser.delete()
                        requester = f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
                        await message.reply_photo(
                            photo="cache/IMG_20211230_211039_090.jpg",
                            caption=f"""
🧑‍💻 **تمت إضافة المسارات إلى قائمة الانتظار**

❤️‍🔥 **الاسم:** [{songname[:999]}]({url})
❤️‍🔥 **المدة:** {duration}
❤️‍🔥 **طلب من:** {requester}

#️⃣ **قائمة الانتضار** {pos}
""",
                            reply_markup=keyboard,
                        )
                    
                    else:
                        try:
                            await call_py.join_group_call(
                                chat_id,
                                AudioVideoPiped(
                                    ytlink,
                                    HighQualityAudio(),
                                    amaze,
                                ),
                                stream_type=StreamType().pulse_stream,
                            )
                            add_to_queue(chat_id, songname, ytlink, url, "Video", Q)
                            await loser.delete()
                            requester = f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
                            thumb ="cache/IMG_20211230_165039_159.jpg"
                            await message.reply_photo(
                                photo="cache/IMG_20211230_211039_090.jpg",
                                caption=f"""
▷ **بدء تشغيل الفيديو**

❤️‍🔥 **الاسم:** [{songname[:999]}]({url})
❤️‍🔥 **المدة:** {duration}
❤️‍🔥 **طلب من:** {requester}

""",
                                reply_markup=keyboard,
                            )
                        except Exception as ep:
                            await loser.delete()
                            await message.reply_text(f"Error: `{ep}`")


@app.on_message(command("انتضار") & filters.group)
async def playlist(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        chat_queue = get_queue(chat_id)
        if len(chat_queue) == 1:
            await m.delete()
            await m.reply(
                f"**🎧 الان يشغل:** \n[{chat_queue[0][0]}]({chat_queue[0][2]}) | `{chat_queue[0][3]}`",
                disable_web_page_preview=True,
            )
        else:
            QUE = f"**🎧 الان العب:** \n[{chat_queue[0][0]}]({chat_queue[0][2]}) | `{chat_queue[0][3]}` \n\n**⏯ قائمة الانتظار:**"
            l = len(chat_queue)
            for x in range(1, l):
                hmm = chat_queue[x][0]
                hmmm = chat_queue[x][2]
                hmmmm = chat_queue[x][3]
                QUE = QUE + "\n" + f"**#{x}** - [{hmm}]({hmmm}) | `{hmmmm}`\n"
            await m.reply(QUE, disable_web_page_preview=True)
    else:
        await m.reply("**🧑‍💻 لايوجد شيء قيد التشغيل**")
