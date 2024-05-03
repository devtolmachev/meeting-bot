from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardButton


def get_watch_questionnaire_markup() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    for text in ['❤️', '💌', '👎', '💤']:
        btn = KeyboardButton(text=text)
        kb.add(btn)

    return kb.as_markup(resize_keyboard=True)


def show_messages_for_me_markup() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    for text in ['Показать сообщения', 'Не показывать сообщения']:
        kb.add(KeyboardButton(text=text))
        kb.adjust(1)

    return kb.as_markup(resize_keyboard=True)


def show_likes_for_me_markup() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    for text in ['Показать лайки', 'Не показывать лайки']:
        kb.add(KeyboardButton(text=text))
        kb.adjust(1)

    return kb.as_markup(resize_keyboard=True)
