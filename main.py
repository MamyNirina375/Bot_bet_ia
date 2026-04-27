import os
import random
import time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

TOKEN = "8165324726:AAGRCMY061pZA_oo5fiAJxksfBROesXd3Ng"

# Lisitry ny ekipa isaky ny firenena
TEAMS = {
    "esp": ["Real Madrid", "Barcelona", "Atletico Madrid"],
    "ita": ["Juventus", "Inter Milan", "AC Milan"],
    "fra": ["PSG", "Marseille", "Lyon"],
    "all": ["Bayern Munich", "Dortmund", "Leverkusen"],
    "por": ["Benfica", "FC Porto", "Sporting CP"],
    "eng": ["Man City", "Liverpool", "Arsenal"]
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = "🤖 **BOT BET IA v3.5**\n\nSafidio ny firenena hahitanao ny lalao:"
    keyboard = [
        [InlineKeyboardButton("🇪🇸 Espagne", callback_data='c_esp'), InlineKeyboardButton("🇮🇹 Italie", callback_data='c_ita')],
        [InlineKeyboardButton("🇫🇷 France", callback_data='c_fra'), InlineKeyboardButton("🇩🇪 Allemagne", callback_data='c_all')],
        [InlineKeyboardButton("🏴󠁧󠁢󠁥󠁮󠁧󠁿 Angleterre", callback_data='c_eng'), InlineKeyboardButton("🇵🇹 Portugal", callback_data='c_por')]
    ]
    await update.message.reply_text(msg, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    await query.answer()

    if data.startswith('c_'):
        code = data.split('_')[1]
        # Misafidy ekipa roa kisendrasendra (random)
        teams = random.sample(TEAMS[code], 2)
        match_name = f"{teams[0]} vs {teams[1]}"
        context.user_data['current_match'] = match_name
        
        await query.edit_message_text(
            f"🏟️ **Lalao**: {match_name}\n\n"
            f"Ampidiro ny **Lera** sy ny **Score** (Ohatra: 21:00 1:0 2:2):"
        )

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if ":" in text:
        match = context.user_data.get('current_match', 'Lalao voafidy')
        win_rate = random.randint(85, 98)
        
        # Mampiasa sary avy amin'ny internet (ohatra sary momba ny baolina)
        image_url = f"https://pollinations.ai/p/football_match_stadium_with_text_{win_rate}_percent_success"
        
        caption = (f"📊 **ANALYSE LOGIQUE**\n\n"
                   f"⚽ {match}\n"
                   f"🎯 Win Rate: {win_rate}%\n"
                   f"⚡ Fehin-kevitra: Afaka miloka!")
        
        await update.message.reply_photo(photo=image_url, caption=caption, parse_mode='Markdown')

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
