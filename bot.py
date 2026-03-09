from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8765748447:AAHtFbahkahDWxilDO9uvGo__eBwsLlJfMM"

menu = {
    "Lavash": 28000,
    "Burger": 25000,
    "Hot Dog": 15000,
    "Cola": 8000
}

user_orders = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["Lavash", "Burger"], ["Hot Dog", "Cola"], ["/order"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "🍔 Evos menyusi\nOvqat tanlang:",
        reply_markup=reply_markup
    )

async def menu_select(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user.id
    text = update.message.text

    if text in menu:
        if user not in user_orders:
            user_orders[user] = []

        user_orders[user].append(text)

        await update.message.reply_text(f"✅ {text} savatchaga qo‘shildi")

async def order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user.id

    if user not in user_orders:
        await update.message.reply_text("❌ Savatcha bo‘sh")
        return

    items = user_orders[user]

    total = sum(menu[item] for item in items)

    text = "🛒 Sizning buyurtma:\n"

    for item in items:
        text += f"• {item} - {menu[item]} so'm\n"

    text += f"\n💰 Jami: {total} so'm"

    await update.message.reply_text(text)

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("order", order))
app.add_handler(MessageHandler(filters.TEXT, menu_select))

app.run_polling()