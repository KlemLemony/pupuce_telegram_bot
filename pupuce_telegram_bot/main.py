# проблема в том, что он не отдает управление следующей функции. ПОЧЕМУ???

# сообщения должны приходить в общий чат
# если от бота два сообщения подряд, то между ними должен быть лаг в 1 секунду
# если вызываешь пупуся сам, он должен недовольно ответить, что иди нахуй - добавить хэндлер поверх всего, где будет просто текстово вызываться пупусь


from aiogram import Bot, Dispatcher, types, executor
from config import TOKEN_API
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta #timedelta возможно удали

storage: MemoryStorage = MemoryStorage()
scheduler = AsyncIOScheduler(timezone='Asia/Colombo')

bot = Bot(TOKEN_API)
dp = Dispatcher(bot,
                storage=storage)

async def on_startup(_):
    print('Я здесь')

class Form(StatesGroup):
    is_everything_ok = State()
    remember_oath = State()

@dp.message_handler(text='пупусь')
async def pupuce(message: types.Message):
    await message.answer("че надо? Иди нахуй")
    await asyncio.sleep(1)
    await bot.send_sticker(chat_id = -954441708, sticker='CAACAgIAAxkBAAEIKHFkEwiKU-xDCnNIoNFwUq37X88AAVgAAjYJAAJ5XOIJQ8ZQFdq6zjcvBA')

@dp.message_handler()
async def i_do_not_understand_you(message: types.Message):
    await message.answer("Отвали, я не хочу разговаривать")
    await asyncio.sleep(1)
    await bot.send_sticker(chat_id = -954441708, sticker='CAACAgIAAxkBAAEIKHNkEwnuXZE78S7NqncS2y4w0G4ylAACEgADNlhqEvnhF8xf8PntLwQ')

async def start_cmd_handler(bot: Bot):
    await bot.send_message(-954441708, f'У тебя все хорошо? Да или нет?')

@dp.message_handler()
async def test(message: types.Message):
    await message.answer("что?")

@dp.message_handler(text='да')
async def start_cmd(message: types.Message):
    await Form.is_everything_ok.set()
    await bot.send_message(chat_id = -954441708, text='ну и чудненько')
    await asyncio.sleep(2)
    await Form.remember_oath.set()
    await message.answer("Клятва на пальчиках в силе? Мы еще охана?")

@dp.message_handler(text='нет')
async def start_cmd(message: types.Message):
    await Form.is_everything_ok.set()
    await bot.send_message(chat_id = -954441708, text='если честно, мне все равно. Я просто спросил')
    await asyncio.sleep(2)
    await Form.remember_oath.set()
    await message.answer("Клятва на пальчиках в силе? Мы еще охана?")
    
@dp.message_handler(state=Form.remember_oath)
async def process_remember_oath(message: types.Message, state: FSMContext):
    if message.text.lower() == 'да':
        await message.answer("япикаееееей, мазафака. Тогда до встречи на следующей неделе! Счастья, здоровья тебе")
    elif message.text.lower() == 'нет':
        await message.answer("Пидор!")
    else:
        await message.answer("чего блять? Ты пожешь написать да или нет?")

    await state.finish()

scheduler.add_job(start_cmd_handler, 'cron',
                  day_of_week=4,
                  hour=13,
                  minute=30,
                  kwargs={'bot': bot})
scheduler.start()

if __name__ == '__main__':
    executor.start_polling(dp,
                           skip_updates=True,
                           on_startup=on_startup)
