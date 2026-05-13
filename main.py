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

async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text.lower()

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

def main():

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_messages))

    print("Bot started")

    app.run_polling()

if __name__ == "__main__":
    main()