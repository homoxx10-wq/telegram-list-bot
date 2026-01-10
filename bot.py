from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import json
import os

DATA_FILE = "queue.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"open": False, "users": []}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🟢 Open List", callback_data="open")],
        [InlineKeyboardButton("➕ Join List", callback_data="join")],
        [InlineKeyboardButton("📋 Show List", callback_data="show")],
        [InlineKeyboardButton("❌ Close List", callback_data="close")],
        [InlineKeyboardButton("🧹 Clear List", callback_data="clear")],
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📋 List Manager\nChoose:",
        reply_markup=keyboard()
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    data = load_data()
    user = q.from_user.first_name

    if q.data == "open":
        data["open"] = True
        save_data(data)
        await q.message.reply_text("✅ List is OPEN")

    elif q.data == "close":
        data["open"] = False
        save_data(data)
        await q.message.reply_text("❌ List is CLOSED")

    elif q.data == "clear":
        data["users"] = []
        save_data(data)
        await q.message.reply_text("🧹 List cleared")

    elif q.data == "join":
        if not data["open"]:
            await q.message.reply_text("❌ List is closed")
            return
        if user in data["users"]:
            await q.message.reply_text("⚠️ You are already in")
            return
        data["users"].append(user)
        save_data(data)
        await q.message.reply_text(f"✅ Added\nYour number: {len(data['users'])}")

    elif q.data == "show":
        if not data["users"]:
            await q.message.reply_text("📭 List empty")
            return
        text = "📋 List:\n\n"
        for i, name in enumerate(data["users"], 1):
            text += f"{i}. {name}\n"
        await q.message.reply_text(text)

app = ApplicationBuilder().token("PUT_BOT_TOKEN_HERE").build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))

app.run_polling()
