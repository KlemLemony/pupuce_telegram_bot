from aiogram import Bot, Dispatcher, types, executor
from config import TOKEN_API
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import random
from random import randint

storage = MemoryStorage()
bot = Bot(TOKEN_API)
dp = Dispatcher(bot, storage=storage)
scheduler = AsyncIOScheduler(timezone='Asia/Colombo')

async def on_startup(_):
    print('Я здесь')

async def start_cmd_handler(bot: Bot):
    await bot.send_message(335261939, text='Он тебя потерял')

scheduler.add_job(start_cmd_handler, trigger='cron',
                  day_of_week=1,
                  hour=16,
                  minute=00,
                  kwargs={'bot': bot})

scheduler.start()

if __name__ == '__main__':
    executor.start_polling(dp,
                           skip_updates=True,
                           on_startup=on_startup)
