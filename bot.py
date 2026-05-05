from datetime import datetime
from zoneinfo import ZoneInfo
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = "8770419775:AAFGT4G97akZr3ARdJpufRHg8luwLBmFTV8"

MOSCOW_TZ = ZoneInfo("Europe/Moscow")
TARGET = datetime(2026, 5, 15, 9, 0, 0, tzinfo=MOSCOW_TZ)


def format_remaining(delta):
    total_seconds = int(delta.total_seconds())

    if total_seconds <= 0:
        return "Время уже наступило!"

    days = total_seconds // 86400
    hours = total_seconds % 86400 // 3600
    minutes = total_seconds % 3600 // 60
    seconds = total_seconds % 60

    return f"Осталось: {days} дн. {hours} ч. {minutes} мин. {seconds} сек."


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Напиши /time, чтобы узнать, сколько осталось до 09:00 15 мая по Москве."
    )


async def time_left(update: Update, context: ContextTypes.DEFAULT_TYPE):
    now = datetime.now(MOSCOW_TZ)
    remaining = TARGET - now
    await update.message.reply_text(format_remaining(remaining))


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("time", time_left))

    app.run_polling()


if __name__ == "__main__":
    main()