import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! 👋\n"
        "Я AI Video Bot.\n\n"
        "Напиши /video и описание видео, которое хочешь создать."
    )

async def video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = " ".join(context.args)

    if not prompt:
        await update.message.reply_text(
            "Напиши описание после команды.\n\n"
            "Например:\n"
            "/video робот гуляет по футуристическому городу"
        )
        return

    await update.message.reply_text(
        f"🎬 Получил запрос:\n{prompt}\n\n"
        "Генератор видео пока подключаем..."
    )

def main():
    if not TOKEN:
        raise RuntimeError("BOT_TOKEN не найден")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("video", video))

    print("Бот запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()
