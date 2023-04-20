"""
Handles messages sent by user.
Then sends the messge to models.Admin.ADMIN.
"""
import datetime

from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message
from telebot import types
from telebot import formatting
# from telebot import *
# import models
from tgbot.models.users_model import Admin



import smtplib  # Импортируем библиотеку по работе с SMTP
# Добавляем необходимые подклассы - MIME-типы
from email.mime.multipart import MIMEMultipart  # Многокомпонентный объект
from email.mime.text import MIMEText  # Текст/HTML

blocked_users = [] # if you want, you can rewrite the bot with database.


async def user_text_message(message: Message, bot: AsyncTeleBot):
    """
    Handles messages sent by user.
    Then sends the message to models.Admin.ADMIN.

    This handler only detects text messages.
    """
    await bot.send_message(
        chat_id=Admin.ADMIN.value, text=f'#{str(message.chat.id)}\n#{str(message.chat.id)}id\n@{message.from_user.username}\n{message.from_user.first_name}:\n\n{message.text}')
    
    
    
    
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Остались еще вопросы?", callback_data='newask')  
    btn2 = types.InlineKeyboardButton("Вопросов больше нет, спасибо", callback_data='noask') 
    markup.add(btn1, btn2)
    await bot.send_message(message.chat.id, text="Спасибо, мы приняли ваше обращение. При необходимости и для получения дополнительной информации с вами свяжется мой помощник. Как только будет готов ответ, мы пришлём его здесь", reply_markup=markup)

    with open('textdata/usertext.txt', 'a+', encoding='utf-8') as usertext:
        print(f'{datetime.datetime.now()}    @{message.from_user.username}    {message.chat.id}    {message.text}', file=usertext)





    addr_from = ""
    addr_to = ""
    password = "" 
    msg = MIMEMultipart()
    msg['From'] = addr_from  
    msg['To'] = addr_to  
    datemessage = str(datetime.datetime.now()).split('.')
    datemessage = datemessage[0]
    msg['Subject'] = f' обращение от {message.from_user.first_name}'  # Тема сообщения
    body = f'#{str(message.chat.id)}\n#{str(message.chat.id)}id\n@{message.from_user.username}\n{datemessage}\n{message.from_user.first_name}:\n\n{message.text}'
    msg.attach(MIMEText(body, 'plain'))  # Добавляем в сообщение текст
    server = smtplib.SMTP_SSL('smtp.yandex.ru', 465)  # Создаем объект SMTP
    # server.starttls()             # Начинаем шифрованный обмен по TLS
    server.login(addr_from, password)  # Получаем доступ
    server.send_message(msg)  # Отправляем сообщение
    server.quit()  # Выходим





async def user_media_message(message: Message, bot: AsyncTeleBot):
    """
    Handles messages sent by user.
    Then sends the message to models.Admin.ADMIN.

    This handler only detects media messages.
    """
    await bot.copy_message(
        chat_id=Admin.ADMIN.value, from_chat_id=message.chat.id,
        message_id=message.message_id,
        caption=formatting.format_text(
            f'#{message.chat.id}',
            f'#{str(message.chat.id)}id',
            f'@{message.from_user.username}',
            f'{message.from_user.first_name}:\n',
            message.caption if message.caption else 'Нет описания'
        ),
    )

    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Остались еще вопросы?", callback_data='newask')  
    btn2 = types.InlineKeyboardButton("Вопросов больше нет, спасибо", callback_data='noask') 
    markup.add(btn1, btn2)
    await bot.send_message(message.chat.id, text="Спасибо, мы приняли ваше обращение. При необходимости и для получения дополнительной информации с вами свяжется мой помощник. Как только будет готов ответ, мы пришлём его здесь", reply_markup=markup)

    with open('textdata/usertext.txt', 'a+', encoding='utf-8') as usertext:
        print(f'{datetime.datetime.now()}    @{message.from_user.username}    {message.chat.id}    {message.caption}', file=usertext)


    addr_from = ""
    addr_to = ""
    password = "" 
    msg = MIMEMultipart()
    msg['From'] = addr_from  
    msg['To'] = addr_to  
    datemessage = str(datetime.datetime.now()).split('.')
    datemessage = datemessage[0]
    msg['Subject'] = f'обращение от {message.from_user.first_name}'  # Тема сообщения
    body = f'#{str(message.chat.id)}\n#{str(message.chat.id)}id\n@{message.from_user.username}\n{datemessage}\n{message.from_user.first_name}:\n\n{message.caption}'
    msg.attach(MIMEText(body, 'plain'))  # Добавляем в сообщение текст
    server = smtplib.SMTP_SSL('smtp.yandex.ru', 465)  # Создаем объект SMTP
    # server.starttls()             # Начинаем шифрованный обмен по TLS
    server.login(addr_from, password)  # Получаем доступ
    server.send_message(msg)  # Отправляем сообщение
    server.quit()  # Выходим


async def user_is_banned(message: Message, bot: AsyncTeleBot):
    """
    Show the user that he/she is banned.
    """
    await bot.send_message(
        chat_id=message.chat.id,
        text='You were banned some time ago. You cannot write anymore.'
    )


async def message_is_too_long(message: Message, bot: AsyncTeleBot):
    """
    Show the user that his/her message is too long.
    """
    await bot.send_message(
        chat_id=message.chat.id,
        text='Текст сообщения слишком длинный. Пожалуйста, сократите его'
    )