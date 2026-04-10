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
            InlineKeyboardButton("💬 Chat Amoi Sini", callback_data="show_chat_options"),
            InlineKeyboardButton("🎮 Link Game", callback_data="show_links")
        ],
        [
            InlineKeyboardButton("❌ List Banned Game ❌", callback_data="show_banned_games")
        ]
    ])

def get_greeting():
    my_tz = pytz.timezone('Asia/Kuala_Lumpur')
    my_time = datetime.now(my_tz).hour
    if 5 <= my_time < 12:
        return "Selamat Pagi"
    elif 12 <= my_time < 18:
        return "Selamat Petang"
    else:
        return "Selamat Malam"

def get_welcome_msg(first_name):
    greeting = get_greeting()
    return (
        "🏆🏆🏆🏆🏆🏆🏆🏆🏆🏆\n"
        "🎰 ✨ **GGWP MALAYSIA** ✨ 🎰\n"
        "🏆🏆🏆🏆🏆🏆🏆🏆🏆🏆\n\n"
        f"*{greeting}, BOSS {first_name.upper()}!* 👑🇲🇾\n"
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
        "━━━━━━━━━━━━━━━━━━━━━\n\n"
        "⬇️ **TEKAN DEKAT BAWAH** ⬇️"
    )

# --- HANDLERS ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    cursor.execute("SELECT user_id FROM users WHERE user_id=?", (user.id,))
    if not cursor.fetchone():
        cursor.execute("INSERT INTO users (user_id) VALUES (?)", (user.id,))
        conn.commit()

    await update.message.reply_text(
        get_welcome_msg(user.first_name),
        reply_markup=get_main_keyboard(),
        parse_mode='Markdown'
    )

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "show_register":
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🟢 WhatsApp Amoi", url="https://wa.me/60195472739?text=Amoi%20saya%20nak%20register%20%F0%9F%A5%B0%F0%9F%9A%80%F0%9F%92%B0"),
                InlineKeyboardButton("🔵 Telegram Amoi", url="https://t.me/GGWP888Admin")
            ],
            [InlineKeyboardButton("⬅️ Laman Utama", callback_data="back_to_main")]
        ])
        await query.edit_message_text(
            text="👑 **Join GGWP** 👑\n\nPilih platform untuk Join, Bossku!",
            reply_markup=keyboard,
            parse_mode='Markdown'
        )

    elif query.data == "show_chat_options":
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🟢 WhatsApp Amoi", url="https://wa.me/60195472739"),
                InlineKeyboardButton("🔵 Telegram Amoi", url="https://t.me/GGWP888Admin")
            ],
            [InlineKeyboardButton("⬅️ Laman Utama", callback_data="back_to_main")]
        ])
        await query.edit_message_text(
            text="💬 **HUBUNGI AMOI GGWP** 💬\n\nSila pilih platform untuk chat dengan kami!",
            reply_markup=keyboard,
            parse_mode='Markdown'
        )

    elif query.data == "show_game_list":
        game_list_text = (
            "👾🎮 **GGWP ROYAL CASINO GAME LIST** 🎮👾\n"
            "━━━━━━━━━━━━━━━━━━━━━\n\n"
            
            "🎰 **Mega888** 🔥 *HOT*\n"
            "🎰 **Pussy888** 🔥 *HOT*\n"
            "🎰 **EVO888** 🔥 *HOT*\n"
            "🎰 **918 Kiss ORI** 🔥 *HOT*\n\n"
            "✨ 918 Kiss Kaya\n"
            "✨ LPE (Lucky Palace)\n"
            "✨ Newtown\n"
            "✨ GreatWall\n"
            "✨ Live22\n"
            "✨ Joker123\n\n"
            "━━━━━━━━━━━━━━━━━━━━━\n"
            "👑 *Pilih Game & Mulai Bermain Sekarang!* 👑"
        )
        back_keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Laman Utama", callback_data="back_to_main")]])
        await query.edit_message_text(text=game_list_text, reply_markup=back_keyboard, parse_mode='Markdown')

    elif query.data == "show_bonus":
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🟢 WhatsApp Amoi", url="https://wa.me/60195472739?text=Amoi%20nak%20claim%20bonus%2027%25%20%F0%9F%A5%B0%F0%9F%8E%81%F0%9F%92%B0"),
                InlineKeyboardButton("🔵 Telegram Amoi", url="https://t.me/GGWP888Admin")
            ],
            [InlineKeyboardButton("⬅️ Laman Utama", callback_data="back_to_main")]
        ])
        await query.edit_message_text(
            text="🎁 **CLAIM BONUS 27%** 🎁\n\nHubungi kami untuk claim bonus anda!",
            reply_markup=keyboard,
            parse_mode='Markdown'
        )

    elif query.data == "show_all_promos":
        promo_text = (
            "🎊 **PROMOTION MEMBER RASMI** 🎊\n"
            "━━━━━━━━━━━━━━━━━━━━━\n\n"
            "💎 **Daily Bonus 20%**\n"
            "💎 **Unlimited Bonus 5%**\n"
            "💎 **Recommend Bonus 30%**\n"
            "💎 **Daily Rebate 8%**\n\n"
            "━━━━━━━━━━━━━━━━━━━━━\n"
            "✨ *Main secara rasmi untuk nikmati semua kelebihan ini!* ✨"
        )
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Laman Utama", callback_data="back_to_main")]])
        await query.edit_message_text(text=promo_text, reply_markup=keyboard, parse_mode='Markdown')

    elif query.data == "show_deposit":
        deposit_text = (
            "🚀 **TERIMA DEPOSIT** 🚀\n"
            "━━━━━━━━━━━━━━━━━━━━━\n\n"
            "💳 **TERIMA DEPOSIT SEMUA BANK**\n"
            "💰 **DUITNOW / QR**\n"
            "✨ **TOUCH N'GO EWALLET**\n\n"
            "🎫 **PIN RELOAD / TOPUP:**\n"
            "⇢ Digi | Celcom | Maxis | U-Mobile\n\n"
            "📲 **SHARE CREDIT:**\n"
            "⇢ Digi | Celcom | Maxis\n\n"
            "⚠️ **PERHATIAN:**\n"
            "❌ *Tidak terima share credit dari U-Mobile*\n\n"
            "━━━━━━━━━━━━━━━━━━━━━\n"
            "👇 *Sila hubungi Admin untuk nombor akaun!*"
        )
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Laman Utama", callback_data="back_to_main")]])
        await query.edit_message_text(text=deposit_text, reply_markup=keyboard, parse_mode='Markdown')

    elif query.data == "show_links":
        links_text = (
            "🎰 **LIST LINK GAME** 🎰\n"
            "━━━━━━━━━━━━━━━━━━━━━\n\n"
            "✨ **918KISS**\n"
            "Android & iOS: [KLIK SINI](https://yop1.918kiss.com/)\n\n"
            "✨ **MEGA888**\n"
            "Android & iOS: [KLIK SINI](https://m.mega166.com/mega/index.html)\n\n"
            "✨ **PUSSY888**\n"
            "Android & iOS: [KLIK SINI](https://ytl.pussy888.com/)\n\n"
            "✨ **LIVE22**\n"
            "Android: [KLIK SINI](https://live22474.com/Login)\n"
            "iOS: [KLIK SINI](https://botanica22.com/Login)\n\n"
            "✨ **918KAYA**\n"
            "Android & iOS: [KLIK SINI](http://download22.da31889.com/)\n\n"
            "✨ **JOKER**\n"
            "Android & iOS: [KLIK SINI](https://www.jokerapp888a.net/)\n\n"
            "✨ **NEWTOWN CASINO**\n"
            "Android: [KLIK SINI](https://cdn.newmax11.com/mobile.html)\n"
            "iOS: [KLIK SINI](https://www.nbig33.com/)\n\n"
            "✨ **EVO888**\n"
            "Android & iOS: [KLIK SINI](https://d.evo366.com/)\n\n"
            "━━━━━━━━━━━━━━━━━━━━━"
        )
        back_keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Laman Utama", callback_data="back_to_main")]])
        await query.edit_message_text(
            text=links_text,
            reply_markup=back_keyboard,
            parse_mode='Markdown',
            disable_web_page_preview=True
        )

    elif query.data == "show_banned_games":
        banned_text = (
            "❌ **LIST BANNED GAMES** ❌\n"
            "━━━━━━━━━━━━━━━━━━━━━\n\n"
            "⚜️ **918KISS / MEGA888 / 918KAYA**\n"
            "🙅 King Derby\n"
            "🙅 Thunderbolt\n"
            "🙅 Motorbike\n"
            "🙅 Roulette\n"
            "🙅 Seaworld\n\n"
            "⚜️ **XE88**\n"
            "🙅 Daily Job Mission\n"
            "🙅 King Derby\n"
            "🙅 Thunderbolt\n"
            "🙅 Motorbike\n"
            "🙅 Roulette\n"
            "🙅 MysteryBox\n\n"
            "⚜️ **PUSSY888**\n"
            "🙅 All Game 4D\n"
            "🙅 King Derby\n"
            "🙅 Thunderbolt\n"
            "🙅 Motorbike\n"
            "🙅 Seaworld\n\n"
            "⚜️ **JOKER**\n"
            "🙅 Powerbar\n\n"
            "━━━━━━━━━━━━━━━━━━━━━\n"
            "⚠️ *Jika bermain game di atas semasa ada bonus aktif, kredit akan di-BURN!*"
        )
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Laman Utama", callback_data="back_to_main")]])
        await query.edit_message_text(text=banned_text, reply_markup=keyboard, parse_mode='Markdown')

    elif query.data == "back_to_main":
        user = update.effective_user
        await query.edit_message_text(
            text=get_welcome_msg(user.first_name),
            reply_markup=get_main_keyboard(),
            parse_mode='Markdown'
        )

# --- MAIN ---
if __name__ == '__main__':
    if not BOT_TOKEN:
        print("ERROR: BOT_TOKEN not found!")
    else:
        application = ApplicationBuilder().token(BOT_TOKEN).build()
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CallbackQueryHandler(handle_callback))
        print("--- GGWP MALAYSIA BOT IS RUNNING ---")
        application.run_polling()
