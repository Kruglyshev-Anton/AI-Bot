from aiogram import Bot, Dispatcher
import asyncio
import logging
from aiogram.types import Message
from aiogram.filters.command import Command

logging.basicConfig(level=logging.INFO)
bot = Bot(token="")
dispatcher=Dispatcher()
@dispatcher.message(Command("start"))
async def start(message: Message):
    await message.answer("Привет")

@dispatcher.message()
async def start(message: Message):
    await message.answer(message.text)

async def START():
    await dispatcher.start_polling(bot)
if __name__=='__main__':
    asyncio.run(START())
