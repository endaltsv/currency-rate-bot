import asyncio
import logging

from bot.bot import bot, dp, message_updater
from utils.scheduler import scheduler

logging.basicConfig(level=logging.INFO)

async def on_startup():
    scheduler.start()
    scheduler.add_job(
        message_updater.update_message,
        'interval',
        seconds=5,
        args=[bot]
    )

async def main():
    await on_startup()
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
