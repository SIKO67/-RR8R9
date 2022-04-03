from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaPhoto,
    Message,
)
from Music import BOT_NAME, BOT_USERNAME
from Music.config import GROUP, CHANNEL

def play_markup(videoid, user_id):
    buttons = [
        [
            InlineKeyboardButton(text="• اެݪقناެة", url=f"https://t.me/{CHANNEL}"),
            InlineKeyboardButton(text="• تَحَكَمَ", callback_data=f"other {videoid}|{user_id}"),
        ],
        [      
               InlineKeyboardButton(text="• مَسِحَ", callback_data=f"close"),
        ],
    ]
    return buttons


def others_markup(videoid, user_id):
    buttons = [
        [
            InlineKeyboardButton(text="▷", callback_data=f"resumevc2"),
            InlineKeyboardButton(text="II", callback_data=f"pausevc2"),
            InlineKeyboardButton(text="‣‣I", callback_data=f"skipvc2"),
            InlineKeyboardButton(text="▢", callback_data=f"stopvc2"),
        ],
        [
            InlineKeyboardButton(text="• اެضِاެفة اެݪى قاެئمة اެنتضاެࢪي ​", callback_data=f'playlist {videoid}|{user_id}'),
            InlineKeyboardButton(text="• اެضِاެفة اެݪىِ قِائمة اެݪمَجمۅعة ", callback_data=f'group_playlist {videoid}|{user_id}'),
        ],
        [
            InlineKeyboardButton(
                text="• تَحَمَيَݪ صَۅٛتَ", callback_data=f"gets audio|{videoid}|{user_id}"
            ),
            InlineKeyboardButton(
                text="• تَحمَيݪ فَيدَيۅ", callback_data=f"gets video|{videoid}|{user_id}"
            ),
        ],
        [
            InlineKeyboardButton(
                text="⪻", callback_data=f"goback {videoid}|{user_id}"
            ),
            InlineKeyboardButton(text="• مَسِحَ", callback_data=f"close2"),
        ],
    ]
    return buttons


play_keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("▷", callback_data="resumevc"),
            InlineKeyboardButton("II", callback_data="pausevc"),
            InlineKeyboardButton("‣‣I", callback_data="skipvc"),
            InlineKeyboardButton("▢", callback_data="stopvc"),
        ],
        [InlineKeyboardButton("• مَسِحَ", callback_data="close")],
    ]
)


def audio_markup(videoid, user_id):
    buttons = [
        [
            InlineKeyboardButton(text="▷", callback_data=f"resumevc2"),
            InlineKeyboardButton(text="II", callback_data=f"pausevc2"),
            InlineKeyboardButton(text="‣‣I", callback_data=f"skipvc2"),
            InlineKeyboardButton(text="▢", callback_data=f"stopvc2"),
        ],
        [InlineKeyboardButton(text="• مَسِحَ", callback_data="close2")],
    ]
    return buttons


def search_markup(
    ID1,
    ID2,
    ID3,
    ID4,
    ID5,
    duration1,
    duration2,
    duration3,
    duration4,
    duration5,
    user_id,
    query,
):
    buttons = [
        [
            InlineKeyboardButton(
                text="¹", callback_data=f"Music2 {ID1}|{duration1}|{user_id}"
            ),
            InlineKeyboardButton(
                text="²", callback_data=f"Music2 {ID2}|{duration2}|{user_id}"
            ),
            InlineKeyboardButton(
                text="³", callback_data=f"Music2 {ID3}|{duration3}|{user_id}"
            ),
        ],
        [
            InlineKeyboardButton(
                text="⁴", callback_data=f"Music2 {ID4}|{duration4}|{user_id}"
            ),
            InlineKeyboardButton(
                text="⁵", callback_data=f"Music2 {ID5}|{duration5}|{user_id}"
            ),
        ],
        [InlineKeyboardButton(text="⪼", callback_data=f"popat 1|{query}|{user_id}")],
        [
            InlineKeyboardButton(
                text="• مَسِحَ", callback_data=f"ppcl2 smex|{user_id}"
            ),
        ],
    ]
    return buttons


