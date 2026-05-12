from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "ضع_التوكن_هنا"
BANKILY_NUMBER = "ضع_رقم_بنكيلي_هنا"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("💰 Buy USDT", callback_data="usdt")],
        [InlineKeyboardButton("₿ Buy BTC", callback_data="btc")],
        [InlineKeyboardButton("🆘 Support", callback_data="support")]
    ]

    await update.message.reply_text(
        "Welcome to Boutil Exchange 🇲🇷\nBuy Crypto via Bankily",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    if q.data == "usdt":
        await q.message.reply_text(
            f"💰 Buy USDT\nSend amount you want.\nPay to Bankily: {BANKILY_NUMBER}\nSend screenshot after payment."
        )

    elif q.data == "btc":
        await q.message.reply_text(
            f"₿ Buy BTC\nSame process.\nBankily: {BANKILY_NUMBER}"
        )

    elif q.data == "support":
        await q.message.reply_text("Contact: @yourusername")

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(buttons))

print("Bot running...")
app.run_polling()
