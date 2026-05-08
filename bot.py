import os
import random
from datetime import datetime
from zoneinfo import ZoneInfo

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes


BOT_TOKEN = os.getenv("BOT_TOKEN")

MOSCOW_TZ = ZoneInfo("Europe/Moscow")
TARGET = datetime(2026, 5, 15, 9, 0, 0, tzinfo=MOSCOW_TZ)


# Сюда вручную добавь участников группы
CHAT_MEMBERS = [
    "@TrustNikki",
    "@EvseevAleksandr",
    "@Dakon",
    "@MrKrakovich",
    "@Oleg_Smolnikov",
    "@starikovalex",
    "@schepyotkin",
    "@egor_kvach",
    "@Titov_1_Kirill",
    "@liukonenm",
    "@shilolad",
    "@timsay",
    "@zuevgeniy",
    "@mrKondrat"
]


def format_remaining(delta):
    total_seconds = int(delta.total_seconds())

    if total_seconds <= 0:
        return None

    days = total_seconds // 86400
    hours = total_seconds % 86400 // 3600
    minutes = total_seconds % 3600 // 60
    seconds = total_seconds % 60

    random_member = random.choice(CHAT_MEMBERS)

    return (
        f"Осталось: {days} дн. "
        f"<b>{hours} ч. {minutes} мин. {seconds} сек.</b>\n"
        f"{random_member}, в эту минуту ты главный Петушок!"
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Напиши /time, чтобы узнать, сколько осталось до 09:00 15 мая по Москве."
    )


async def time_left(update: Update, context: ContextTypes.DEFAULT_TYPE):
    now = datetime.now(MOSCOW_TZ)
    remaining = TARGET - now

    text = format_remaining(remaining)

    if text is None:
        await update.message.reply_text("Время уже наступило!")
        return

    await update.message.reply_text(
        text,
        parse_mode="HTML"
    )


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("time", time_left))

    app.run_polling()


if __name__ == "__main__":
    main()