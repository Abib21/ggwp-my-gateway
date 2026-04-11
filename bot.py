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
            InlineKeyboardButton("🆔 REGISTER", callback_data="show_register"),
            InlineKeyboardButton("🚀 TERIMA DEPOSIT", callback_data="show_deposit")
        ],
        [
            InlineKeyboardButton("🎁 CLAIM BONUS 27%", callback_data="show_bonus"),
            InlineKeyboardButton("💰 PROMOTION", callback_data="show_all_promos")
        ],
        [
            InlineKeyboardButton("🎰 GAME LIST", callback_data="show_game_list"),
            InlineKeyboardButton("🎮 LINK GAME", callback_data="show_links")
        ],
        [
            InlineKeyboardButton("💬 CHAT AMOI", callback_data="show_chat_options"),
            InlineKeyboardButton("📢 BUKTI CUCI", url="https://t.me/ggwp888channel")
        ],
        [
            InlineKeyboardButton("💰 MAX/LIMIT CUCI", callback_data="show_max_cuci")
        ],
        [
            InlineKeyboardButton("❌ LIST BANNED GAME ❌", callback_data="show_banned_games")
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
    return f"""🏆 🏆 🏆 🏆 🏆 🏆 🏆 🏆 🏆 🏆
🎰 ✨ **GGWP MALAYSIA** ✨ 🎰
🏆 🏆 🏆 🏆 🏆 🏆 🏆 🏆 🏆 🏆

*{greeting}, BOSS {first_name.upper()}!* 👑 🇲🇾
🎁 **PROMOSI KHAS MEMBER BARU**

┌──────────────────────────┐
  💵 **MIN DEPOSIT** ⇢ *RM20*
  💰 **CLAIM BONUS** ⇢ *27% EXTRA*
  💳 **METHOD** ⇢ *BANKIN / DUITNOW*
└──────────────────────────┘

⚠️ **TERMA & SYARAT BONUS**
🚫 *Dilarang bermain Live Game*
🚫 *Dilarang bermain Banned Games*
‼️ **(Jika langgar, kredit akan di-BURN!)** ‼️

⚡ **SERVICE STATUS**
🔹 **CUCI (WD)** ⇢ 🟢 **PANTAS 3 MIN**
🔹 **TNG E-WALLET** ⇢ ⚡ **AUTO DEPOSIT**
━━━━━━━━━━━━━━━━━━━━━

⬇️ **TEKAN DEKAT BAWAH** ⬇️"""

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

    try:
        await query.delete_message()
    except:
        pass

    back_button = InlineKeyboardButton("⬅️ Laman Utama", callback_data="back_to_main")

    if query.data == "show_register":
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🟢 WhatsApp Amoi", url="https://wa.me/60195472739?text=Amoi%20saya%20nak%20register%20%F0%9F%A5%B0%F0%9F%9A%80%F0%9F%92%B0"),
                InlineKeyboardButton("🔵 Telegram Amoi", url="https://t.me/GGWP888Admin")
            ],
            [back_button]
        ])
        await context.bot.send_message(chat_id=query.message.chat_id, text="👑 **Join GGWP** 👑\n\nPilih platform untuk Join, Bossku!", reply_markup=keyboard, parse_mode='Markdown')

    elif query.data == "show_chat_options":
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🟢 WhatsApp Amoi", url="https://wa.me/60195472739"),
                InlineKeyboardButton("🔵 Telegram Amoi", url="https://t.me/GGWP888Admin")
            ],
            [back_button]
        ])
        await context.bot.send_message(chat_id=query.message.chat_id, text="💬 **HUBUNGI AMOI GGWP** 💬\n\nSila pilih platform untuk chat dengan kami!", reply_markup=keyboard, parse_mode='Markdown')

    elif query.data == "show_game_list":
        game_list_text = (
            "👑 🎰 **GGWP ROYAL CASINO** 🎰 👑\n"
            "✨ *Exclusive Game Selection* ✨\n"
            "━━━━━━━━━━━━━━━━━━━━━\n\n"
            "🔥 **TOP GACOR SEKARANG** 🔥\n"
            "🏆 **Mega888** ⇢ ⚡ [ *HOT* ]\n"
            "🏆 **Pussy888** ⇢ ⚡ [ *HOT* ]\n"
            "🏆 **EVO888** ⇢ ⚡ [ *HOT* ]\n"
            "🏆 **918 Kiss ORI** ⇢ ⚡ [ *HOT* ]\n\n"
            "💎 **PREMIUM CASINO SELECTION**\n"
            "⭐ 918 Kiss Kaya\n"
            "⭐ LPE (Lucky Palace)\n"
            "⭐ Newtown Casino\n"
            "⭐ GreatWall (GW99)\n"
            "⭐ Live22 Malaysia\n"
            "⭐ Joker123 Gaming\n\n"
            "━━━━━━━━━━━━━━━━━━━━━\n"
        )
        await context.bot.send_message(chat_id=query.message.chat_id, text=game_list_text, reply_markup=InlineKeyboardMarkup([[back_button]]), parse_mode='Markdown')

    elif query.data == "show_max_cuci":
        max_cuci_text = (
            "💰🤑 **GGWP ROYAL CASINO MAX BAYAR** 🤑💰\n\n"
            "*Turnover x2*\n\n"
            "💵 **Maximum Bayar**\n"
            "*(Via Telco/Reload Pin/Share Kredit)*\n\n"
            "💰 Topup Rm5 - Rm10 Max RM188\n"
            "💰 Topup Rm11 - Rm30 Max Rm388\n"
            "💰 Topup Rm31 - Rm50 Max Rm588\n"
            "💰 Topup Rm51 - Rm100 Max Rm888\n"
            "🔥 Topup Rm101 Keatas Max 1088\n\n"
            "*MIN IN RM5 | MIN CUCI RM100*\n"
            "━━━━━━━━━━━━━━━━━━━━━\n"
            "🏧 **Maximum Bayar**\n"
            "*(Via Bankin/TnG)*\n\n"
            "💰 IN Rm10 - Rm29 Max Rm888\n"
            "💰 IN Rm30 - Rm49 Max Rm1388\n"
            "💰 IN Rm50 - Rm99 Max Rm2388\n"
            "💰 IN Rm100 - Rm299 Max Rm8888\n"
            "💰 IN Rm300 - Rm499 Max Rm12888\n"
            "🔥 IN Rm500 ke atas Max Rm16888\n\n"
            "*MIN TOPUP 10 | MIN CUCI 50*\n\n"
            "⚠️ Bawa Bonus Hanya Boleh main Slot game Sahaja\n"
            "❗️ Live Game/Fish/Table Game No Bonus\n"
            "✔️ Janji Cuci, Janji Bayar\n"
            "✅ 24 jams & Trusted Company"
        )
        await context.bot.send_message(chat_id=query.message.chat_id, text=max_cuci_text, reply_markup=InlineKeyboardMarkup([[back_button]]), parse_mode='Markdown')

    elif query.data == "show_bonus":
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🟢 WhatsApp Amoi", url="https://wa.me/60195472739?text=Amoi%20nak%20claim%20bonus%2027%25%20🥰🎁💰"),
                InlineKeyboardButton("🔵 Telegram Amoi", url="https://t.me/GGWP888Admin")
            ],
            [back_button]
        ])
        await context.bot.send_message(chat_id=query.message.chat_id, text="🎁 **CLAIM BONUS 27%** 🎁\n\nHubungi kami untuk claim bonus anda!", reply_markup=keyboard, parse_mode='Markdown')

    elif query.data == "show_all_promos":
        text = "🎊 **PROMOTION MEMBER RASMI** 🎊\n━━━━━━━━━━━━━━━━━━━━━\n\nDaily 20% | Unlimited 5% | Recommend 30% | Rebate 8%"
        await context.bot.send_message(chat_id=query.message.chat_id, text=text, reply_markup=InlineKeyboardMarkup([[back_button]]), parse_mode='Markdown')

    elif query.data == "show_deposit":
        deposit_text = (
            "🚀 ⚡ **GGWP OFFICIAL DEPOSIT** ⚡ 🚀\n"
            "✨ *Fast Service • Trusted Agent* ✨\n"
            "━━━━━━━━━━━━━━━━━━━━━\n\n"
            "💳 **PERBANKAN TEMPATAN**\n"
            "⇢ *Semua Bank Malaysia Diterima*\n"
            "⇢ *Transfer Pantas & Selamat*\n\n"
            "💰 **E-WALLET & QR**\n"
            "⇢ **DuitNow / QR Pay** (Semua Bank)\n"
            "⇢ **Touch N'Go eWallet** (Auto Deposit)\n\n"
            "🎫 **PIN RELOAD / TOPUP**\n"
            "⇢ 🟡 Digi\n"
            "⇢ 🔵 Celcom\n"
            "⇢ 🔴 Maxis / Hotlink\n"
            "⇢ 🟠 U-Mobile\n\n"
            "📲 **SHARE CREDIT (TRANSFER)**\n"
            "⇢ ✅ Digi\n"
            "⇢ ✅ Celcom\n"
            "⇢ ✅ Maxis\n"
            "⚠️ *No U-Mobile Share Credit* ❌\n\n"
            "━━━━━━━━━━━━━━━━━━━━━\n"
            "‼️ **PENTING** ‼️\n"
            "👇 *Sila hubungi Admin untuk nomor akaun terkini!*\n"
            "✨ **Deposit Laju, Jackpot Padu!** ✨"
        )
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=deposit_text,
            reply_markup=InlineKeyboardMarkup([[back_button]]),
            parse_mode='Markdown'
        )

    # ✅ FIX 1: Correctly indented inside handle_callback (was outside the function before)
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
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=links_text,
            reply_markup=InlineKeyboardMarkup([[back_button]]),
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
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=banned_text,
            reply_markup=InlineKeyboardMarkup([[back_button]]),
            parse_mode='Markdown'
        )

    # ✅ FIX 2: Removed 2 duplicate "back_to_main" blocks, kept only one
    elif query.data == "back_to_main":
        user = update.effective_user
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=get_welcome_msg(user.first_name),
            reply_markup=get_main_keyboard(),
            parse_mode='Markdown'
        )

if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_callback))
    print("--- GGWP MALAYSIA BOT IS RUNNING ---")
    application.run_polling()
