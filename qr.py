from telegram import Update,InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters,CommandHandler,CallbackQueryHandler
import qrcode
import os

# TOKEN = "8275593957:AAGGWRzcIzevxlyKrGUH--MTkKfGyWfxt7Y"
TOKEN = os.environ.get("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔗 Website", callback_data="website")],
        [InlineKeyboardButton("📱 WhatsApp", callback_data="whatsapp")],
        [InlineKeyboardButton("📸 Instagram", callback_data="instagram")],
        [InlineKeyboardButton("📍 Location", callback_data="location")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "👇 Choose what you want to generate QR for:",
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "back":
        context.user_data.clear()
        await start(query, context)
        return   # ⬅️ خیلی مهم
    
    context.user_data["mode"] = query.data

    messages = {
        "website": "🌐 Send website URL:",
        "whatsapp": "📱 Send WhatsApp number (example: +989123456789):",
        "instagram": "📸 Send Instagram username (without @):",
        "location": "📍 Send Google Maps link:"
    }

    await query.message.reply_text(messages[query.data])



async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    mode = context.user_data.get("mode")

    if not mode:
        await update.message.reply_text("❗ Please choose an option first using /start")
        return

    if mode == "website":
        data = text

    elif mode == "whatsapp":
        number = text.replace("+", "").replace(" ", "")
        data = f"https://wa.me/{number}"

    elif mode == "instagram":
        username = text.replace("@", "")
        data = f"https://instagram.com/{username}"

    elif mode == "location":
        data = text  # Google Maps link

    else:
        await update.message.reply_text("❌ Unknown option")
        return

    img = qrcode.make(data)
    file_name = "qr.png"
    img.save(file_name)
    
    keyboard = [
    [InlineKeyboardButton("🔙 Back to Menu", callback_data="back")]
]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_photo(
    photo=open(file_name, "rb"),
    caption="✅ QR Code generated successfully",
    reply_markup=reply_markup
)

    os.remove(file_name)


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.add_handler(CommandHandler("start", start))
    
    app.add_handler(CallbackQueryHandler(button_handler))
    
    app.add_handler(CommandHandler("start", start))
    
    app.add_handler(CallbackQueryHandler(button_handler))
    
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    


    print("🤖 Bot is running v2...")
    app.run_polling()

if __name__ == "__main__":
    main()
