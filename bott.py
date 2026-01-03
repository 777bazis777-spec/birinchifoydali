from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import requests
import os

TOKEN = "8330852154:AAGJ4iFum7-fl_MTmSwyZwC20a8x"

CITIES = {
    "Toshkent": "Tashkent",
    "Andijon": "Andijan",
    "Farg‘ona": "Fergana",
    "Marg‘ilon": "Margilan",
    "Namangan": "Namangan",
    "Samarqand": "Samarkand",
    "Buxoro": "Bukhara",
    "Navoiy": "Navoi",
    "Qarshi": "Karshi",
    "Termiz": "Termez",
    "Jizzax": "Jizzakh",
    "Guliston": "Gulistan",
    "Urganch": "Urgench",
    "Xiva": "Khiva",
    "Nukus": "Nukus",
    "Angren": "Angren",
    "Olmaliq": "Almalyk",
    "Chirchiq": "Chirchiq",
    "Qo‘qon": "Kokand",
    "Denov": "Denau",
    "Zarafshon": "Zarafshan",
    "Bekobod": "Bekabad",
    "Shahrisabz": "Shahrisabz"
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = []
    row = []
    for city in CITIES:
        row.append(InlineKeyboardButton(city, callback_data=city))
        if len(row) == 2:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)

    await update.message.reply_text(
        "📍 Shaharni tanlang:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

async def city_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    city_uz = query.data
    city_en = CITIES[city_uz]

    url = "https://api.aladhan.com/v1/timingsByCity"
    params = {
        "city": city_en,
        "country": "Uzbekistan",
        "method": 2
    }

    data = requests.get(url, params=params).json()["data"]["timings"]

    text = (
        f"🕌 *{city_uz} — Bugungi namoz vaqtlari*\n\n"
        f"🌅 Bomdod: {data['Fajr']}\n"
        f"☀️ Quyosh: {data['Sunrise']}\n"
        f"🕛 Peshin: {data['Dhuhr']}\n"
        f"🕒 Asr: {data['Asr']}\n"
        f"🌇 Shom: {data['Maghrib']}\n"
        f"🌙 Xufton: {data['Isha']}"
    )

    await query.edit_message_text(text, parse_mode="Markdown")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(city_selected))

app.run_polling()
