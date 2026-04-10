import sqlite3
import logging
import os
from datetime import datetime
import pytz
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler

# --- CONFIGURATION ---
BOT_TOKEN = "8297691834:AAE-5u3iHuHhKzFAStx0jsFlcErbNO0BT5U" 
ADMIN_ID = 5341486382 

logging.basicConfig(level=logging.INFO)

# --- DATABASE SETUP ---
conn = sqlite3.connect("ggwp_my.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        referrer INTEGER
    )
    """)
conn.commit()

# --- UTILS ---
def get_main_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🆔 Register Akaun", callback_data="show_register"),
            InlineKeyboardButton("🚀 Terima Deposit", url="https://ggwp.com/deposit")
        ],
        [
            InlineKeyboardButton("🎁 Claim Bonus 27%", url="https://ggwp.com/promosi"),
            InlineKeyboardButton("💰 Bonus Tersedia", url="https://ggwp.com/bonus")
        ],
        [
            InlineKeyboardButton("🎰 List Game", url="https://ggwp.com/games"),
            InlineKeyboardButton("📢 Channel Bukti Cuci", url="https://t.me/ggwp888channel")
        ],
        [
            InlineKeyboardButton("💬 Chat Amoi Sini", url="https://wa.me/60195472739"),
            InlineKeyboardButton("🎮 Link Game", url="https://ggwp.com/play")
        ]
    ])

# --- HANDLERS ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id

    # 1. Get Malaysia Time (MYT)
    my_tz = pytz.timezone('Asia/Kuala_Lumpur')
    my_time = datetime.now(my_tz).hour

    # 2. Local Greeting Logic
    if 5 <= my_time < 12:
        greeting = "Selamat Pagi"
    elif 12 <= my_time < 18:
        greeting = "Selamat Petang"
    else:
        greeting = "Selamat Malam"

    # 3. Database Logic
    cursor.execute("SELECT user_id FROM users WHERE user_id=?", (user_id,))
    if not cursor.fetchone():
        cursor.execute("INSERT INTO users (user_id) VALUES (?)", (user_id,))
        conn.commit()

    # 4. Welcome Message
    welcome_msg = (
        "🏆🏆🏆🏆🏆🏆🏆🏆🏆🏆\n"
        "🎰 ✨ **GGWP MALAYSIA** ✨ 🎰\n"
        "🏆🏆🏆🏆🏆🏆🏆🏆🏆🏆\n\n"
        f"*{greeting}, BOSS {user.first_name.upper()}!* 👑🇲🇾\n"
        "Selamat datang ke platform paling 'steady' di Malaysia.\n\n"
        "🎁 **PROMOSI KHAS MEMBER BARU**\n"
        "┌───────────────────┐\n"
        " 💵 **MIN DEPOSIT** ⇢ *RM20*\n"
        " 💰 **CLAIM BONUS** ⇢ *27% EXTRA*\n"
        " 💳 **METHOD** ⇢ *BANKIN / DUITNOW*\n"
        "└───────────────────┘\n\n"
        "⚠️ **TERMA & SYARAT BONUS**\n"
        "🚫 *Dilarang bermain Live Game*\n"
        "🚫 *Dilarang bermain Banned Games*\n"
        "*(Jika langgar, kredit akan di-BURN!)*\n\n"
        "⚡ **SERVICE STATUS**\n"
        "🔹 **CUCI (WD)** ⇢ [ **PANTAS 3 MIN** ]\n"
        "🔹 **TNG E-WALLET** ⇢ [ **AUTO DEPO** ]\n"
        "━━━━━━━━━━━━━━━━━━━━━\n"
        "✨ *Lubuk Cuci Bossku, Gerenti Jackpot!* ✨\n"
        "━━━━━━━━━━━━━━━━━━━━━\n\n"
        "⬇️ **TEKAN BUTANG DI BAWAH** ⬇️"
    )

    await update.message.reply_text(welcome_msg, reply_markup=get_main_keyboard(), parse_mode='Markdown')

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "show_register":
        register_keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🟢 WhatsApp Amoi", url="https://wa.me/60195472739?text=Amoi%20saya%20nak%20register"),
                InlineKeyboardButton("🔵 Telegram Admin", url="https://t.me/GGWP888Admin")
            ],
            [
                InlineKeyboardButton("⬅️ Kembali Menu Utama", callback_data="back_to_main")
            ]
        ])
        
        await query.edit_message_text(
            text="👑 **MENU PENDAFTARAN GGWP** 👑\n\n"
                 "Sila pilih platform untuk daftar akaun, BOSSku!\n"
                 "Amoi tunggu di sana ya! ❤️\n\n"
                 "─────────────────────",
            reply_markup=register_keyboard,
            parse_mode='Markdown'
        )

    elif query.data == "back_to_main":
        # Mengembalikan ke tampilan awal
        user = update.effective_user
        my_tz = pytz.timezone('Asia/Kuala_Lumpur')
        my_time = datetime.now(my_tz).hour
        greeting = "Selamat Pagi" if 5 <= my_time < 12 else "Selamat Petang" if 12 <= my_time < 18 else "Selamat Malam"

        welcome_msg = (
            "🏆🏆🏆🏆🏆🏆🏆🏆🏆🏆\n"
            "🎰 ✨ **GGWP MALAYSIA** ✨ 🎰\n"
            "🏆🏆🏆🏆🏆🏆🏆🏆🏆🏆\n\n"
            f"*{greeting}, BOSS {user.first_name.upper()}!* 👑🇲🇾\n\n"
            "🎁 **PROMOSI KHAS MEMBER BARU**\n"
            "┌───────────────────┐\n"
            " 💵 **MIN DEPOSIT** ⇢ *RM20*\n"
            " 💰 **CLAIM BONUS** ⇢ *27% EXTRA*\n"
            " 💳 **METHOD** ⇢ *BANKIN / DUITNOW*\n"
            "└───────────────────┘\n\n"
            "⬇️ **TEKAN BUTANG DI BAWAH** ⬇️"
        )
        await query.edit_message_text(text=welcome_msg, reply_markup=get_main_keyboard(), parse_mode='Markdown')

# --- ADMIN COMMANDS ---

async def users_count(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID: return
    cursor.execute("SELECT COUNT(*) FROM users")
    await update.message.reply_text(f"👥 Total player GGWP: {cursor.fetchone()[0]}")

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID or not context.args: return
    msg_text = " ".join(context.args)
    cursor.execute("SELECT user_id FROM users")
    users = cursor.fetchall()
    sent = 0
    for (uid,) in users:
        try:
            await context.bot.send_message(chat_id=uid, text=msg_text)
            sent += 1
        except: pass
    await update.message.reply_text(f"✅ Blasting Selesai! Berjaya: {sent}")

# --- MAIN ---
if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("users", users_count))
    application.add_handler(CommandHandler("broadcast", broadcast))
    application.add_handler(CallbackQueryHandler(handle_callback))
    
    print("--- GGWP MALAYSIA BOT IS RUNNING ---")
    application.run_polling()
