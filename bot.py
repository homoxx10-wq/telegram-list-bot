from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = "8291160805:AAFGCJLQngyFsVDJGQjkP_qnH2GOIDuDI68"  # <-- Replace this with the token you got from BotFather

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I am your Turn Bot!")

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))

print("Bot is ready!")

app.run_polling()
