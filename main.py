import logging
import os

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)
dp = Dispatcher(Bot(token=str(os.getenv("TOKEN"))),storage=MemoryStorage())
hodmarkup=types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
hodmarkup.add(types.KeyboardButton("1"))
hodmarkup.add(types.KeyboardButton("2"))
hodmarkup.add(types.KeyboardButton("Рестарт"))

restart=types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
restart.add(types.KeyboardButton("Рестарт"))

class Status(StatesGroup):
    h1=State()
    h2=State()
    h3=State()
    end=State()

@dp.message_handler(state=Status.end)
async def h3check(message:types.Message)->None:
    if message.text=="1":
        await message.answer("Маньяк оказался недружелюбным, ты проиграл.", reply_markup=restart)
        await Status.h1.set()
    elif message.text=="2":
        await message.answer("Ты дождался дня, пока сова уснет, и спокойно прошел мимо нее.")
        await message.answer_photo("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ25IEvK_iraVhHnS6uaG526GVOO98D4DUf9g&usqp=CAU","Ты нашел выход из подземелья, поздравляю! Сыграем еще раз?", reply_markup=restart)
        await Status.h1.set()
    elif message.text=="Рестарт":
        await Status.h1.set()
        await h1quest(message)

async def h3quest(message):
    await message.answer("Ты выжил, ведь аммиак - легкий газ, и он поднимается вверх.",reply_markup=hodmarkup)
    await message.answer("В следующем помещении есть окно, через которое видно, что сейчас ночь, но через него нельзя выбраться, так что выбери путь:")
    await message.answer("1.Дверь, за которой серийный маньяк")
    await message.answer("2.Дверь, за которой агрессивная сова")
    await Status.end.set()

@dp.message_handler(state=Status.h3)
async def h2check(message:types.Message)->None:
    if message.text=="1":
        await h3quest(message)
    elif message.text=="2":
        await message.answer("Ты задохнулся, ведь аммиак - легкий газ, и он поднимается вверх.",reply_markup=restart)
        await Status.h1.set()
    elif message.text=="Рестарт":
        await Status.h1.set()
        await h1quest(message)

async def h2quest(message):
    await message.answer("Да, лев умер, т.к. не ел ЦЕЛЫХ 5 МЕСЯЦЕВ.", reply_markup=hodmarkup)
    await message.answer("Снова развилка, но уже вертикальная. Ты чуешь запах аммиака. Выбери путь:")
    await message.answer("1.Продолжить идти по коридору")
    await message.answer("2.Подняться вверх по лестнице")
    await Status.h3.set()

@dp.message_handler(state=Status.h2)
async def h1check(message:types.Message)->None:
    if message.text=="1":
        await h2quest(message)
    elif message.text=="2":
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
        markup.add(types.KeyboardButton("Рестарт"))
        await message.answer("О чем ты думал!! ты умер",reply_markup=restart)
        await Status.h1.set()
    elif message.text=="Рестарт":
        await Status.h1.set()
        await h1quest(message)

@dp.message_handler(state=Status.h1)
async def h1quest(message:types.Message)->None:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(types.KeyboardButton("1"))
    markup.add(types.KeyboardButton("2"))
    await message.answer("Выбери путь:", reply_markup=markup)
    await message.answer("1.Дверь, за которой грозный лев, который не ел 5 месяцев")
    await message.answer("2.Дверь, за которой коридор с лавой вместо пола")
    await Status.h2.set()

@dp.message_handler(state="*")
async def start(message:types.Message)->None:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
    markup.add(types.KeyboardButton("Старт"))
    await message.answer("Это квест игра, в которой тебе нужно будет добраться до выхода, выбирая верный путь.",reply_markup=markup)
    await Status.h1.set()

if __name__ == "__main__":
    executor.start_polling(dp,skip_updates=True)
