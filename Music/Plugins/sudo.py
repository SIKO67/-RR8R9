import os

from Music import OWNER, app
from Music.MusicUtilities.database.sudo import add_sudo, get_sudoers, remove_sudo
from pyrogram import filters
from pyrogram.types import Message


@app.on_message(filters.command("مطور") & filters.user(OWNER))
async def useradd(_, message: Message):
    if not message.reply_to_message:
        if len(message.command) != 2:
            await message.reply_text(
                "الرد على رسائل المستخدم أو تقديم اسم المستخدم."
            )
            return
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        message.from_user
        sudoers = await get_sudoers()
        if user.id in sudoers:
            return await message.reply_text("Sudah menjadi Pengguna Sudo.")
        added = await add_sudo(user.id)
        if added:
            await message.reply_text(
                f"تم رفع **{user.mention}** كـ مطور في البوت بنجاح"
            )
            return os.execvp("python3", ["python3", "-m", "Music"])
        await edit_or_reply(message, text="Terjadi kesalahan, periksa log.")
        return
    message.from_user.id
    user_id = message.reply_to_message.from_user.id
    mention = message.reply_to_message.from_user.mention
    sudoers = await get_sudoers()
    if user_id in sudoers:
        return await message.reply_text("بالفعل تم رفعة في قائمة المطورين.")
    added = await add_sudo(user_id)
    if added:
        await message.reply_text(f"تم اضافة **{mention}** الى قائمة المطورين")
        return os.execvp("python3", ["python3", "-m", "Music"])
    await edit_or_reply(message, text="Terjadi kesalahan, periksa log.")
    return


@app.on_message(filters.command("حذف") & filters.user(OWNER))
async def userdel(_, message: Message):
    if not message.reply_to_message:
        if len(message.command) != 2:
            await message.reply_text(
                "الرد على رسالة مستخدم أو تقديم اسم مستخدم."
            )
            return
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        message.from_user
        if user.id not in await get_sudoers():
            return await message.reply_text(f"بالفعل تم تنزيلة.")
        removed = await remove_sudo(user.id)
        if removed:
            await message.reply_text(f"تم حذف **{user.mention}** من المطورين.")
            return os.execvp("python3", ["python3", "-m", "Music"])
        await message.reply_text(f"حدث شيء خطأ.")
        return
    message.from_user.id
    user_id = message.reply_to_message.from_user.id
    mention = message.reply_to_message.from_user.mention
    if user_id not in await get_sudoers():
        return await message.reply_text(f"بالفعل تم حذفة.")
    removed = await remove_sudo(user_id)
    if removed:
        await message.reply_text(f"حذف **{mention}** من المطورين.")
        return os.execvp("python3", ["python3", "-m", "Music"])
    await message.reply_text(f"Something wrong happened.")


@app.on_message(filters.command("المطورين"))
async def sudoers_list(_, message: Message):
    sudoers = await get_sudoers()
    text = "**قائمة مطورين البوت 🧑‍💻 تم برمجة كل هذه العمل بواسطة @rr8r9**\n\n"
    for count, user_id in enumerate(sudoers, 1):
        try:
            user = await app.get_users(user_id)
            user = user.first_name if not user.mention else user.mention
        except Exception:
            continue
        text += f"• {user}\n"
    if not text:
        await message.reply_text("لايوجد مطورين ")
    else:
        await message.reply_text(text)
