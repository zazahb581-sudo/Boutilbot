import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters
)

TOKEN = "8171808465:AAHp6TccNjcBy3W2iBiA54j-0AJppmZUmJU" 
ADMIN_ID = 8649975859

# ===== START =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [InlineKeyboardButton("🛒 Place Order", callback_data="place_order")],
        [InlineKeyboardButton("🟢 Buy USDT", callback_data="buy_usdt")],
        [InlineKeyboardButton("🟡 Buy BTC", callback_data="buy_btc")],
        [InlineKeyboardButton("💰 Prices", callback_data="prices")],
        [InlineKeyboardButton("🆘 Support", callback_data="support")]
    ]

    text = (
        "Welcome to Boutilbot Store\n\n"
        "Owner: ELEMINE AHOEIBIB\n"
        "Support: 34888115"
    )

    await update.message.reply_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ===== BUTTONS =====
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    q = update.callback_query
    await q.answer()

    data = q.data

    if data == "place_order":

        order_id = random.randint(10000, 99999)

        await q.message.reply_text(
            f"Order Created\n\n"
            f"Order ID: #{order_id}\n"
            f"Send payment to: 34888115"
        )

    elif data == "buy_usdt":
        await q.message.reply_text("Use Place Order first.")

    elif data == "buy_btc":
        await q.message.reply_text("Use Place Order first.")

    elif data == "prices":
        await q.message.reply_text("USDT: 1.05 USD")

    elif data == "support":
        await q.message.reply_text("Support: 34888115")

# ===== PHOTO =====
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user
    photo = update.message.photo[-1]

    await context.bot.send_photo(
        chat_id=ADMIN_ID,
        photo=photo.file_id,
        caption=f"Payment Screenshot\nUser: @{user.username}\nID: {user.id}"
    )

    await update.message.reply_text("Screenshot received ✅")

# ===== CHAT =====
async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = (update.message.text or "").lower().strip()
    user = update.effective_user

    # ❌ ignore empty or weird inputs
    if not text:
        return

    # ❌ ignore button texts (IMPORTANT FIX)
    button_words = ["place order", "buy usdt", "buy btc", "prices", "support"]
    if text in button_words:
        return

    # send to admin ONLY real chat messages
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"User @{user.username} ({user.id}):\n{text}"
    )

    # ===== AUTO REPLIES =====
    if "hello" in text or "hi" in text:
        await update.message.reply_text("Hello 👋")

    elif "price" in text:
        await update.message.reply_text("USDT: 1.05 USD")

    elif "payment" in text:
        await update.message.reply_text("Send screenshot + Order ID")

    elif "problem" in text:
        await update.message.reply_text("Support: 34888115")

    elif "bonjour" in text:
        await update.message.reply_text("Bonjour 👋")

    elif "مرحبا" in text:
        await update.message.reply_text("مرحبا 👋")

    else:
        await update.message.reply_text("How can I help you?")

# ===== MAIN =====
def main():

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))

    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_messages))

    print("Bot started")
    app.run_polling()

if __name__ == "__main__":
    main()