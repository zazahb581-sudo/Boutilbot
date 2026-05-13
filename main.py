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

    if q.data == "place_order":

        order_id = random.randint(10000, 99999)

        await q.message.reply_text(
            f"Order ID: #{order_id}\n\n"
            f"Send payment to:\n34888115"
        )

    elif q.data == "buy_usdt":

        await q.message.reply_text(
            "Use Place Order first."
        )

    elif q.data == "buy_btc":

        await q.message.reply_text(
            "Use Place Order first."
        )

    elif q.data == "prices":

        await q.message.reply_text(
            "USDT: 1.05 USD"
        )

    elif q.data == "support":

        await q.message.reply_text(
            "Support: 34888115"
        )

# ===== PHOTO =====
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    photo = update.message.photo[-1]

    await context.bot.send_photo(
        chat_id=ADMIN_ID,
        photo=photo.file_id,
        caption=(
            f"📸 Payment Screenshot\n\n"
            f"👤 User: @{user.username}\n"
            f"🆔 ID: {user.id}"
        )
    )

    await update.message.reply_text(
        "✅ Screenshot received.\nSupport will review your payment."
    )

# ===== CHAT =====
async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text.lower()

    user = update.effective_user

    # ===== SEND MESSAGE TO ADMIN =====
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=(
            f"📩 New Message\n\n"
            f"👤 User: @{user.username}\n"
            f"🆔 ID: {user.id}\n\n"
            f"💬 Message:\n{text}"
        )
    )

    # ===== AUTO REPLIES =====
    if "hello" in text or "hi" in text:

        await update.message.reply_text(
            "Hello 👋"
        )

    elif "price" in text:

        await update.message.reply_text(
            "USDT: 1.05 USD"
        )

    elif "payment" in text:

        await update.message.reply_text(
            "Send screenshot + Order ID"
        )

    elif "problem" in text:

        await update.message.reply_text(
            "Support: 34888115"
        )

    elif "bonjour" in text:

        await update.message.reply_text(
            "Bonjour 👋"
        )

    elif "مرحبا" in text:

        await update.message.reply_text(
            "مرحبا 👋"
        )

    else:

        await update.message.reply_text(
            "Type /start"
        )

# ===== MAIN =====
def main():

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_messages
        )
    )

    app.add_handler(
        MessageHandler(
            filters.PHOTO,
            handle_photo
        )
    )

    print("Bot started")

    app.run_polling()

if __name__ == "__main__":
    main()