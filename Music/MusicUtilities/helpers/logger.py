from Music.config import LOG_GROUP_ID
from Music import app


async def LOG_CHAT(message, what):
    if message.chat.username:
        chatusername = (f"@{message.chat.username}")
    else:
        chatusername = ("مجموعة خاصة")
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    mention = "["+user_name+"](tg://user?id="+str(user_id)+")" 
    logger_text = f"""
__** 🧑‍💻 عزيزي المطور قام احد بتشغيل البوت ،اليك المعلومات {what}**__

**🧑‍💻الدردشة:** {message.chat.title} [`{message.chat.id}`]
**🧑‍💻المستخدم:** {mention}
**🧑‍💻المعرف:** @{message.from_user.username}
**🧑‍💻ايدي المستخدم:** `{message.from_user.id}`
**🧑‍💻رابط المجموعة:** {chatusername}
**🧑‍💻الكلمة التي بحثها:** {message.text}"""
    await app.send_message(LOG_GROUP_ID, f"{logger_text}", disable_web_page_preview=True)
    
