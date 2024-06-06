from aiogram import Bot, Dispatcher
import asyncio
from aiogram.types import Message, ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.command import Command
import requests
import urllib.parse
from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models.gigachat import GigaChat
import uuid


chat = GigaChat(credentials="", verify_ssl_certs=False)
FirstPromt="Ты бот помощник-советчик. Ты советуешь собеседнику книги,"\
                                 " в том числе помогаешь составлять список литературы на лето,"\
                                 " советуешь фильмы или что-нибудь другое,"\
                                 " что захочет собеседник, исходя из его предпочтений."
UsersMess=dict()
bot = Bot(token="")
dispatcher = Dispatcher()



button_films = KeyboardButton(text='Посоветуй мне фильм.')
button_books = KeyboardButton(text='Посоветуй мне книгу.')
button_lit = KeyboardButton(text='Помоги мне составить список литературы на лето.')
button_beg = KeyboardButton(text='/start')
button_clear = KeyboardButton(text='/clear')


kb=[[button_beg], [button_clear], [button_films], [button_books], [button_lit]]

keyboard2 = ReplyKeyboardMarkup(keyboard=kb,one_time_keyboard=True,resize_keyboard=True)
MemoryWindow=10


@dispatcher.message(Command("start"))
async def start(message: Message):
    UsersMess[message.from_user.id] = [SystemMessage(FirstPromt)]
    await message.reply(
        '''Привет!
Я бот-советник, призванный помогать людям подбирать книги, фильмы или что-нибудь ещё.
Выберите то, по поводу чего вы хотели бы посоветоваться со мной, или напишите сразу, что вы хотите спросить.''',
        reply_markup=keyboard2)

@dispatcher.message(Command("clear"))
async def clear(message: Message):
    UsersMess[message.from_user.id] = [SystemMessage(FirstPromt)]
    await message.reply("Я забыл предыдущую переписку!", reply_markup=keyboard2)

@dispatcher.message()
async def Dialog(message: Message):
    id=message.from_user.id
    UsersMess[id].append(HumanMessage(content=message.text))
    ansModel=chat(UsersMess[id])
    UsersMess[id].append(ansModel)
    if len(UsersMess[id])==MemoryWindow+3:#на вход только модели последние 10 сообщений + первое от системы(чтобы бот не забывал что он советчик), в целях экономии токенов
        UsersMess[id].pop(1)
        UsersMess[id].pop(1)
    await message.answer(ansModel.content)


async def START():
    await dispatcher.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(START())
