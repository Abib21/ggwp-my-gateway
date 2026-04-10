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
            InlineKeyboardButton("🚀 Terima Deposit", callback_data="show_deposit")
        ],
        [
            InlineKeyboardButton("🎁 Claim Bonus 27%", callback_data="show_bonus"),
            InlineKeyboardButton("💰 Bonus Tersedia", callback_data="show_all_promos")
        ],
        [
            InlineKeyboardButton("🎰 List Game", callback_data="show_game_list"),
            InlineKeyboardButton("📢 Channel Bukti Cuci", url="https://t.me/ggwp888channel")
        ],
        [
            InlineKeyboardButton("💬 Chat Amoi Sini", callback_data="show_chat_options"), # Diubah ke Callback
            InlineKeyboardButton("🎮 Link Game", callback_data="show_links")
        ],
        [
            InlineKeyboardButton("❌ List Banned Game ❌", callback_data="show_banned_games")
        ]
    ])

# --- HANDLERS ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id

    my_tz = pytz.timezone('Asia/Kuala_Lumpur')
    my_time = datetime.now(my_tz).hour
    greeting = "Selamat Pagi" if 5 <= my_time < 12 else "Selamat Petang" if 12 <= my_time < 18 else "Selamat Malam"

    cursor.execute("SELECT user_id FROM users WHERE user_id=?", (user_id,))
    if not cursor.fetchone():
        cursor.execute("INSERT INTO users (user_id) VALUES (?)", (user_id,))
        conn.commit()

    welcome_msg = (
        "🏆🏆🏆🏆🏆🏆🏆🏆🏆🏆\n"
        "🎰 ✨ **GGWP MALAYSIA** ✨ 🎰\n"
        "🏆🏆🏆🏆🏆🏆🏆🏆🏆🏆\n\n"
        f"*{greeting}, BOSS {user.first_name.upper()}!* 👑🇲🇾\n"
        "Selamat datang ke platform paling 'steady' di Malaysia.\n\n"
        "⬇️ **TEKAN BUTANG DI BAWAH** ⬇️"
    )
    await update.message.reply_text(welcome_msg, reply_markup=get_main_keyboard(), parse_mode='Markdown')

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # 1. REGISTER OPTIONS
    if query.data == "show_register":
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🟢 WhatsApp Amoi", url="https://wa.me/60195472739?text=Amoi%20saya%20nak%20register%20%F0%9F%A5%B0%F0%9F%9A%80%F0%9F%92%B0"),
                InlineKeyboardButton("🔵 Telegram Admin", url="https://t.me/GGWP888Admin")
            ],
            [InlineKeyboardButton("⬅️ Kembali", callback_data="back_to_main")]
        ])
        await query.edit_message_text(text="👑 **PENDAFTARAN GGWP** 👑\n\nPilih platform untuk daftar, Bossku!", reply_markup=keyboard)

    # 2. CHAT OPTIONS (FITUR BARU)
    elif query.data == "show_chat_options":
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🟢 WhatsApp Chat", url="https://wa.me/60195472739"),
                InlineKeyboardButton("🔵 Telegram Chat", url="https://t.me/GGWP888Admin")
            ],
            [InlineKeyboardButton("⬅️ Kembali", callback_data="back_to_main")]
        ])
        await query.edit_message_text(text="💬 **HUBUNGI AMOI GGWP** 💬\n\nSila pilih platform untuk chat dengan kami!", reply_markup=keyboard)

    # 3. GAME LIST (REVISI)
    elif query.data == "show_game_list":
        game_list_text = (
            "👾🎮 **GGWP ROYAL CASINO GAME LIST** 🎮👾\n"
            "━━━━━━━━━━━━━━━━━━━━━\n\n"
            "🎰 **Mega888** (🔥 *HOT*)\n"
            "🎰 **Pussy888** (🔥 *HOT*)\n"
            "🎰 **EVO888** (🔥 *HOT*)\n"
            "🎰 **918 Kiss ORI** (🔥 *HOT*)\n\n"
            "✨ 918 Kiss Kaya | LPE | Newtown | GreatWall | Live22 | Joker\n\n"
            "━━━━━━━━━━━━━━━━━━━━━\n"
            "👑 *Pilih Game & Hantam Jackpot Sekarang!* 👑"
        )
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Kembali", callback_data="back_to_main")]])
        await query.edit_message_text(text=game_list_text, reply_markup=keyboard, parse_mode='Markdown')

    # 4. BONUS OPTIONS
    elif query.data == "show_bonus":
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🟢 WhatsApp Amoi", url="https://wa.me/60195472739?text=Amoi%20nak%20claim%20bonus%2027%25%20%F0%9F%A5%B0%F0%9F%8E%81%F0%9F%92%B0"),
                InlineKeyboardButton("🔵 Telegram Admin", url="https://t.me/GGWP888Admin")
            ],
            [InlineKeyboardButton("⬅️ Kembali", callback_data="back_to_main")]
        ])
        await query.edit_message_text(text="🎁 **CLAIM BONUS 27%** 🎁\n\nHubungi kami untuk claim bonus anda!", reply_markup=keyboard)

    # 5. ALL PROMOS
    elif query.data == "show_all_promos":
        promo_text = "💎 **PROMOTION MEMBER RASMI** 💎\n\n20% Daily | 5% Unlimited | 30% Recommend | 8% Rebate"
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Kembali", callback_data="back_to_main")]])
        await query.edit_message_text(text=promo_text, reply_markup=keyboard, parse_mode='Markdown')

    # 6. DEPOSIT INFO
    elif query.data == "show_deposit":
        deposit_text = "🚀 **INFO TERIMA DEPOSIT** 🚀\n\nSemua Bank | DuitNow | TNG | Pin Reload | Share Credit (No U-Mobile)"
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Kembali", callback_data="back_to_main")]])
        await query.edit_message_text(text=deposit_text, reply_markup=keyboard, parse_mode='Markdown')

    # 7. LINK GAME (SENARAI PENUH)
    elif query.data == "show_links":
        links_text = "🎰 **LIST LINK GAME** 🎰\n\n918Kiss | Mega888 | Pussy888 | Live22 | Joker | Newtown | Evo888"
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Kembali", callback_data="back_to_main")]])
        await query.edit_message_text(text=links_text, reply_markup=keyboard, parse_mode='Markdown', disable_web_page_preview=True)

    # 8. BANNED GAMES
    elif query.data == "show_banned_games":
        banned_text = "❌🚨 **BANNED GAME** 🚨❌\n\n🚫 King Derby | Thunderbolt | Motorbike | Roulette | Seaworld | MysteryBox"
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Kembali", callback_data="back_to_main")]])
        await query.edit_message_text(text=banned_text, reply_markup=keyboard, parse_mode='Markdown')

    # BACK TO MAIN
    elif query.data == "back_to_main":
        await query.edit_message_text(text="🏆 **GGWP MALAYSIA** 🏆\n\nSila pilih menu utama:", reply_markup=get_main_keyboard(), parse_mode='Markdown')

# --- MAIN ---
if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_callback))
    print("--- GGWP MALAYSIA BOT IS RUNNING ---")
    application.run_polling()
