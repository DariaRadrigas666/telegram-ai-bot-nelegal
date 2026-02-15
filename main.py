import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from openai import AsyncOpenAI

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    user_text = update.message.text
    try:
        response = await client.chat.completions.acreate(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": user_text}]
        )
        reply = response.choices[0].message.content
        await update.message.reply_text(reply)
    except Exception as e:
        await update.message.reply_text("Произошла ошибка при обработке запроса.")
        print(f"Error: {e}")

async def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    # Запуск polling без закрытия event loop
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    print("Бот запущен")
    # Ждём завершения приложения (например Ctrl+C)
    await app.updater.idle()
    await app.stop()
    await app.shutdown()

# --- запуск без asyncio.run() ---
loop = asyncio.get_event_loop()
loop.create_task(main())
loop.run_forever()

async def main():
    # Создаём приложение бота
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    # Регистрируем обработчик текстовых сообщений
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Запуск бота
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
