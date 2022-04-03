import asyncio

from Music import BOT_ID, OWNER, app
from Music.MusicUtilities.database.chats import get_served_chats
from Music.MusicUtilities.database.gbanned import (
    add_gban_user,
    is_gbanned_user,
    remove_gban_user,
)
from Music.MusicUtilities.database.sudo import get_sudoers
from pyrogram import filters
from pyrogram.errors import FloodWait


@app.on_message(filters.command("حظر عام") & filters.user(OWNER))
async def ban_globally(_, message):
    if not message.reply_to_message:
        if len(message.command) < 2:
            await message.reply_text("**الاستخدام:**\n/حظر [بالمعرف | بالأيدي]")
            return
        user = message.text.split(None, 2)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        from_user = message.from_user
        sudoers = await get_sudoers()
        if user.id == from_user.id:
            return await message.reply_text("تريد حظر نفسك ؟ اعتقد بأنك حمار?")
        elif user.id == BOT_ID:
            await message.reply_text("تريدني ان احظر نفسي؟ اذهب والعب بعيداً??")
        elif user.id in sudoers:
            await message.reply_text("هل تريدني حظر مطور؟ لايمكنني?")
        else:

            await add_gban_user(user.id)
            served_chats = []
            chats = await get_served_chats()
            for chat in chats:
                served_chats.append(int(chat["chat_id"]))
            m = await message.reply_text(
                f"""
**جاري الحظر {user.mention}**

الوقت: {len(served_chats)}
"""
            )
            number_of_chats = 0
            for sex in served_chats:
                try:
                    await app.kick_chat_member(sex, user.id)
                    number_of_chats += 1
                    await asyncio.sleep(1)
                except FloodWait as e:
                    await asyncio.sleep(int(e.x))
                except Exception:
                    pass
            ban_text = f"""
__**🧑‍💻حظر عام بواسطة احد المطورين**__
**الاسم:** {message.chat.title} [`{message.chat.id}`]
**معرف المطور:** {from_user.mention}
**مستخدمين محظورين:** {user.mention}
**معرف المستخدم المحظور:** `{user.id}`
**دردشة:** {number_of_chats}
"""
            try:
                await m.delete()
            except Exception:
                pass
            await message.reply_text(
                f"{ban_text}",
                disable_web_page_preview=True,
            )
        return
    from_user_id = message.from_user.id
    from_user_mention = message.from_user.mention
    user_id = message.reply_to_message.from_user.id
    mention = message.reply_to_message.from_user.mention
    sudoers = await get_sudoers()
    if user_id == from_user_id:
        await message.reply_text("تريد حظر نفسك ؟ انت حمار ?")
    elif user_id == BOT_ID:
        await message.reply_text("تريد ان احظر نفسي؟ اذهب والعب بعيداً??")
    elif user_id in sudoers:
        await message.reply_text("تريد حظر المطور بكل سهولة؟🧑‍💻")
    else:
        is_gbanned = await is_gbanned_user(user_id)
        if is_gbanned:
            await message.reply_text("بالفعل محظور 🧑‍💻.")
        else:
            await add_gban_user(user_id)
            served_chats = []
            chats = await get_served_chats()
            for chat in chats:
                served_chats.append(int(chat["chat_id"]))
            m = await message.reply_text(
                f"""
**Menginisialisasi Larangan Global pada {mention}**

Waktu yang diharapkan: {len(served_chats)}
"""
            )
            number_of_chats = 0
            for sex in served_chats:
                try:
                    await app.kick_chat_member(sex, user_id)
                    number_of_chats += 1
                    await asyncio.sleep(1)
                except FloodWait as e:
                    await asyncio.sleep(int(e.x))
                except Exception:
                    pass
            ban_text = f"""
__**🧑‍💻حظر عام بواسطة احد المطورين**__
**الاسم:** {message.chat.title} [`{message.chat.id}`]
**معرف المطور:** {from_user_mention}
**مستخدمين محظورين:** {mention}
**معرف مستخدم الدردشة:** `{user_id}`
**دردشة:** {number_of_chats}"""
            try:
                await m.delete()
            except Exception:
                pass
            await message.reply_text(
                f"{ban_text}",
                disable_web_page_preview=True,
            )
            return


@app.on_message(filters.command("مسح") & filters.user(OWNER))
async def unban_globally(_, message):
    if not message.reply_to_message:
        if len(message.command) != 2:
            await message.reply_text("**الاستخدام:**\n/الغاء حظر [بالمعرف | بالأيدي]")
            return
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        from_user = message.from_user
        sudoers = await get_sudoers()
        if user.id == from_user.id:
            await message.reply_text("تريد رفع الحظر عن نفسك اذهب والعب بعيداً?")
        elif user.id == BOT_ID:
            await message.reply_text("تريدني ان الغي الحظر عن نفسي ؟ انت اهبل؟??")
        elif user.id in sudoers:
            await message.reply_text("لايمكن ذالك.")
        else:
            is_gbanned = await is_gbanned_user(user.id)
            if not is_gbanned:
                await message.reply_text("هو بالفعل حر ، ليش تتنمر عليه?")
            else:
                await remove_gban_user(user.id)
                await message.reply_text(f"بالفعل تم الغاء حظرة 🧑‍💻!")
        return
    from_user_id = message.from_user.id
    user_id = message.reply_to_message.from_user.id
    message.reply_to_message.from_user.mention
    sudoers = await get_sudoers()
    if user_id == from_user_id:
        await message.reply_text("تريد رفع الحظر عن نفسك؟ العب بعيداً?")
    elif user_id == BOT_ID:
        await message.reply_text(
            "هل يجب علي إلغاء حظر نفسي؟."
        )
    elif user_id in sudoers:
        await message.reply_text("لا يمكن حظر / حظر مستخدمي المطور.")
    else:
        is_gbanned = await is_gbanned_user(user_id)
        if not is_gbanned:
            await message.reply_text("هو بالفعل حر ، ليش تتنمر عليه?")
        else:
            await remove_gban_user(user_id)
            await message.reply_text(f"بالفعل تم الغاء حظره!")


chat_watcher_group = 5


@app.on_message(group=chat_watcher_group)
async def chat_watcher_func(_, message):
    try:
        userid = message.from_user.id
    except Exception:
        return
    checking = f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
    if await is_gbanned_user(userid):
        try:
            await message.chat.kick_member(userid)
        except Exception:
            return
        await message.reply_text(
            f"""
{checking} secara global dilarang oleh Musik dan telah dikeluarkan dari obrolan.

**Kemungkinan Alasan:** Potensi Spammer dan Penyalahguna.
"""
        )
