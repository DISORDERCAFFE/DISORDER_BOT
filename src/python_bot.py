import os
import asyncio
from datetime import datetime
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from deepseek_api import ask_mudrets  # Мой модуль для DeepSeek

# Стильная клава
KEYBOARD = [
    ["📜 Правила", "⚡️ Фишки"],
    ["🧙‍♂️ Спросить Мудрецов", "🎵 Найти трек"],
    ["📮 Кинуть месседж в Кафешку"]
]

async def start(update: Update, context):
    await update.message.reply_text(
        "🍵 Йоу! Я бот от DISORDER CAFFE\nВыбирай действие:",
        reply_markup=ReplyKeyboardMarkup(KEYBOARD, resize_keyboard=True)
    )

async def handle_msg(update: Update, context):
    user = update.effective_user  # Ловим всю инфу о юзере
    msg = update.message.text

    if msg == "📜 Правила":
        await update.message.reply_text("1. Не спамить\n2. Чтить Устав Кафе")

    elif msg == "⚡️ Фишки":
        await update.message.reply_text("Я умею:\n- Грузить треки\n- Консультироваться с Мудрецами\n- Передавать месседжи")

    elif msg == "🧙‍♂️ Спросить Мудрецов":
        await update.message.reply_text("Задай вопрос Мудрецам Востока:")
        context.user_data["awaiting_question"] = True

    elif msg == "🎵 Найти трек":
        await update.message.reply_text("Кидай название трека или исполнителя:")
        context.user_data["awaiting_song"] = True

    elif msg == "📮 Кинуть месседж в Кафешку":
        await update.message.reply_text("Чё передать админам? Пиши:")
        context.user_data["awaiting_feedback"] = True

    elif context.user_data.get("awaiting_question"):
        answer = await ask_mudrets(msg)  # Отправляем вопрос Мудрецам
        await update.message.reply_text(f"🧙‍♂️ Ответ Мудрецов:\n\n{answer}")
        context.user_data["awaiting_question"] = False

    elif context.user_data.get("awaiting_song"):
        # Тут будет поиск музыки
        await update.message.reply_text(f"🔊 Ищу: {msg}...")
        await update.message.reply_text("🎧 Вот что нашёл: [ссылка на трек]")
        context.user_data["awaiting_song"] = False

    elif context.user_data.get("awaiting_feedback"):
        # Формируем полный отчёт о юзере
        user_info = f"""
        ⚠️ НОВОЕ СООБЩЕНИЕ ОТ ЮЗЕРА ⚠️
        ├ ID: {user.id}
        ├ Юзернейм: @{user.username}
        ├ Имя: {user.full_name}
        ├ Язык: {user.language_code}
        ├ Рега: {user.link}
        └ Сообщение: {msg}
        """
        await context.bot.send_message(
            chat_id=os.getenv("ADMIN_ID"),
            text=user_info
        )
        await update.message.reply_text("✅ Месседж долетел до Кафешки!")
        context.user_data["awaiting_feedback"] = False

if __name__ == "__main__":
    app = Application.builder().token(os.getenv("BOT_TOKEN")).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT, handle_msg))
    app.run_polling()