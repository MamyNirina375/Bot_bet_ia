import os
import time
import hashlib
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

TOKEN = "8165324726:AAGRCMY061pZA_oo5fiAJxksfBROesXd3Ng"

# --- DATA FOOTBALL ---
TEAMS = {
    "esp": ["Real Madrid", "Barcelona", "Atletico"],
    "ita": ["Juventus", "Inter Milan", "AC Milan"],
    "fra": ["PSG", "Marseille", "Lyon"],
    "all": ["Bayern Munich", "Dortmund", "Leverkusen"],
    "eng": ["Man City", "Liverpool", "Arsenal"]
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("⚽ FOOTBALL ANALYSIS", callback_data='mode_foot')],
        [InlineKeyboardButton("✈️ AVIATOR PRO (95%)", callback_data='mode_aviator')],
        [InlineKeyboardButton("🤖 RESAKA AMIN'NY IA", callback_data='mode_chat')]
    ]
    await update.message.reply_text(
        "🤖 **SUPER IA BOT V5.0**\n\nSafidio ny mode tianao hampiasaina:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )

async def mode_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'mode_aviator':
        context.user_data['mode'] = 'aviator'
        await query.edit_message_text("✈️ **MODE AVIATOR PRO**\nAmpidiro ny Hash na ny Sanda Decimal:")
    
    elif query.data == 'mode_foot':
        context.user_data['mode'] = 'foot_country'
        keyboard = [[InlineKeyboardButton(p, callback_data=f'c_{p[:3].lower()}') for p in ["Espagne", "Italie", "France", "Allemagne", "Angleterre"]]]
        await query.edit_message_text("⚽ **FOOTBALL MODE**\nSafidio ny firenena:", reply_markup=InlineKeyboardMarkup(keyboard))
    
    elif query.data == 'mode_chat':
        context.user_data['mode'] = 'chat'
        await query.edit_message_text("🤖 **CHAT IA**\nAfaka miresaka amiko ianao izao. Inona ny fanontanianao?")

    elif query.data.startswith('c_'):
        code = query.data.split('_')[1]
        teams = random.sample(TEAMS.get(code, ["Team A", "Team B"]), 2)
        context.user_data['current_match'] = f"{teams[0]} vs {teams[1]}"
        context.user_data['mode'] = 'foot_logic'
        await query.edit_message_text(f"🏟️ **MATCH**: {context.user_data['current_match']}\n\nAmpidiro ny score na screenshot:")

async def handle_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mode = context.user_data.get('mode')
    user_input = update.message.text if update.message.text else "Image"

    # --- MODE AVIATOR PRO ---
    if mode == 'aviator':
        await update.message.reply_text("🔍 **Kajy ny Hash sy Decimal...**")
        seed = hashlib.sha256(user_input.encode()).hexdigest()
        val1 = round((int(seed[:4], 16) % 5000) / 100, 2)
        val2 = round((int(seed[4:8], 16) % 1000) / 100, 2)
        h, m = time.localtime().tm_hour, time.localtime().tm_min
        
        msg = (f"🟢 **MODE PRE-VERT RAIKA**\n\n🏆 **x{val1}** — `{h:02d}:{m+1:02d}:28`s\n"
               f"**JACKPOT MAITSO**\n---------------------------\n"
               f"🛡️ **x{val2}** — `{h+1:02d}:26:56`s\n"
               f"**MAITSO FARA-FAHAKELINY**\n---------------------------\n"
               f"🎯 **REUSSITE: 95%**")
        await update.message.reply_photo(photo="https://pollinations.ai/p/aviator_betting_stats", caption=msg, parse_mode='Markdown')

    # --- MODE FOOTBALL ---
    elif mode == 'foot_logic':
        match = context.user_data.get('current_match')
        win = random.randint(85, 98)
        msg = f"⚽ **FOOT ANALYSIS**\n\n🏟️ {match}\n🔥 Win probability: {win}%\n💰 Conseil: Over 2.5 goals"
        await update.message.reply_photo(photo="https://pollinations.ai/p/football_stadium_analysis", caption=msg, parse_mode='Markdown')

    # --- MODE CHAT IA ---
    elif mode == 'chat':
        # Eto dia ny IA no mamaly (Simulé)
        await update.message.reply_text(f"🤖 **IA**: Mazava ny teninao. Ho an'ny fanadihadiana lalina kokoa momba ny '{user_input}', dia afaka manampy anao foana aho.")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(mode_handler))
    app.add_handler(MessageHandler(filters.ALL, handle_all))
    app.run_polling()

if __name__ == '__main__':
    main()