def search_markup2(
    ID6,
    ID7,
    ID8,
    ID9,
    ID10,
    duration6,
    duration7,
    duration8,
    duration9,
    duration10,
    user_id,
    query,
):
    buttons = [
        [
            InlineKeyboardButton(
                text="⁶", callback_data=f"Music2 {ID6}|{duration6}|{user_id}"
            ),
            InlineKeyboardButton(
                text="⁷", callback_data=f"Music2 {ID7}|{duration7}|{user_id}"
            ),
            InlineKeyboardButton(
                text="⁸", callback_data=f"Music2 {ID8}|{duration8}|{user_id}"
            ),
        ],
        [
            InlineKeyboardButton(
                text="⁹", callback_data=f"Music2 {ID9}|{duration9}|{user_id}"
            ),
            InlineKeyboardButton(
                text="¹⁰", callback_data=f"Music2 {ID10}|{duration10}|{user_id}"
            ),
        ],
        [
            InlineKeyboardButton(text="⪻", callback_data=f"popat 2|{query}|{user_id}"),
        ],
        [InlineKeyboardButton(text="• مَسِحَ", callback_data=f"ppcl2 smex|{user_id}")],
    ]
    return buttons


def personal_markup(link):
    buttons = [
        [InlineKeyboardButton(text="• مَۅقعَ يَۅتيَۅب", url=f"{link}")],
        [InlineKeyboardButton(text="• مَسِحَ", callback_data=f"close2")],
    ]
    return buttons


start_keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                "• اެݪاެۅٛاެمَࢪ", url="https://telegra.ph/ҡʏʏ-ᴍᴇᴍ-ᴇx-01-21-2"
            )
        ],
        [InlineKeyboardButton("• مَسِحَ", callback_data="close2")],
    ]
)

confirm_keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("ʏᴀ", callback_data="cbdel"),
            InlineKeyboardButton("• مَسِحَ", callback_data="close2"),
        ]
    ]
)

confirm_group_keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("ʏᴀ", callback_data="cbgroupdel"),
            InlineKeyboardButton("ᴛɪᴅᴀᴋ", callback_data="close2"),
        ]
    ]
)

close_keyboard = InlineKeyboardMarkup(
    [[InlineKeyboardButton("مسح", callback_data="close2")]]
)

play_list_keyboard = InlineKeyboardMarkup( 
            [
                [
                    InlineKeyboardButton(
                        "• اެضِاެفة اެݪى قاެئمة اެنتضاެࢪي​", callback_data="P_list"
                    ),
                    InlineKeyboardButton(
                        "• اެضِاެفة اެݪىِ قِائمة اެݪمَجمۅعة​​", callback_data="G_list"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "• مَسِحَ​", callback_data="close2"
                    )
                ]
            ]
        )

def playlist_markup(user_name, user_id):
    buttons= [
            [
                InlineKeyboardButton(text=f"مَسِحَ", callback_data=f'play_playlist {user_id}|group'),
                InlineKeyboardButton(text=f"{user_name[:8]}", callback_data=f'play_playlist {user_id}|personal'),
            ],
            [
                InlineKeyboardButton(text="ᴛᴜᴛᴜᴘ​", callback_data="close2")              
            ],
        ]
    return buttons


def start_pannel():
    if not CHANNEL and not GROUP:
        buttons = [
            [
                InlineKeyboardButton(
                    text="🔧 sᴇᴛᴛɪɴɢs", callback_data="settingm"
                )
            ],
        ]
        return f"🎛  **This is {BOT_NAME}**", buttons
    if not CHANNEL and GROUP:
        buttons = [
            [
                InlineKeyboardButton(
                    text="🔧 sᴇᴛᴛɪɴɢs", callback_data="settingm"
                )
            ],
            [
                InlineKeyboardButton(
                    text="✨ sᴜᴘᴘᴏʀᴛ", url=f"https://t.me/{GROUP}"
                ),
            ],
        ]
        return f"🎛  **This is {BOT_NAME}*", buttons
    if CHANNEL and not GROUP:
        buttons = [
            [
                InlineKeyboardButton(
                    text="🔧 sᴇᴛᴛɪɴɢs", callback_data="settingm"
                )
            ],
            [
                InlineKeyboardButton(
                    text="✨ ᴄʜᴀɴɴᴇʟ", url=f"https://t.me/{GROUP}"
                ),
            ],
        ]
        return f"🎛  **This is {BOT_NAME}**", buttons
    if CHANNEL and GROUP:
        buttons = [
            [
                InlineKeyboardButton(
                    text="🔧 sᴇᴛᴛɪɴɢs", callback_data="settingm"
                )
            ],
            [
                InlineKeyboardButton(
                    text="✨ ᴄʜᴀɴɴᴇʟ", url=f"https://t.me/{CHANNEL}"
                ),
                InlineKeyboardButton(
                    text="✨ sᴜᴘᴘᴏʀᴛ", url=f"https://t.me/{GROUP}"
                ),
            ],
        ]
        return f"🎛  **This is {BOT_NAME}**", buttons


