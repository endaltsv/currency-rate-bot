import logging
from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest

from services.exchange import fetch_exchange_rates
from config import CHAT_ID, MESSAGE_ID

def format_exchange_message(rates):
    message_text = f"""
${rates['usd_rate']:.4f}₽  €{rates['eur_rate']:.4f}₽  ₺{rates['try_rate']:.4f}₽
₿{rates['btc_price']}$  ♦{rates['eth_price']}$  💎{rates['ton_price']}$
"""
    return message_text

class MessageUpdater:
    def __init__(self):
        self.message_id = MESSAGE_ID

    async def update_message(self, bot: Bot):
        rates = await fetch_exchange_rates()
        message_text = format_exchange_message(rates)
        try:
            await bot.edit_message_text(
                text=message_text,
                chat_id=CHAT_ID,
                message_id=self.message_id
            )
        except TelegramBadRequest as e:
            if "message is not modified" in str(e):
                pass
            else:
                logging.error(f"Ошибка при редактировании сообщения: {e}")
        except Exception as e:
            logging.error(f"Ошибка при редактировании сообщения: {e}")