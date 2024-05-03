from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardBuilder


def get_subscribe_btn() -> InlineKeyboardBuilder:
    text = "Купить подписку"
    callback_data = "get_subscribe"
    btn = InlineKeyboardButton(text=text, callback_data=callback_data)
    kb = InlineKeyboardBuilder()
    kb.add(btn)
    return kb
