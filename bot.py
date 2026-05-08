from datetime import datetime
from zoneinfo import ZoneInfo
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

import os
BOT_TOKEN = os.getenv("BOT_TOKEN")
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

    total_seconds = int(remaining.total_seconds())

    if total_seconds <= 0:
        await update.message.reply_text("Время уже наступило!")
        return

    days = total_seconds // 86400
    hours = total_seconds % 86400 // 3600
    minutes = total_seconds % 3600 // 60
    seconds = total_seconds % 60

    # Получаем участников чата
    chat = update.effective_chat
    admins = await context.bot.get_chat_administrators(chat.id)

    # Берем случайного участника из админов
    import random
    random_user = random.choice(admins).user

    # Формируем тег
    if random_user.username:
        mention = f"@{random_user.username}"
    else:
        mention = random_user.first_name

    text = (
        f"Осталось: {days} дн. "
        f"**{hours} ч. {minutes} мин. {seconds} сек.**\n\n"
        f"{mention}, в эту минуту ты главный Петушок!"
    )

    await update.message.reply_text(
        text,
        parse_mode="Markdown"
    )


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("time", time_left))

    app.run_polling()


if __name__ == "__main__":
    main()