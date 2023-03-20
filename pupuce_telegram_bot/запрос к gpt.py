# Ошибка возникает потому, что state не был передан в хэндлеры start_cmd и remember_oath. Вместо этого, state был передан в функцию
# start_cmd_handler, которая вызывается по расписанию с помощью AsyncIOScheduler. Поэтому в момент вызова хэндлеров, переменная state
# имеет значение None. Чтобы исправить эту ошибку, необходимо передавать state в хэндлеры напрямую, а не через start_cmd_handler. Для
# этого можно использовать декораторы @dp.callback_query_handler() или @dp.message_handler() без аргумента state. Внутри хэндлеров
# можно использовать FSMContext для работы со стейтами.

from aiogram import Bot, Dispatcher, types, executor
from config import TOKEN_API
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime

storage = MemoryStorage()
bot = Bot(TOKEN_API)
dp = Dispatcher(bot, storage=storage)
scheduler = AsyncIOScheduler(timezone='Asia/Colombo')

async def on_startup(_):
    print('Я здесь')

class Form(StatesGroup):
    is_everything_ok = State()
    remember_oath = State()

async def start_cmd_handler(bot: Bot):
    await bot.send_message(-954441708, f'У')
    await Form.is_everything_ok.set()

@dp.message_handler(text='да', state=Form.is_everything_ok)
async def start_cmd(message: types.Message, state: FSMContext):
    await bot.send_message(chat_id = -954441708, text='ну')
    await asyncio.sleep(2)
    await message.answer("Кл")
    await Form.next()

@dp.message_handler(text='да', state=Form.remember_oath)
async def start_cmd(message: types.Message, state: FSMContext):
    await bot.send_message(chat_id = -954441708, text='яп')
    await state.finish()

scheduler.add_job(start_cmd_handler, trigger='cron',
                  day_of_week=0,
                  hour=16,
                  minute=55,
                  kwargs={'bot': bot})
scheduler.start()

if __name__ == '__main__':
    executor.start_polling(dp,
                           skip_updates=True,
                           on_startup=on_startup)




