from aiogram import Bot, Dispatcher, types, executor
from config import TOKEN_API
from aiogram.dispatcher.filters.state import State, StatesGroup
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime

scheduler = AsyncIOScheduler(timezone='Asia/Colombo')

bot = Bot(TOKEN_API)
dp = Dispatcher(bot)

async def on_startup(_):
    print('Я здесь')

async def start_cmd_handler(bot: Bot):
    await bot.send_message(-954441708, f'У тебя все хорошо? Да или нет?')

@dp.message_handler(text='да')
async def start_cmd(message: types.Message):
    await bot.send_message(chat_id = -954441708, text='ну и чудненько')

@dp.message_handler(text='нет')
async def start_cmd(message: types.Message):
    await bot.send_message(chat_id = -954441708, text='если честно, мне все равно. Я просто спросил')

scheduler.add_job(start_cmd_handler, trigger='cron',
                  day_of_week=0,
                  hour=12,
                  minute=28,
                  kwargs={'bot': bot})
scheduler.start()

if __name__ == '__main__':
    executor.start_polling(dp,
                           skip_updates=True,
                           on_startup=on_startup)

