# проблема в том, что он не отдает управление следующей функции. ПОЧЕМУ???

# сообщения должны приходить в общий чат
# если от бота два сообщения подряд, то между ними должен быть лаг в 1 секунду

# если вызываешь пупуся сам, он должен недовольно ответить, что иди нахуй

# проверка

from aiogram import Bot, Dispatcher, types, executor
from config import TOKEN_API
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
import asyncio

storage: MemoryStorage = MemoryStorage()

bot = Bot(TOKEN_API)
dp = Dispatcher(bot,
                storage=storage)

async def on_startup(_):
    print('Я здесь')

class Form(StatesGroup):
    is_everything_ok = State()
    remember_oath = State()

@dp.message_handler(commands='pupuce')
async def start_cmd_handler(message: types.Message):
    await Form.is_everything_ok.set()
    await bot.send_message(chat_id = -954441708, text='У тебя все хорошо?')

@dp.message_handler(state=Form.is_everything_ok)
async def process_is_everything_ok(message: types.Message, state: FSMContext):
    if message.text.lower() == 'да':
        await message.answer("ну и чудненько")
        await asyncio.sleep(5)
        await Form.remember_oath.set()
        await message.answer("Клятва на пальчиках в силе? Мы еще охана?")
    elif message.text.lower() == 'нет':
        await message.answer("если честно, мне все равно. Я просто спросил")
        await asyncio.sleep(5)
        await Form.remember_oath.set()
        await message.answer("Клятва на пальчиках в силе? Мы еще охана?")
    else:
        await message.answer("чего блять? Ты пожешь написать да или нет?")

@dp.message_handler(state=Form.remember_oath)
async def process_remember_oath(message: types.Message, state: FSMContext):
    if message.text.lower() == 'да':
        await message.answer("япикаееееей, мазафака. Тогда до встречи на следующей неделе! Счастья, здоровья тебе")
    elif message.text.lower() == 'нет':
        await message.answer("Пидор!")
    else:
        await message.answer("чего блять? Ты пожешь написать да или нет?")

    await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp,
                           skip_updates=True,
                           on_startup=on_startup)
