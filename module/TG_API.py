# -*- coding: utf-8 -*-
"""
Модуль для отправки одной новости в Telegram
"""

import logging
import asyncio
from telegram import Bot
from telegram.ext import ApplicationBuilder

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Замените на Ваш реальный токен
TELEGRAM_BOT_TOKEN = "7890778236:AAEhZTtReO6pd30HuFjVqqUCRrAoTxmCQy0"

# Укажите идентификатор канала или имя пользователя канала (формат @channel_username)
CHANNEL_ID = "@Gazeta_ru_pars"  # Измените на свой канал

async def _send_single_news_async(title: str, url: str, channel_id: str, bot_token: str):
    """
    Вспомогательная асинхронная функция для отправки одной новости.
    """
    # Текст сообщения: сначала заголовок, потом ссылка
    message_text = f"{title}\n{url}"

    try:
        application = ApplicationBuilder().token(bot_token).build()
        bot: Bot = application.bot
        await bot.send_message(chat_id=channel_id, text=message_text)
        logging.info("Новость успешно отправлена.")
    except Exception as e:
        logging.error(f"Ошибка при отправке новости: {e}")

def send_news(news_item, channel_id: str = CHANNEL_ID, bot_token: str = TELEGRAM_BOT_TOKEN):
    """
    Синхронная функция для отправки одной новости.

    :param news_item: объект класса NewsItem (с атрибутами title, url, pub_time)
    :param channel_id: Telegram-канал (например, @my_channel или integer ID)
    :param bot_token: Токен Вашего бота
    """
    asyncio.run(_send_single_news_async(news_item.title, news_item.url, channel_id, bot_token))
