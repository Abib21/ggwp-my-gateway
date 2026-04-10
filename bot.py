import sqlite3
import logging
import os
from datetime import datetime
import pytz
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# --- CONFIGURATION ---
BOT_TOKEN = "8297691834:AAE-5u3iHuHhKzFAStx0jsFlcErbNO0BT5U" 
ADMIN_ID = 5341486382 # Your Admin ID

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

    # 4. Keyboard Setup
    keyboard = [
        [
            InlineKeyboardButton("🆔 Register", url="https://ggwp.com/register"),
            InlineKeyboardButton("🚀 Terima deposit", url="https://ggwp.com/login")
        ],
        [
            InlineKeyboardButton("🎁 Claim Bonus 27%", url="https://ggwp.com/promosi"),
            InlineKeyboardButton("💰 Bonus Tersedia", url="https://ggwp.com/guide")
        ],
        [
            InlineKeyboardButton("🎰 List Game", url="https://t.me/GGWP_Signal"),
            InlineKeyboardButton("📢 Channel Bukti Cuci", url="https://t.me/ggwp888channel")
        ],
        [
            InlineKeyboardButton("💬 Chat Amoi Sini", url="https://ggwp.com/support"),
            InlineKeyboardButton("🎮 Link Game", url="https://t.me/GGWP_Support")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # 5. Welcome Message (Sudah diperbaiki indentasinya)
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
        "✨ *Main Sini, Confirm Cuci* ✨\n"
        "━━━━━━━━━━━━━━━━━━━━━\n\n"
    )

    await update.message.reply_text(welcome_msg, reply_markup=reply_markup, parse_mode='Markdown')

# --- ADMIN COMMANDS ---

async def users_count(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    cursor.execute("SELECT COUNT(*) FROM users")
    total = cursor.fetchone()[0]
    await update.message.reply_text(f"👥 Total player GGWP: {total}")

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    
    if not context.args:
        await update.message.reply_text("❌ Guna: /broadcast [pesan]")
        return

    msg_text = " ".join(context.args)
    cursor.execute("SELECT user_id FROM users")
    all_users = cursor.fetchall()

    sent = 0
    failed = 0
    for (uid,) in all_users:
        try:
            await context.bot.send_message(chat_id=uid, text=msg_text)
            sent += 1
        except Exception:
            failed += 1

    await update.message.reply_text(f"✅ Blasting Selesai!\nBerjaya: {sent}\nGagal: {failed}")

# --- MAIN ---
if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("users", users_count))
    application.add_handler(CommandHandler("broadcast", broadcast))

    print("--- GGWP MALAYSIA BOT IS RUNNING ---")
    application.run_polling()
