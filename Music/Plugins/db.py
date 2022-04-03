import asyncio
from pyrogram import Client, filters
from pyrogram.types import Dialog, Chat, Message
from pyrogram.errors import UserAlreadyParticipant
from Music.config import OWNER_ID
from Music.MusicUtilities.tgcallsrun import ASS_ACC as USER


@Client.on_message(filters.command("اذاعة عام") & filters.user(OWNER_ID) & ~filters.edited)
async def gcast(_, message: Message):
    sent=0
    failed=0
    if message.from_user.id not in OWNER_ID:
        return
    else:
        wtf = await message.reply("اذاعة طارئة ، تم...")
        if not message.reply_to_message:
            await wtf.edit("رد على رسالة مو هيج")
            return
        lmao = message.reply_to_message.text
        async for dialog in USER.iter_dialogs():
            try:
                await USER.send_message(dialog.chat.id, lmao)
                sent = sent+1
                await wtf.edit(f"يجري الاذاعة \n\nمرسلة إلى: {sent} دردشة \nفشل الإرسال إلى: {failed} دردشة")
                await asyncio.sleep(0.7)
            except:
                failed=failed+1
                await wtf.edit(f"يجري الاذاعة \n\nمرسلة إلى: {sent} دردشة \nفشل الإرسال إلى: {failed} دردشة")
                await asyncio.sleep(0.7)

        await message.reply_text(f"تم الاذاعة عزيزي المطور 🧑‍💻 \n\nمرسلة إلى: {sent} دردشة \nفشل الإرسال إلى: {failed} دردشة")
