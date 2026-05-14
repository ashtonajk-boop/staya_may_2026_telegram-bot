import os
import random
from datetime import datetime
from zoneinfo import ZoneInfo

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes


BOT_TOKEN = os.getenv("BOT_TOKEN")

MOSCOW_TZ = ZoneInfo("Europe/Moscow")
TARGET = datetime(2026, 5, 15, 9, 0, 0, tzinfo=MOSCOW_TZ)


NOT_GOING_MEMBERS = [
    "@Dakon",
    "@starikovalex",
    "@egor_kvach",
    "@Titov_1_Kirill",
    "@mrKondrat",
]


ROAST_TEMPLATES = [
    "Через {seconds} сек. ребята поедут тусить, а {user} будет дома грустить.",
    "Через {seconds} сек. стая выдвигается, а {user} остаётся охранять диван.",
    "Через {seconds} сек. начнётся легенда, а {user} будет смотреть сторис и делать вид, что всё нормально.",
    "Через {seconds} сек. ребята уедут за приключениями, а {user} — максимум до холодильника.",
    "Через {seconds} сек. тусовка стартует, а {user} официально назначается главным домашним наблюдателем.",
    "Через {seconds} сек. стая будет в движении, а {user} — в пледе.",
    "Через {seconds} сек. начнётся веселье, а {user} будет выбирать, какой сериал не спасёт этот вечер.",
    "Через {seconds} сек. ребята поедут шуметь, а {user} будет тихо завидовать из дома.",
    "Через {seconds} сек. стая соберётся, а {user} останется в режиме «ну я мысленно с вами».",
    "Через {seconds} сек. все будут делать историю, а {user} будет делать чай.",
    "Через {seconds} сек. ребята поедут отдыхать, а {user} будет отдыхать от собственной решительности.",
    "Через {seconds} сек. стая выезжает, а {user} получает почётный титул пропускатора года.",
    "Через {seconds} сек. начнётся движ, а {user} будет двигать только курсор мышки.",
    "Через {seconds} сек. все будут на тусе, а {user} будет наедине с тишиной и неправильным выбором.",
    "Через {seconds} сек. ребята стартуют, а {user} остаётся дома репетировать фразу «в следующий раз точно».",
    "Через {seconds} сек. стая поедет кайфовать, а {user} будет кайфовать от отсутствия кайфа.",
    "Через {seconds} сек. тусовка начнётся, а {user} будет главным зрителем чужого веселья.",
    "Через {seconds} сек. ребята уедут, а {user} останется дома как DLC, которое никто не скачал.",
    "Через {seconds} сек. стая будет на месте, а {user} будет на месте преступления против веселья.",
    "Через {seconds} сек. начнётся праздник, а {user} будет праздновать день упущенных возможностей.",
    "Через {seconds} сек. ребята поедут тусить, а {user} будет дома грустить так громко, что соседи поймут.",
    "Через {seconds} сек. стая выдвигается, а {user} остаётся в резерве. Очень глубоком резерве.",
    "Через {seconds} сек. движ начнётся, а {user} будет легендой только в чате.",
    "Через {seconds} сек. все будут на охоте за весельем, а {user} — на охоте за зарядкой.",
    "Через {seconds} сек. ребята уедут в историю, а {user} останется в черновиках.",
    "Через {seconds} сек. стая будет жить моментом, а {user} будет жить с мыслью «зря не поехал».",
    "Через {seconds} сек. начнётся настоящий съезд, а {user} будет съезжать с темы дома.",
    "Через {seconds} сек. все будут в движении, а {user} — в статусе «не беспокоить, я страдаю».",
    "Через {seconds} сек. ребята поедут делать контент, а {user} будет ставить лайки сквозь слёзы.",
    "Через {seconds} сек. стая стартует, а {user} остаётся дома — зато без риска стать легендой.",
]


def format_remaining(delta):
    total_seconds = int(delta.total_seconds())

    if total_seconds <= 0:
        return None

    days = total_seconds // 86400
    hours = total_seconds % 86400 // 3600
    minutes = total_seconds % 3600 // 60
    seconds = total_seconds % 60

    random_user = random.choice(NOT_GOING_MEMBERS)
    roast_template = random.choice(ROAST_TEMPLATES)
    roast_text = roast_template.format(
        user=random_user,
        seconds=total_seconds
    )

    return (
        f"Осталось: {days} дн. "
        f"<b>{hours} ч. {minutes} мин. {seconds} сек.</b>\n\n"
        f"{roast_text}"
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