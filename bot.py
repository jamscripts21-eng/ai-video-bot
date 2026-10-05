import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from runwayml import RunwayML

TELEGRAM_TOKEN = os.getenv("BOT_TOKEN")
RUNWAY_API_KEY = os.getenv("RUNWAYML_API_SECRET")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! 👋\n\n"
        "Я AI Video Bot 🎬\n"
        "Напиши:\n"
        "/video описание видео"
    )


async def video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = " ".join(context.args)

    if not prompt:
        await update.message.reply_text(
            "Напиши описание после /video.\n\n"
            "Например:\n"
            "/video робот идёт по ночному Токио"
        )
        return

    if not RUNWAY_API_KEY:
        await update.message.reply_text("❌ API ключ генератора не найден.")
        return

    await update.message.reply_text(
        "🎬 Начинаю генерацию видео...\n"
        "Это может занять некоторое время."
    )

    try:
        client = RunwayML(api_key=RUNWAY_API_KEY)

        task = client.text_to_video.create(
            model="gen4.5",
            prompt_text=prompt,
            ratio="1280:720",
            duration=5,
        )

        task = task.wait_for_task_output()

        video_url = task.output[0]

        await update.message.reply_video(
            video=video_url,
            caption="🎬 Готово!"
        )

    except Exception as e:
        print("ERROR:", e)
        await update.message.reply_text(
            "❌ Не удалось создать видео.\n"
            "Проверь настройки Runway API."
        )


def main():
    if not TELEGRAM_TOKEN:
        raise RuntimeError("BOT_TOKEN не найден")

    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("video", video))

    print("Бот запущен!")
    app.run_polling()


if __name__ == "__main__":
    main()
