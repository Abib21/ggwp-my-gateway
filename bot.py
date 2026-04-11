import sqlite3
import logging
import os
from datetime import datetime
import pytz
from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup,
    KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
)
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes,
    CallbackQueryHandler, MessageHandler, filters
)

# =============================================================================
# CONFIGURATION
# =============================================================================
BOT_TOKEN  = "8297691834:AAE-5u3iHuHhKzFAStx0jsFlcErbNO0BT5U"
ADMIN_ID   = 5341486382
GROUP_ID   = "-5299802622"  # GGWP Staff Notification Group
CHANNEL_ID = None           # Isi jika ada channel, contoh: "-1001234567890"

# =============================================================================
# LOGGING
# FIX: Format logging lebih informatif — tunjuk masa, level, dan mesej
# =============================================================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

# =============================================================================
# DATABASE SETUP
# =============================================================================
conn = sqlite3.connect("ggwp_my.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id     INTEGER PRIMARY KEY,
        username    TEXT,
        phone       TEXT,
        date_joined TEXT
    )
""")
conn.commit()

# =============================================================================
# UTILS
# =============================================================================
def get_main_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🆔 REGISTER",            callback_data="show_register"),
            InlineKeyboardButton("🚀 TERIMA DEPOSIT",      callback_data="show_deposit")
        ],
        [
            InlineKeyboardButton("🎁 CLAIM BONUS 27%",     callback_data="show_bonus"),
            InlineKeyboardButton("💰 PROMOTION",            callback_data="show_all_promos")
        ],
        [
            InlineKeyboardButton("🎰 GAME LIST",           callback_data="show_game_list"),
            InlineKeyboardButton("🎮 LINK GAME",            callback_data="show_links")
        ],
        [
            InlineKeyboardButton("💬 CHAT AMOI",           callback_data="show_chat_options"),
            InlineKeyboardButton("📢 BUKTI CUCI",           url="https://t.me/ggwp888channel")
        ],
        [
            InlineKeyboardButton("💰 MAX/LIMIT CUCI",      callback_data="show_max_cuci")
        ],
        [
            InlineKeyboardButton("❌ LIST BANNED GAME ❌",  callback_data="show_banned_games")
        ]
    ])

def get_greeting() -> str:
    my_tz   = pytz.timezone('Asia/Kuala_Lumpur')
    my_time = datetime.now(my_tz).hour
    if 5 <= my_time < 12:
        return "Selamat Pagi"
    elif 12 <= my_time < 18:
        return "Selamat Petang"
    else:
        return "Selamat Malam"

def get_welcome_msg(first_name: str) -> str:
    # FIX: Telegram Markdown hanya sokong *bold* bukan **bold**
    # Semua ** ditukar kepada * supaya formatting betul-betul papar dalam Telegram
    greeting = get_greeting()
    return (
        "🏆 🏆 🏆 🏆 🏆 🏆 🏆 🏆 🏆 🏆\n"
        "🎰 ✨ *GGWP MALAYSIA* ✨ 🎰\n"
        "🏆 🏆 🏆 🏆 🏆 🏆 🏆 🏆 🏆 🏆\n\n"
        f"*{greeting}, BOSS {first_name.upper()}!* 👑 🇲🇾\n"
        "🎁 *PROMOSI KHAS MEMBER BARU*\n\n"
        "┌──────────────────────────┐\n"
        "  💵 *MIN DEPOSIT* ⇢ RM20\n"
        "  💰 *CLAIM BONUS* ⇢ 27% EXTRA\n"
        "  💳 *METHOD* ⇢ BANKIN / DUITNOW\n"
        "└──────────────────────────┘\n\n"
        "⚠️ *TERMA & SYARAT BONUS*\n"
        "🚫 Dilarang bermain Live Game\n"
        "🚫 Dilarang bermain Banned Games\n"
        "‼️ *(Jika langgar, kredit akan di-BURN!)* ‼️\n\n"
        "⚡ *SERVICE STATUS*\n"
        "🔹 *CUCI (WD)* ⇢ 🟢 PANTAS 3 MIN\n"
        "🔹 *TNG E-WALLET* ⇢ ⚡ AUTO DEPOSIT\n"
        "━━━━━━━━━━━━━━━━━━━━━\n\n"
        "⬇️ *TEKAN DEKAT BAWAH* ⬇️"
    )

def get_safe_name(user) -> str:
    """Pulangkan nama paparan yang selamat — untuk notifikasi & log."""
    if user.username:
        return f"@{user.username}"
    elif user.first_name:
        return user.first_name
    elif user.last_name:
        return user.last_name
    else:
        return f"User_{user.id}"

def get_display_first_name(user) -> str:
    """
    Pulangkan nama untuk get_welcome_msg() sahaja.
    Pastikan .upper() tidak crash — @username tidak sesuai
    untuk 'BOSS {nama}', jadi gunakan first_name sebagai keutamaan.
    """
    if user.first_name:
        return user.first_name
    elif user.last_name:
        return user.last_name
    elif user.username:
        return user.username
    else:
        return f"Boss_{user.id}"

def is_registered(user_id: int) -> bool:
    cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
    return cursor.fetchone() is not None

def get_my_time() -> datetime:
    return datetime.now(pytz.timezone('Asia/Kuala_Lumpur'))

async def post_join_announcement(bot, display_name: str, phone_no: str, now: datetime):
    # FEATURE: Format masa join yang lebih lengkap dan cantik untuk staff group
    day_names = {
        "Monday": "Isnin", "Tuesday": "Selasa", "Wednesday": "Rabu",
        "Thursday": "Khamis", "Friday": "Jumaat",
        "Saturday": "Sabtu", "Sunday": "Ahad"
    }
    day_en   = now.strftime("%A")
    day_my   = day_names.get(day_en, day_en)
    date_str = now.strftime("%d/%m/%Y")
    time_str = now.strftime("%I:%M %p")   # contoh: 02:35 PM

    announcement = (
        "🔔 *MEMBER BARU GGWP* 🔔\n"
        "━━━━━━━━━━━━━━━━━━━━━\n"
        f"👤 *Nama:* {display_name}\n"
        f"📞 *No. HP:* `{phone_no}`\n"
        "━━━━━━━━━━━━━━━━━━━━━\n"
        f"📅 *Tarikh:* {day_my}, {date_str}\n"
        f"🕐 *Masa:* {time_str} (WIB/MYT)\n"
        "━━━━━━━━━━━━━━━━━━━━━\n"
        "✅ _Sila follow up dengan member baru ini!_"
    )

    for chat_id, label in [(CHANNEL_ID, "Channel"), (GROUP_ID, "Staff Group")]:
        if not chat_id:
            continue
        try:
            await bot.send_message(
                chat_id=chat_id,
                text=announcement,
                parse_mode='Markdown'
            )
            logger.info(f"✅ Announcement dihantar ke {label} ({chat_id})")
        except Exception as e:
            logger.warning(f"⚠️ Gagal hantar ke {label} ({chat_id}): {e}")

# =============================================================================
# HANDLERS
# =============================================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    # Jika sudah daftar, terus tunjuk menu utama
    if is_registered(user.id):
        logger.info(f"Returning user: {get_safe_name(user)} ({user.id})")
        await update.message.reply_text(
            get_welcome_msg(get_display_first_name(user)),
            reply_markup=get_main_keyboard(),
            parse_mode='Markdown'
        )
        return

    # Belum daftar — minta share nombor HP
    logger.info(f"New visitor: {get_safe_name(user)} ({user.id})")
    contact_btn  = [[KeyboardButton("📲 DAFTAR SEKARANG (SHARE NO. HP)", request_contact=True)]]
    reply_markup = ReplyKeyboardMarkup(contact_btn, one_time_keyboard=True, resize_keyboard=True)

    await update.message.reply_text(
        f"Selamat Datang Boss *{get_display_first_name(user)}*! ✨\n\n"
        "Sila tekan butang *DAFTAR SEKARANG* di bawah untuk sahkan akaun dan mula bermain. 🎰",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )


async def handle_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact  = update.message.contact
    user     = update.effective_user
    phone_no = contact.phone_number

    # FIX: Pastikan nombor HP sentiasa ada "+" di hadapan
    if not phone_no.startswith("+"):
        phone_no = "+" + phone_no

    display_name = get_safe_name(user)
    now          = get_my_time()
    date_str     = now.strftime('%Y-%m-%d')

    # Guard: jangan daftar semula
    if is_registered(user.id):
        logger.info(f"Re-registration attempt: {display_name} ({user.id})")
        await update.message.reply_text(
            "✅ Akaun anda sudah berdaftar!",
            reply_markup=ReplyKeyboardRemove()
        )
        await update.message.reply_text(
            get_welcome_msg(get_display_first_name(user)),
            reply_markup=get_main_keyboard(),
            parse_mode='Markdown'
        )
        return

    # Simpan ke database
    cursor.execute(
        "INSERT OR REPLACE INTO users (user_id, username, phone, date_joined) VALUES (?, ?, ?, ?)",
        (user.id, display_name, phone_no, date_str)
    )
    conn.commit()
    logger.info(f"✅ Member baru didaftar: {display_name} ({phone_no})")

    # Notifikasi ADMIN (private)
    notif_text = (
        f"🔔 *NEW MEMBER GGWP* 🔔\n\n"
        f"👤 {display_name}\n"
        f"📞 `{phone_no}`\n"
        f"📅 {date_str}  🕐 {now.strftime('%H:%M')}\n"
        f"🚀 Baru saja bergabung di GGWP!"
    )
    try:
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=notif_text,
            parse_mode='Markdown'
        )
    except Exception as e:
        # FIX: Jangan silent fail — log supaya admin tahu ada masalah
        logger.warning(f"⚠️ Gagal notifikasi admin: {e}")

    # Post ke Staff Group & Channel (dengan format masa yang lengkap)
    await post_join_announcement(context.bot, display_name, phone_no, now)

    # Tunjuk menu utama kepada user
    await update.message.reply_text(
        "✅ *Akaun Berjaya Disahkan!* 🎉",
        reply_markup=ReplyKeyboardRemove(),
        parse_mode='Markdown'
    )
    await update.message.reply_text(
        get_welcome_msg(get_display_first_name(user)),
        reply_markup=get_main_keyboard(),
        parse_mode='Markdown'
    )


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user  = update.effective_user

    # FIX: Guard — user mesti daftar dulu sebelum boleh guna mana-mana butang
    if not is_registered(user.id):
        await query.answer(
            "⚠️ Sila /start dahulu untuk daftar!",
            show_alert=True
        )
        logger.warning(f"Unregistered callback attempt: {user.id} → {query.data}")
        return

    await query.answer()

    # FIX: Log dengan proper — berguna untuk debug
    logger.info(f"Callback: {get_safe_name(user)} → {query.data}")

    # FIX: Guna logging pada except — jangan biarkan silent
    try:
        await query.delete_message()
    except Exception as e:
        logger.debug(f"Tidak boleh delete mesej: {e}")

    back_button = InlineKeyboardButton("⬅️ Laman Utama", callback_data="back_to_main")
    chat_id     = query.message.chat_id

    # ------------------------------------------------------------------
    if query.data == "show_register":
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🟢 WhatsApp Amoi", url="https://wa.me/60195472739?text=Amoi%20saya%20nak%20register%20%F0%9F%A5%B0%F0%9F%9A%80%F0%9F%92%B0"),
                InlineKeyboardButton("🔵 Telegram Amoi", url="https://t.me/GGWP888Admin")
            ],
            [back_button]
        ])
        await context.bot.send_message(
            chat_id=chat_id,
            text="👑 *Join GGWP* 👑\n\nPilih platform untuk Join, Bossku!",
            reply_markup=keyboard,
            parse_mode='Markdown'
        )

    # ------------------------------------------------------------------
    elif query.data == "show_chat_options":
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🟢 WhatsApp Amoi", url="https://wa.me/60195472739"),
                InlineKeyboardButton("🔵 Telegram Amoi", url="https://t.me/GGWP888Admin")
            ],
            [back_button]
        ])
        await context.bot.send_message(
            chat_id=chat_id,
            text="💬 *HUBUNGI AMOI GGWP* 💬\n\nSila pilih platform untuk chat dengan kami!",
            reply_markup=keyboard,
            parse_mode='Markdown'
        )

    # ------------------------------------------------------------------
    elif query.data == "show_game_list":
        game_list_text = (
            "👑 🎰 *GGWP ROYAL CASINO* 🎰 👑\n"
            "✨ _Exclusive Game Selection_ ✨\n"
            "━━━━━━━━━━━━━━━━━━━━━\n\n"
            "🔥 *TOP GACOR SEKARANG* 🔥\n"
            "🏆 *Mega888* ⇢ ⚡ [ _HOT_ ]\n"
            "🏆 *Pussy888* ⇢ ⚡ [ _HOT_ ]\n"
            "🏆 *EVO888* ⇢ ⚡ [ _HOT_ ]\n"
            "🏆 *918 Kiss ORI* ⇢ ⚡ [ _HOT_ ]\n\n"
            "💎 *PREMIUM CASINO SELECTION*\n"
            "⭐ 918 Kiss Kaya\n"
            "⭐ LPE (Lucky Palace)\n"
            "⭐ Newtown Casino\n"
            "⭐ GreatWall (GW99)\n"
            "⭐ Live22 Malaysia\n"
            "⭐ Joker123 Gaming\n\n"
            "━━━━━━━━━━━━━━━━━━━━━"
        )
        await context.bot.send_message(
            chat_id=chat_id,
            text=game_list_text,
            reply_markup=InlineKeyboardMarkup([[back_button]]),
            parse_mode='Markdown'
        )

    # ------------------------------------------------------------------
    elif query.data == "show_max_cuci":
        max_cuci_text = (
            "💰🤑 *GGWP ROYAL CASINO MAX BAYAR* 🤑💰\n\n"
            "_Turnover x2_\n\n"
            "💵 *Maximum Bayar*\n"
            "_(Via Telco/Reload Pin/Share Kredit)_\n\n"
            "💰 Topup Rm5  - Rm10  Max RM188\n"
            "💰 Topup Rm11 - Rm30  Max Rm388\n"
            "💰 Topup Rm31 - Rm50  Max Rm588\n"
            "💰 Topup Rm51 - Rm100 Max Rm888\n"
            "🔥 Topup Rm101 Keatas Max 1088\n\n"
            "_MIN IN RM5 | MIN CUCI RM100_\n"
            "━━━━━━━━━━━━━━━━━━━━━\n"
            "🏧 *Maximum Bayar*\n"
            "_(Via Bankin/TnG)_\n\n"
            "💰 IN Rm10  - Rm29  Max Rm888\n"
            "💰 IN Rm30  - Rm49  Max Rm1388\n"
            "💰 IN Rm50  - Rm99  Max Rm2388\n"
            "💰 IN Rm100 - Rm299 Max Rm8888\n"
            "💰 IN Rm300 - Rm499 Max Rm12888\n"
            "🔥 IN Rm500 ke atas Max Rm16888\n\n"
            "_MIN TOPUP 10 | MIN CUCI 50_\n\n"
            "⚠️ Bawa Bonus Hanya Boleh main Slot game Sahaja\n"
            "❗️ Live Game/Fish/Table Game No Bonus\n"
            "✔️ Janji Cuci, Janji Bayar\n"
            "✅ 24 jams & Trusted Company"
        )
        await context.bot.send_message(
            chat_id=chat_id,
            text=max_cuci_text,
            reply_markup=InlineKeyboardMarkup([[back_button]]),
            parse_mode='Markdown'
        )

    # ------------------------------------------------------------------
    elif query.data == "show_bonus":
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🟢 WhatsApp Amoi", url="https://wa.me/60195472739?text=Amoi%20nak%20claim%20bonus%2027%25%20🥰🎁💰"),
                InlineKeyboardButton("🔵 Telegram Amoi", url="https://t.me/GGWP888Admin")
            ],
            [back_button]
        ])
        await context.bot.send_message(
            chat_id=chat_id,
            text="🎁 *CLAIM BONUS 27%* 🎁\n\nHubungi kami untuk claim bonus anda!",
            reply_markup=keyboard,
            parse_mode='Markdown'
        )

    # ------------------------------------------------------------------
    elif query.data == "show_all_promos":
        text = (
            "🎊 *PROMOTION MEMBER RASMI* 🎊\n"
            "━━━━━━━━━━━━━━━━━━━━━\n\n"
            "Daily 20% | Unlimited 5% | Recommend 30% | Rebate 8%"
        )
        await context.bot.send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=InlineKeyboardMarkup([[back_button]]),
            parse_mode='Markdown'
        )

    # ------------------------------------------------------------------
    elif query.data == "show_deposit":
        deposit_text = (
            "🚀 ⚡ *GGWP OFFICIAL DEPOSIT* ⚡ 🚀\n"
            "✨ _Fast Service • Trusted Agent_ ✨\n"
            "━━━━━━━━━━━━━━━━━━━━━\n\n"
            "💳 *PERBANKAN TEMPATAN*\n"
            "⇢ Semua Bank Malaysia Diterima\n"
            "⇢ Transfer Pantas & Selamat\n\n"
            "💰 *E-WALLET & QR*\n"
            "⇢ DuitNow / QR Pay (Semua Bank)\n"
            "⇢ Touch N'Go eWallet (Auto Deposit)\n\n"
            "🎫 *PIN RELOAD / TOPUP*\n"
            "⇢ 🟡 Digi\n"
            "⇢ 🔵 Celcom\n"
            "⇢ 🔴 Maxis / Hotlink\n"
            "⇢ 🟠 U-Mobile\n\n"
            "📲 *SHARE CREDIT (TRANSFER)*\n"
            "⇢ ✅ Digi\n"
            "⇢ ✅ Celcom\n"
            "⇢ ✅ Maxis\n"
            "⚠️ _No U-Mobile Share Credit_ ❌\n\n"
            "━━━━━━━━━━━━━━━━━━━━━\n"
            "‼️ *PENTING* ‼️\n"
            "👇 _Sila hubungi Admin untuk nomor akaun terkini!_\n"
            "✨ *Deposit Laju, Jackpot Padu!* ✨"
        )
        await context.bot.send_message(
            chat_id=chat_id,
            text=deposit_text,
            reply_markup=InlineKeyboardMarkup([[back_button]]),
            parse_mode='Markdown'
        )

    # ------------------------------------------------------------------
    elif query.data == "show_links":
        links_text = (
            "🎰 *LIST LINK GAME* 🎰\n"
            "━━━━━━━━━━━━━━━━━━━━━\n\n"
            "✨ *918KISS*\n"
            "Android & iOS: [KLIK SINI](https://yop1.918kiss.com/)\n\n"
            "✨ *MEGA888*\n"
            "Android & iOS: [KLIK SINI](https://m.mega166.com/mega/index.html)\n\n"
            "✨ *PUSSY888*\n"
            "Android & iOS: [KLIK SINI](https://ytl.pussy888.com/)\n\n"
            "✨ *LIVE22*\n"
            "Android: [KLIK SINI](https://live22474.com/Login)\n"
            "iOS: [KLIK SINI](https://botanica22.com/Login)\n\n"
            "✨ *918KAYA*\n"
            "Android & iOS: [KLIK SINI](http://download22.da31889.com/)\n\n"
            "✨ *JOKER*\n"
            "Android & iOS: [KLIK SINI](https://www.jokerapp888a.net/)\n\n"
            "✨ *NEWTOWN CASINO*\n"
            "Android: [KLIK SINI](https://cdn.newmax11.com/mobile.html)\n"
            "iOS: [KLIK SINI](https://www.nbig33.com/)\n\n"
            "✨ *EVO888*\n"
            "Android & iOS: [KLIK SINI](https://d.evo366.com/)\n\n"
            "━━━━━━━━━━━━━━━━━━━━━"
        )
        await context.bot.send_message(
            chat_id=chat_id,
            text=links_text,
            reply_markup=InlineKeyboardMarkup([[back_button]]),
            parse_mode='Markdown',
            disable_web_page_preview=True
        )

    # ------------------------------------------------------------------
    elif query.data == "show_banned_games":
        banned_text = (
            "❌ *LIST BANNED GAMES* ❌\n"
            "━━━━━━━━━━━━━━━━━━━━━\n\n"
            "⚜️ *918KISS / MEGA888 / 918KAYA*\n"
            "🙅 King Derby\n"
            "🙅 Thunderbolt\n"
            "🙅 Motorbike\n"
            "🙅 Roulette\n"
            "🙅 Seaworld\n\n"
            "⚜️ *XE88*\n"
            "🙅 Daily Job Mission\n"
            "🙅 King Derby\n"
            "🙅 Thunderbolt\n"
            "🙅 Motorbike\n"
            "🙅 Roulette\n"
            "🙅 MysteryBox\n\n"
            "⚜️ *PUSSY888*\n"
            "🙅 All Game 4D\n"
            "🙅 King Derby\n"
            "🙅 Thunderbolt\n"
            "🙅 Motorbike\n"
            "🙅 Seaworld\n\n"
            "⚜️ *JOKER*\n"
            "🙅 Powerbar\n\n"
            "━━━━━━━━━━━━━━━━━━━━━\n"
            "⚠️ _Jika bermain game di atas semasa ada bonus aktif, kredit akan di-BURN!_"
        )
        await context.bot.send_message(
            chat_id=chat_id,
            text=banned_text,
            reply_markup=InlineKeyboardMarkup([[back_button]]),
            parse_mode='Markdown'
        )

    # ------------------------------------------------------------------
    elif query.data == "back_to_main":
        await context.bot.send_message(
            chat_id=chat_id,
            text=get_welcome_msg(get_display_first_name(user)),
            reply_markup=get_main_keyboard(),
            parse_mode='Markdown'
        )

    # FIX: Handle unknown callback_data — elak silent fail
    else:
        logger.warning(f"Unknown callback_data: {query.data} dari {user.id}")
        await context.bot.send_message(
            chat_id=chat_id,
            text="⚠️ Ralat: Butang tidak dikenali. Sila kembali ke menu utama.",
            reply_markup=InlineKeyboardMarkup([[back_button]])
        )

# =============================================================================
# ADMIN COMMANDS
# =============================================================================

async def check_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    cursor.execute("SELECT COUNT(*) FROM users")
    total = cursor.fetchone()[0]
    cursor.execute(
        "SELECT COUNT(*) FROM users WHERE date_joined = ?",
        (get_my_time().strftime('%Y-%m-%d'),)
    )
    today = cursor.fetchone()[0]
    await update.message.reply_text(
        f"📊 *STATISTIK BOT GGWP*\n\n"
        f"👥 Total Player Berdaftar: *{total}*\n"
        f"🆕 Daftar Hari Ini: *{today}*",
        parse_mode='Markdown'
    )

async def list_players(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    cursor.execute(
        "SELECT username, phone, date_joined FROM users ORDER BY date_joined DESC LIMIT 50"
    )
    players = cursor.fetchall()
    if not players:
        await update.message.reply_text("Tiada player berdaftar lagi.")
        return
    lines = ["📋 *DAFTAR PLAYER (50 Terkini)* 📋\n"]
    for i, (uname, phone, date) in enumerate(players, 1):
        lines.append(f"{i}. {uname} ⇢ 📞 `{phone}` _({date})_")
    message = "\n".join(lines)
    # FIX: Split supaya tidak melebihi had 4096 aksara Telegram
    for i in range(0, len(message), 4000):
        await update.message.reply_text(message[i:i+4000], parse_mode='Markdown')

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    if not context.args:
        await update.message.reply_text(
            "Guna: `/broadcast Mesej anda di sini`",
            parse_mode='Markdown'
        )
        return
    msg = " ".join(context.args)
    cursor.execute("SELECT user_id FROM users")
    all_users = cursor.fetchall()
    success, failed = 0, 0
    for (uid,) in all_users:
        try:
            await context.bot.send_message(chat_id=uid, text=msg)
            success += 1
        except Exception as e:
            logger.warning(f"Broadcast gagal untuk user {uid}: {e}")
            failed += 1
    await update.message.reply_text(
        f"📢 *Broadcast Selesai*\n\n"
        f"✅ Berjaya: *{success}*\n"
        f"❌ Gagal: *{failed}*",
        parse_mode='Markdown'
    )

# =============================================================================
# MAIN
# =============================================================================
if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Public
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.CONTACT, handle_contact))
    application.add_handler(CallbackQueryHandler(handle_callback))

    # Admin only
    application.add_handler(CommandHandler("status", check_status))
    application.add_handler(CommandHandler("list_players", list_players))
    application.add_handler(CommandHandler("broadcast", broadcast))

    print("--- GGWP MALAYSIA BOT IS RUNNING ---")
    application.run_polling()