def private_panel():
    if not CHANNEL and not GROUP:
        buttons = [
            [
                InlineKeyboardButton(
                    "➕ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘs",
                    url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
                )
            ],
        ]
        return f"🎛  **This is {BOT_NAME}**", buttons
    if not CHANNEL and GROUP:
        buttons = [
            [
                InlineKeyboardButton(
                    "➕ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴏs",
                    url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
                )
            ],
            [
                InlineKeyboardButton(
                    text="✨ sᴜᴘᴘᴏʀᴛ", url=f"https://t.me/{GROUP}"
                ),
            ],
        ]
        return f"🎛  **This is {BOT_NAME}*", buttons
    if CHANNEL and not GROUP:
        buttons = [
            [
                InlineKeyboardButton(
                    "➕ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘs",
                    url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
                )
            ],
            [
                InlineKeyboardButton(
                    text="✨ ᴄʜᴀɴɴᴇʟ", url=f"https://t.me/{GROUP}"
                ),
            ],
        ]
        return f"🎛  **This is {BOT_NAME}**", buttons
    if CHANNEL and GROUP:
        buttons = [
            [
                InlineKeyboardButton(
                    "➕ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘs",
                    url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
                )
            ],
            [
                InlineKeyboardButton(
                    text="✨ ᴄʜᴀɴɴᴇʟ", url=f"https://t.me/{CHANNEL}"
                ),
                InlineKeyboardButton(
                    text="✨ sᴜᴘᴘᴏʀᴛ", url=f"https://t.me/{GROUP}"
                ),
            ],
        ]
        return f"🎛  **This is {BOT_NAME}**", buttons


def setting_markup():
    buttons = [
        [
            InlineKeyboardButton(text="• جودة الصوت ", callback_data="AQ"),
            InlineKeyboardButton(text="•  مستوى الصوت", callback_data="AV"),
        ],
        [
            InlineKeyboardButton(
                text="• المستخدمون الموثوقون ", callback_data="AU"
            ),
            InlineKeyboardButton(
                text="• لوحة التحكم", callback_data="Dashboard"
            ),
        ],
        [
            InlineKeyboardButton(text="• مَسِحَ", callback_data="close"),
        ],
    ]
    return f"🔧  **{BOT_NAME}• الاعدادات**", buttons


def volmarkup():
    buttons = [
        [
            InlineKeyboardButton(
                text="• إعادة ضبط حجم الصوت", callback_data="HV"
            )
        ],
        [
            InlineKeyboardButton(text="• حجم منخفض", callback_data="LV"),
            InlineKeyboardButton(text="• حجم متوسط ", callback_data="MV"),
        ],
        [
            InlineKeyboardButton(text="• حجم مرتفع ", callback_data="HV"),
            InlineKeyboardButton(text="• حجم مرتفع جداً ", callback_data="VAM"),
        ],
        [
            InlineKeyboardButton(
                text="🔽 حجم مخصص 🔽", callback_data="Custommarkup"
            )
        ],
        [InlineKeyboardButton(text="🔙 ࢪجَۅٛعَ", callback_data="settingm")],
    ]
    return f"🔧  **{BOT_NAME} • الاعدادات**", buttons


