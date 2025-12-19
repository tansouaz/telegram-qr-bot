from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import qrcode
import os

TOKEN = "8582274278:AAHly6OuFIFDOkH2P0yTdamDBVXRJsYBwKQ"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    # ساخت QR
    img = qrcode.make(text)

    file_name = "qr.png"
    img.save(file_name)

    # ارسال عکس
    await update.message.reply_photo(photo=open(file_name, "rb"))

    # پاک کردن فایل
    os.remove(file_name)

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
