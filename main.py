import sqlite3
import base64
from openai import OpenAI

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters

# ================= CONFIG =================

TOKEN = "8171808465:AAHp6TccNjcBy3W2iBiA54j-0AJppmZUmJU"
OPENAI_KEY_BASE64 = "c2stcHJvai1uZVA0TTlpb1l2eGxlOXYwSGlGenQtVFhBSXVhVjFYNFkzSGpXdHBLSTF4em00QkNlTTJmbG8tQUwxODZ3bjkwRWlIcXlzRE9NaFQzQmxia0ZKZVh4blhpVTZDRnpKLXlPSlo1WE1IMWZUakFIWWxub1lWeWlpM0dadDl5WjR5YnB1bVdqMVcxOS03TTVDZUlvdXJ2Y1VnYVBPVUE="

OPENAI_API_KEY = base64.b64decode(OPENAI_KEY_BASE64).decode()

client = OpenAI(api_key=OPENAI_API_KEY)

ADMIN_ID = 8649975859

BTC_WALLET = "bc1qznuszsknaph068v0rzsalvhdw3vyk650n3vz7u"
BANKILY_NUMBER = "34888115"

# ================= DATABASE =================

conn = sqlite3.connect("system.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS wallet (
    user_id INTEGER PRIMARY KEY,
    balance REAL DEFAULT 0
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    status TEXT,
    reason TEXT
)
""")

conn.commit()

# ================= WALLET =================

def add_balance(user_id, amount):
    cursor.execute("""
    INSERT INTO wallet(user_id, balance)
    VALUES(?, ?)
    ON CONFLICT(user_id)
    DO UPDATE SET balance = balance + ?
    """, (user_id, amount, amount))
    conn.commit()

def get_balance(user_id):
    cursor.execute("SELECT balance FROM wallet WHERE user_id=?", (user_id,))
    row = cursor.fetchone()
    return row[0] if row else 0

# ================= AI =================

def analyze_payment_image(image_base64):

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a fraud detection AI. Return ONLY APPROVE or REJECT with short reason."
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Check this payment proof"},
                    {"type": "image_url", "image_url": {"url": image_base64}}
                ]
            }
        ]
    )

    return response.choices[0].message.content

# ================= HANDLERS =================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [InlineKeyboardButton("BTC", callback_data="btc")],
        [InlineKeyboardButton("BANKILY", callback_data="bankily")],
        [InlineKeyboardButton("WALLET", callback_data="wallet")],
        [InlineKeyboardButton("ADMIN", callback_data="admin")]
    ]

    await update.message.reply_text(
        "BOT ACTIVE",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    q = update.callback_query
    await q.answer()

    user_id = q.from_user.id

    if q.data == "btc":
        await q.message.reply_text(BTC_WALLET)

    elif q.data == "bankily":
        await q.message.reply_text(BANKILY_NUMBER)

    elif q.data == "wallet":
        await q.message.reply_text(f"{get_balance(user_id)}")

    elif q.data == "admin":

        if user_id != ADMIN_ID:
            await q.message.reply_text("NO ACCESS")
            return

        cursor.execute("SELECT COUNT(*) FROM logs")
        total = cursor.fetchone()[0]

        cursor.execute("SELECT SUM(balance) FROM wallet")
        total_wallet = cursor.fetchone()[0] or 0

        await q.message.reply_text(f"{total} {total_wallet}")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    file = await update.message.photo[-1].get_file()
    img = await file.download_as_bytearray()

    image_base64 = "data:image/png;base64," + base64.b64encode(img).decode()

    result = analyze_payment_image(image_base64)

    decision = "APPROVE" if "APPROVE" in result.upper() else "REJECT"

    cursor.execute(
        "INSERT INTO logs (user_id, status, reason) VALUES (?, ?, ?)",
        (user.id, decision, result[:300])
    )
    conn.commit()

    if decision == "APPROVE":
        add_balance(user.id, 10)
        await update.message.reply_text("APPROVED")
    else:
        await update.message.reply_text("REJECTED")

# ================= MAIN =================

def main():

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    print("RUNNING")
    app.run_polling()

if __name__ == "__main__":
    main()