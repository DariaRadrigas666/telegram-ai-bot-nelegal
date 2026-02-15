import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from openai import AsyncOpenAI

# Инициализация клиента OpenAI
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Токен телеграма
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None or update.message.text is None:
        return  # Игнорируем пустые сообщения

    user_text = update.message.text

    try:
        # Асинхронный вызов OpenAI API
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
    # Создаём приложение бота
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    # Регистрируем обработчик текстовых сообщений
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Запуск бота
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
