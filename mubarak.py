import requests
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters


TOKEN = "8341569619:AAGnm6A8p63yzt74RsMDto7n0UqAN1j5bwg"
TARGET_PRICE = 0.01200  

current_price_global = 0
chat_id_global = 436301406
alert_sent = False



def get_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=mubarak&vs_currencies=usd"
    response = requests.get(url)
    data = response.json()
    return float(data["mubarak"]["usd"])



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global chat_id_global
    chat_id_global = update.effective_chat.id

    keyboard = [["قیمت الان مبارک"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "ربات فعال شد ✅",
        reply_markup=reply_markup
    )



async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "قیمت الان مبارک":
        price = get_price()
        await update.message.reply_text(f"💰 قیمت فعلی مبارک: ${price:.8f}")



async def price_checker(context: ContextTypes.DEFAULT_TYPE):
    global current_price_global, chat_id_global, alert_sent

    if chat_id_global is None:
        return

    try:
        price = get_price()
        print("قیمت فعلی:", price)

        # اگر به تارگت رسید و قبلاً هشدار نداده
        if price >= TARGET_PRICE and not alert_sent:
            alert_sent = True

            for i in range(10):
                await context.bot.send_message(
                    chat_id=chat_id_global,
                    text=f"🚀🚀🚀 به تارگت رسید!\nقیمت: ${price:.8f}"
                )

        # اگر دوباره زیر تارگت رفت → اجازه هشدار مجدد
        if price < TARGET_PRICE:
            alert_sent = False

        current_price_global = price

    except Exception as e:
        print("خطا در گرفتن قیمت:", e)



app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, button_handler))

app.job_queue.run_repeating(price_checker, interval=60, first=10)

print("ربات روشن شد...")
app.run_polling()
