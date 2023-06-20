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

class Form(StatesGroup):
    is_everything_ok = State()
    remember_oath = State()

async def start_cmd_handler(bot: Bot):
    await bot.send_message(5992630905, f'У тебя все хорошо? Да или нет?')
    await dp.current_state(chat=5992630905, user=335261939).set_state(Form.is_everything_ok)

@dp.message_handler(text='да', state=Form.is_everything_ok)
async def start_cmd(message: types.Message, state: FSMContext):
    await bot.send_message(chat_id = 5992630905, text='ну и чудненько')
    await asyncio.sleep(2)
    await message.answer("Клятва на пальчиках в силе? Мы еще охана?")
    await Form.next()

@dp.message_handler(text='нет', state=Form.is_everything_ok)
async def start_cmd(message: types.Message, state: FSMContext):
    await bot.send_message(chat_id = 5992630905, text='если честно, мне все равно. Я просто спросил')
    await asyncio.sleep(2)
    await message.answer("Клятва на пальчиках в силе? Мы еще охана?")
    await Form.next()

@dp.message_handler(state=Form.is_everything_ok)
async def start_cmd(message: types.Message, state: FSMContext):
    await bot.send_message(chat_id = 5992630905, text='я тебя не понимаю')
    #await asyncio.sleep(1)
    await bot.send_sticker(chat_id = 5992630905, sticker='CAACAgIAAxkBAAEIKHNkEwnuXZE78S7NqncS2y4w0G4ylAACEgADNlhqEvnhF8xf8PntLwQ')

@dp.message_handler(text='да', state=Form.remember_oath)
async def start_cmd(message: types.Message, state: FSMContext):
    await bot.send_message(chat_id = 5992630905, text='япикаееееей, мазафака. Тогда до встречи на следующей неделе! Счастья, здоровья тебе')
    await state.finish()

@dp.message_handler(text='нет', state=Form.remember_oath)
async def start_cmd(message: types.Message, state: FSMContext):
    await bot.send_message(chat_id = 5992630905, text='Пидор')
    await state.finish()

@dp.message_handler(state=Form.remember_oath)
async def start_cmd(message: types.Message, state: FSMContext):
    await bot.send_message(chat_id = 5992630905, text='чего блять? Ты пожешь написать да или нет?')
    
@dp.message_handler(text=['пупусь','pupuce', 'пу', 'Пупусь','Pupuce', 'Пу', 'Пупусь!', 'пупусь!'])
async def pupuce(message: types.Message):
    await message.answer("че надо? Иди нахуй")
    await asyncio.sleep(1)
    await bot.send_sticker(chat_id = 5992630905, sticker='CAACAgIAAxkBAAEIKHFkEwiKU-xDCnNIoNFwUq37X88AAVgAAjYJAAJ5XOIJQ8ZQFdq6zjcvBA')

#@dp.message_handler()
#async def go_fuck_yourself(message: types.Message):
#    await message.answer("Отвали, я не хочу разговаривать")
#    await asyncio.sleep(1)
#    await bot.send_sticker(chat_id = -1001610055755, sticker='CAACAgIAAxkBAAEIKHNkEwnuXZE78S7NqncS2y4w0G4ylAACEgADNlhqEvnhF8xf8PntLwQ')

#scheduler.add_job(start_cmd_handler, trigger='cron',
#                  day_of_week=1,
#                  hour=11,
#                  minute=7,
#                  kwargs={'bot': bot})

scheduler.add_job(start_cmd_handler, trigger='interval',
                  minutes=10,
                  kwargs={'bot': bot})

scheduler.start()

if __name__ == '__main__':
    executor.start_polling(dp,
                           skip_updates=True,
                           on_startup=on_startup)