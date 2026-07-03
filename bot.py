
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import os

TOKEN = os.getenv("TOKEN")

cart = {}

products = {
    "G01": "G01 أسود",
    "G02": "G02 أزرق",
    "G03": "G03 شفاف"
}

def total(user_id):
    return sum(cart.get(user_id, {}).values())

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🕶️ G01", callback_data="add_G01")],
        [InlineKeyboardButton("🕶️ G02", callback_data="add_G02")],
        [InlineKeyboardButton("🕶️ G03", callback_data="add_G03")],
        [InlineKeyboardButton("🛒 السلة", callback_data="cart")]
    ]

    await update.message.reply_text(
        "مرحبا في Infinity Optics 🕶️",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    uid = query.from_user.id

    if uid not in cart:
        cart[uid] = {}

    data = query.data

    if data.startswith("add_"):
        item = data.replace("add_", "")
        cart[uid][item] = cart[uid].get(item, 0) + 1
        await query.message.reply_text("✔ تمت الإضافة")

    elif data == "cart":
        t = total(uid)

        msg = "🛒 السلة:\n\n"

        for k, v in cart.get(uid, {}).items():
            msg += f"{products[k]} × {v}\n"

        msg += f"\n📦 المجموع: {t}/20"

        if t < 20:
            msg += "\n⚠️ الحد الأدنى 20 قطعة"
        else:
            msg += "\n✔ يمكنك الطلب"
            msg += "\n📩 WhatsApp: https://wa.me/213XXXXXXXX"

        await query.message.reply_text(msg)

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))

app.run_polling()
