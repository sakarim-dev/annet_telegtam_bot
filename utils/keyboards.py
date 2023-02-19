from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup
from aiogram import types


def get_admin_keyboard() -> ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, is_persistent=True)
    button_two = types.KeyboardButton('Количество пользователей')
    markup.add(button_two)
    return markup


def get_main_keyboard() -> ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, is_persistent=True)
    button_one = types.KeyboardButton('Предварительная запись на Практикум «Энергия жизни»')
    button_two = types.KeyboardButton('Запись на тет-а-тет с Аннет')
    button_three = types.KeyboardButton('Пройти отбор на Наставничество от Аннет')
    button_four = types.KeyboardButton('Контакты')

    markup.add(button_one, button_two, button_three, button_four)

    return markup


def get_record_keyboard() -> InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup()
    button_one = types.InlineKeyboardButton('Записаться', callback_data='record')
    markup.add(button_one)

    return markup


def get_record_repeat_keyboard() -> InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup(row_width=1)
    button_one = types.InlineKeyboardButton('Записаться заново', callback_data='record')
    button_two = types.InlineKeyboardButton('Все верно', callback_data='all_right')
    markup.add(button_one, button_two)

    return markup


def get_links_keyboard() -> InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup(row_width=1)
    button_one = types.InlineKeyboardButton('Телеграм-канал', url='https://t.me/+bK7RcoSuxHUxZWIy/')
    button_two = types.InlineKeyboardButton('Кейсы/результаты/отзывы', url='https://www.instagram.com/annet.trener/')
    button_three = types.InlineKeyboardButton('Профиль Instagram', url='https://www.instagram.com/annet.enjoy/')
    markup.add(button_one, button_two, button_three)

    return markup


def get_form_one_keyboard() -> InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup(row_width=1)
    button_one = types.InlineKeyboardButton('Анкета',
                                            url='https://docs.google.com/forms/d/e'
                                                '/1FAIpQLSdQNATRngiOvmsaZBhjv8KflanTdpG7LkeIX-_uZNtJT8YT0w/viewform')
    markup.add(button_one)

    return markup


def get_form_two_keyboard() -> InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup(row_width=1)
    button_one = types.InlineKeyboardButton('Анкета',
                                            url='https://docs.google.com/forms/d/e'
                                                '/1FAIpQLSdQNATRngiOvmsaZBhjv8KflanTdpG7LkeIX-_uZNtJT8YT0w/viewform')
    markup.add(button_one)

    return markup
