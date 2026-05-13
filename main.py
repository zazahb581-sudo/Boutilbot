import os
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

TOKEN = "8171808465:AAHp6TccNjcBy3W2iBiA54j-0AJppmZUmJU"

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
        "💼 Welcome to Boutilbot Store\n\n"
        "👤 Owner: ELEMINE AHOEIBIB\n"
        "🏪 Virtual Crypto Exchange\n\n"
        "📞 Support: 34888115 (24/7)\n"
        "📧 Email: zazahb581@gmail.com\n\n"
        "Choose an option below:"
    )

    await update.message.reply_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ===== BUTTONS =====
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    q = update.callback_query
    await q.answer()

    # PLACE ORDER
    if q.data == "place_order":

        order_id = random.randint(10000, 99999)

        await q.message.reply_text(
            f"🛒 Order Created Successfully\n\n"
            f"📦 Order ID: #{order_id}\n\n"
            f"💳 Payment Method: Bankily\n"
            f"📱 Number: 34888115\n\n"
            f"📌 Instructions:\n"
            f"1. Send payment via Bankily\n"
            f"2. Take screenshot of payment\n"
            f"3. Send screenshot + Order ID to support\n\n"
            f"⚠️ Orders without Order ID will not be processed."
        )

    # BUY USDT
    elif q.data == "buy_usdt":

        await q.message.reply_text(
            "🟢 USDT Purchase\n\n"
            "Use Place Order button first."
        )

    # BUY BTC
    elif q.data == "buy_btc":

        await q.message.reply_text(
            "🟡 BTC Purchase\n\n"
            "Use Place Order button first."
        )

    # PRICES
    elif q.data == "prices":

        await q.message.reply_text(
            "💰 Current Prices\n\n"
            "USDT: 1.05 USD\n"
            "BTC: Market Price"
        )

    # SUPPORT
    elif q.data == "support":

        await q.message.reply_text(
            "🆘 Customer Support (24/7)\n\n"
            "📞 Phone: 34888115\n"
            "📧 Email: zazahb581@gmail.com\n\n"
            "👤 Owner: ELEMINE AHOEIBIB\n"
            "🏪 Store: Boutilbot"
        )

# ===== MAIN =====
def main():

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))

    print("Bot started")

    app.run_polling()

if __name__ == "__main__":
    main()
