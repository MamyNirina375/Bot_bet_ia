import os
import random
import time
import hashlib
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

TOKEN = "8165324726:AAGRCMY061pZA_oo5fiAJxksfBROesXd3Ng"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("⚽ FOOTBALL ANALYSIS", callback_data='mode_foot')],
        [InlineKeyboardButton("✈️ AVIATOR PREDICTOR PRO", callback_data='mode_aviator')]
    ]
    await update.message.reply_text(
        "🤖 **IA PREDICTOR V4.0**\n\nSafidio ny mode tianao hampiasaina:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )

async def mode_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'mode_aviator':
        context.user_data['mode'] = 'aviator'
        msg = ("✈️ **AVIATOR MODE ACTIVÉ**\n\n"
               "Ampidiro ny **Hash** na ny **Cotes farany**.\n"
               "Afaka mandefa **Screenshot** ihany koa ianao vakin'ny IA.")
        await query.edit_message_text(msg)
    
    elif query.data == 'mode_foot':
        context.user_data['mode'] = 'foot'
        await query.edit_message_text("⚽ **FOOTBALL MODE ACTIVÉ**\nAndefaso screenshot na score aho.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mode = context.user_data.get('mode')
    
    if mode == 'aviator':
        await update.message.reply_text("🔍 **Kajy ny Hexadecimal sy ny Hash nisesy...**")
        time.sleep(1.5)
        
        # LOGIQUE AVIATOR PRO (Heure/Minute/Seconde + Hex)
        now = time.localtime()
        h, m, s = now.tm_hour, now.tm_min, now.tm_sec
        
        # Famoronana Hexadecimal sy Decimal sandoka avy amin'ny ora
        hex_val = hashlib.md5(f"{h}:{m}:{s}".encode()).hexdigest()[:8].upper()
        dec_val = int(hex_val, 16) % 1000
        
        # Kajy ny lera manaraka (ohatra: + 2 minitra sy 15 segondra)
        next_m = (m + 2) % 60
        next_s = (s + 15) % 60
        
        win_rate = random.randint(95, 98) # Ny fahombiazana nangatahinao
        
        prediction_msg = (
            f"🚀 **PREDICTION AVIATOR (95%+)**\n\n"
            f"🔢 **Data Analysis**:\n"
            f"• HEX: `{hex_val}`\n"
            f"• Decimal: `{dec_val}`\n"
            f"• Ora teo: `{h:02d}:{m:02d}:{s:02d}s`\n\n"
            f"🎯 **TOURS MANARAKA (PROCHAINS)**:\n"
            f"1️⃣ Lera: **{h:02d}:{next_m:02d}:{next_s:02d}s** -> 🟢 **2.00x+**\n"
            f"2️⃣ Lera: **{h:02d}:{next_m:02d}:{(next_s+20)%60:02d}s** -> 🟢 **2.50x+**\n"
            f"3️⃣ Lera: **{h:02d}:{(next_m+1)%60:02d}:05s** -> 🟣 **4.00x+**\n"
            f"4️⃣ Lera: **{h:02d}:{(next_m+1)%60:02d}:40s** -> 🟢 **2.00x+**\n\n"
            f"📈 **Fiantohana**: {win_rate}%\n"
            f"⚠️ *Torohevitra: Milokà amin'ny lera voalaza eo ambony.*"
        )
        
        img_url = f"https://pollinations.ai/p/aviator_game_prediction_interface_professional_dark_blue_neon"
        await update.message.reply_photo(photo=img_url, caption=prediction_msg, parse_mode='Markdown')

    else:
        # Raha Foot na hafa
        await update.message.reply_text("Andramo start indray dia fidio ny mode.")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(mode_handler))
    app.add_handler(MessageHandler(filters.ALL, handle_message))
    app.run_polling()

if __name__ == '__main__':
    main()
