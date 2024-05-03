from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardBuilder


def get_start_btn() -> InlineKeyboardBuilder:
    kb = InlineKeyboardBuilder()
    btn = InlineKeyboardButton(text="Познакомиться", callback_data='registration')
    kb.add(btn)
    return kb
