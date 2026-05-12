
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

import os
TOKEN = os.environ.get("TOKEN")

BANKILY_NUMBER = "34888115"
SUPPORT_EMAIL = "zazahb581@gmail.com"
CUSTOMER_SERVICE = "34888115"
OWNER_NAME = "ELEMINE AHOEIBIB"

USDT_RATE = "1 USDT ≈ 1.05 USD"
BTC_RATE = "Market Price (Live)"

# START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Buy USDT", callback_data="buy_usdt")],
        [InlineKeyboardButton("Buy BTC", callback_data="buy_btc")],
        [InlineKeyboardButton("Prices", callback_data="prices")],
        [InlineKeyboardButton("Support", callback_data="support")]
    ]

    text = f"""
Welcome to Boutil Exchange

Owner: {OWNER_NAME}
Customer Service: {CUSTOMER_SERVICE}
Email: {SUPPORT_EMAIL}

Pay via Bankily: {BANKILY_NUMBER}

Select an option below:
"""

    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

# BUTTONS
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    if q.data == "buy_usdt":
        await q.message.reply_text(
            f"BUY USDT\n\nSend amount to buy.\nPay via Bankily: {BANKILY_NUMBER}\nSend screenshot after payment."
        )

    elif q.data == "buy_btc":
        await q.message.reply_text(
            f"BUY BTC\n\nPay via Bankily: {BANKILY_NUMBER}\nMarket price applies."
        )

    elif q.data == "prices":
        await q.message.reply_text(
            f"PRICES\n\nUSDT: {USDT_RATE}\nBTC: {BTC_RATE}"
        )

    elif q.data == "support":
        await q.message.reply_text(
            f"SUPPORT\n\nOwner: {OWNER_NAME}\nEmail: {SUPPORT_EMAIL}\nService: 24/7"
        )

# RUN
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))

    print("Bot is running...")
    app.run_polling(close_loop=False)

if __name__ == "__main__":
    main()