def custommarkup():
    buttons = [
        [
            InlineKeyboardButton(text="+10", callback_data="PTEN"),
            InlineKeyboardButton(text="-10", callback_data="MTEN"),
        ],
        [
            InlineKeyboardButton(text="+25", callback_data="PTF"),
            InlineKeyboardButton(text="-25", callback_data="MTF"),
        ],
        [
            InlineKeyboardButton(text="+50", callback_data="PFZ"),
            InlineKeyboardButton(text="-50", callback_data="MFZ"),
        ],
        [InlineKeyboardButton(text="🔼 حجم مخصص 🔼", callback_data="AV")],
    ]
    return f"🔧  **{BOT_NAME} • الاعدادات**", buttons


def usermarkup():
    buttons = [
        [
            InlineKeyboardButton(text="• المستخدمون الموثوقون", callback_data="EVE"),
            InlineKeyboardButton(text="• المشرفون فقط", callback_data="AMS"),
        ],
        [
            InlineKeyboardButton(
                text="• المستخدمون الموثوقون", callback_data="USERLIST"
            )
        ],
        [InlineKeyboardButton(text="🔙 ࢪجَۅٛعَ", callback_data="settingm")],
    ]
    return f"🔧  **{BOT_NAME} • الاعدادات**", buttons


def dashmarkup():
    buttons = [
        [
            InlineKeyboardButton(text="• الاستخدام", callback_data="UPT"),
            InlineKeyboardButton(text="• الرام", callback_data="RAT"),
        ],
        [
            InlineKeyboardButton(text="• المعالج", callback_data="CPT"),
            InlineKeyboardButton(text="• القرص", callback_data="DIT"),
        ],
        [InlineKeyboardButton(text="🔙 ࢪجَۅٛعَ", callback_data="settingm")],
    ]
    return f"🔧  **{BOT_NAME} • الاعدادات**", buttons


stats1 = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text="• احصائيات", callback_data=f"sys_stats"
            ),
            InlineKeyboardButton(
                text="• احصائيات يناير", callback_data=f"sto_stats"
            ),
        ],
        [
            InlineKeyboardButton(
                text="• احصائيات البوت", callback_data=f"bot_stats"
            ),
            InlineKeyboardButton(
                text="• احصائيات المساعد", callback_data=f"assis_stats"
            )
        ],
    ]
)

stats2 = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text="• احصائيات ", callback_data=f"gen_stats"
            ),
            InlineKeyboardButton(
                text="• احصائيات يناير", callback_data=f"sto_stats"
            ),
        ],
        [
            InlineKeyboardButton(
                text="• احصائيات البوت", callback_data=f"bot_stats"
            ),
            InlineKeyboardButton(
                text="• احصائيات المساعد", callback_data=f"assis_stats"
            )
        ],
    ]
)

stats3 = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text="• احصائيات", callback_data=f"sys_stats"
            ),
            InlineKeyboardButton(
                text="• احصائيات يناير", callback_data=f"gen_stats"
            ),
        ],
        [
            InlineKeyboardButton(
                text="• احصائيات البوت", callback_data=f"bot_stats"
            ),            
            InlineKeyboardButton(
                text="• احصائيات المساعد", callback_data=f"assis_stats"
            )
        ],
    ]
)

stats4 = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text="• احصائيات", callback_data=f"sys_stats"
            ),
            InlineKeyboardButton(
                text="• احصائيات التخزين", callback_data=f"sto_stats"
            ),
        ],
        [
            InlineKeyboardButton(
                text="• احصائيات يناير", callback_data=f"gen_stats"
            ),
            InlineKeyboardButton(
                text="• احصائيات المساعد", callback_data=f"assis_stats"
            )
        ],
    ]
)


stats5 = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text="• احصائيات", callback_data=f"sys_stats"
            ),
            InlineKeyboardButton(
                text="• احصائيات التخزين", callback_data=f"sto_stats"
            ),
        ],
        [
            InlineKeyboardButton(
                text="• احصائيات البوت", callback_data=f"bot_stats"
            ),
            InlineKeyboardButton(
                text="• احصائيات يناير", callback_data=f"gen_stats"
            )
        ],
    ]
)


stats6 = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text="جمع احصائيات المساعد....",
                callback_data=f"wait_stats",
            )
        ]
    ]
)
