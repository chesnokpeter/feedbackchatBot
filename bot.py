#ЕКСПЕРИМЕНТАЛЬНАЯ ВЕТКА
import datetime
import asyncio

# filters
from tgbot.filters.admin_filter import AdminFilter
from tgbot.filters.message_length import MessageLengthFilter
from tgbot.filters.banned_filter import IsBannedFilter
from telebot.asyncio_filters import IsReplyFilter

# handlers
from tgbot.handlers.admin import admin_user
from tgbot.handlers.user_message import (
    user_text_message, user_media_message, message_is_too_long,
    user_is_banned
)
from tgbot.handlers.banning import ban_user, unban_user

from telebot import types

# telebot
from telebot.async_telebot import AsyncTeleBot

from tgbot.models.users_model import Admin

# config
from tgbot import config



MEDIA = ['photo', 'video', 'audio', 'document', 'voice', 'animation']
TEXT_MEDIA = ['text', 'photo', 'video', 'audio', 'document', 'voice', 'animation']

bot = AsyncTeleBot(config.TOKEN)

def register_handlers():
    bot.register_message_handler(ban_user, admin=True, pass_bot=True, is_reply=True, commands=['ban'])
    bot.register_message_handler(unban_user, admin=True, pass_bot=True, is_reply=True, commands=['unban'])
    bot.register_message_handler(admin_user, admin=True, pass_bot=True, is_reply=True, content_types=TEXT_MEDIA)
    bot.register_message_handler(user_text_message, content_types=['text'], pass_bot=True, admin=False, length=config.MAX_MESSAGE_LENGTH, banned=False)
    bot.register_message_handler(user_media_message, content_types=MEDIA,pass_bot=True, admin=False, length=config.MAX_CAPTION, banned=False)
    bot.register_message_handler(message_is_too_long, content_types=TEXT_MEDIA, pass_bot=True, admin=False, banned=False)
    bot.register_message_handler(user_is_banned, content_types=TEXT_MEDIA, pass_bot=True, admin=False, banned=True)


@bot.message_handler(commands=['check'])
async def send_welcome(message):
    await bot.send_message(message.chat.id, 'Я работаю')
    with open('textdata/users.txt', 'a+') as users:
        print(f'{datetime.datetime.now()}    @{message.from_user.username}    {message.chat.id}    /check', file=users)





@bot.message_handler(commands=['start'])
async def send_welcome(message):
    with open('textdata/userid.txt', 'a+') as userid:
        print(message.chat.id, file=userid)
    with open('textdata/users.txt', 'a+') as users:
        print(f'{datetime.datetime.now()}    @{message.from_user.username}    {message.chat.id}    /start', file=users)
    markup = types.InlineKeyboardMarkup()
    ask = types.InlineKeyboardButton("Спросить депутата", callback_data='ask')
    markup.add(ask)
    url1 = types.InlineKeyboardButton("", url='')  
    url2 = types.InlineKeyboardButton("", url='')
    markup.add(url1, url2)
    await bot.send_message(message.chat.id, text='', reply_markup=markup)





@bot.callback_query_handler(func=lambda call: True)
async def callback_inline(call):
    if call.data == 'ask':
        await bot.send_message(call.message.chat.id, 'Задайте ваш вопрос и подробно опишите ситуацию.\nОтправьте информацию одним сообщением.')
        with open('textdata/users.txt', 'a+') as users:
            print(f'{datetime.datetime.now()}    @{call.message.from_user.username}    {call.message.chat.id}    .ask', file=users)
    elif call.data == 'newask':
        await bot.send_message(call.message.chat.id, 'Задайте ваш вопрос и подробно опишите ситуацию.\nОтправьте информацию одним сообщением.')
        with open('textdata/users.txt', 'a+') as users:
            print(f'{datetime.datetime.now()}    @{call.message.from_user.username}    {call.message.chat.id}    .newask', file=users)
    elif call.data == 'noask':
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton("Начать заново", callback_data='restart')
        markup.add(btn)
        await bot.send_message(call.message.chat.id, text='Спасибо за ваше обращение', reply_markup=markup)
        with open('textdata/users.txt', 'a+') as users:
            print(f'{datetime.datetime.now()}    @{call.message.from_user.username}    {call.message.chat.id}    .noask', file=users)
    elif call.data == 'restart':
        markup = types.InlineKeyboardMarkup()
        ask = types.InlineKeyboardButton("Спросить депутата", callback_data='ask')
        markup.add(ask)
        url1 = types.InlineKeyboardButton("", url='')  
        url2 = types.InlineKeyboardButton("", url='') 
        markup.add(url1, url2)
        await bot.send_message(call.message.chat.id, text='', reply_markup=markup)
        with open('textdata/users.txt', 'a+') as users:
            print(f'{datetime.datetime.now()}    @{call.message.from_user.username}    {call.message.chat.id}    .restart', file=users)




@bot.message_handler(commands=['statistic'])
async def send_welcome(message):
    with open('textdata/users.txt', 'a+') as users:
        print(f'{datetime.datetime.now()}    @{message.from_user.username}    {message.chat.id}    /statistic', file=users)
    f = open('textdata/errors.txt', 'rb')
    await bot.send_document(Admin.ADMIN.value, f)
    f = open('textdata/userid.txt', 'rb')
    await bot.send_document(Admin.ADMIN.value, f)
    f = open('textdata/users.txt', 'rb')
    await bot.send_document(Admin.ADMIN.value, f)
    f = open('textdata/usertext.txt', 'rb')
    await bot.send_document(Admin.ADMIN.value, f)




register_handlers()

print(f"{datetime.datetime.now()}    start")

# custom filters
bot.add_custom_filter(AdminFilter())
bot.add_custom_filter(MessageLengthFilter())
bot.add_custom_filter(IsBannedFilter())
bot.add_custom_filter(IsReplyFilter())



async def run():
    await bot.polling(non_stop=True)





if __name__=='__main__':
    while True:
        try:
            asyncio.run(run())
        except Exception as e:
            with open('textdata/errors.txt', 'a+') as errors:
                print(f'{datetime.datetime.now()}    {e}', file=errors)
            print(e)
            continue

