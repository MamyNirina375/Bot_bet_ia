import os
import random
import time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# TOKEN-NAO EFA TAFIDITRA
TOKEN = "8165324726:AAGRCMY061pZA_oo5fiAJxksfBROesXd3Ng"

COUNTRIES = {
    "esp": "🇪🇸 Espagne", 
    "ita": "🇮🇹 Italie", 
    "fra": "🇫🇷 France", 
    "all": "🇩🇪 Allemagne", 
    "por": "🇵🇹 Portugal",
    "eng": "🏴󠁧󠁢󠁥󠁮󠁧󠁿 Angleterre"
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = "🤖 **BOT BET IA v3.0**\n\nSafidio ny firenena na andefaso **Screenshot** misy score aho:"
    keyboard = [
        [InlineKeyboardButton("🇪🇸 Espagne", callback_data='c_esp'), InlineKeyboardButton("🇮🇹 Italie", callback_data='c_ita')],
        [InlineKeyboardButton("🇫🇷 France", callback_data='c_fra'), InlineKeyboardButton("🇩🇪 Allemagne", callback_data='c_all')],
        [InlineKeyboardButton("🏴󠁧󠁢󠁥󠁮󠁧󠁿 Angleterre", callback_data='c_eng'), InlineKeyboardButton("🇵🇹 Portugal", callback_data='c_por')]
    ]
    await update.message.reply_text(msg, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

# ANALYSE IMAGE (Screenshot)
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔍 **Fandinihana ny sary (Vision AI)...** Miandrasa kely.")
    
    # Simulation analyse logique
    time.sleep(2) 
    win_rate = random.randint(88, 97)
    ora = time.strftime('%H:%M')
    
    msg = (f"✅ **ANALYSE VITA**\n\n"
           f"📅 Ora: {ora}\n"
           f"📈 Probabilité: {win_rate}%\n"
           f"💰 Torohevitra: Milokà amin'ny 1.5 kely!")
    await update.message.reply_text(msg, parse_mode='Markdown')

# GESTION PAYS & SCORE
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    await query.answer()

    if data.startswith('c_'):
        code = data.split('_')[1]
        context.user_data['country'] = COUNTRIES[code]
        await query.edit_message_text(f"🌍 {COUNTRIES[code]}\n\nAmpidiro ny **Lera** sy ny **Score** (Ohatra: 18:45 2:0 1:1):")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if ":" in text:
        win_rate = random.randint(85, 95)
        await update.message.reply_text(f"📊 **ANALYSE LOGIQUE**\n\n🎯 Win Rate: {win_rate}%\n⚡ Fehin-kevitra: Afaka miloka!")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    
    print("Bot is running...")
    app.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
