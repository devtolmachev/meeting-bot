from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardBuilder

from src.database import User


async def get_hide_earn_btn(user_id: int) -> InlineKeyboardBuilder:
    user = User(user_id)
    earn_is_hiden = False if await user.hide_earn() is False else True

    if earn_is_hiden:
        text = "Открыть заработок"
        callback_data = 'unlock_earn'
    else:
        callback_data = 'lock_earn'
        text = "Скрыть заработок"

    btn = InlineKeyboardButton(text=text, callback_data=callback_data)
    kb = InlineKeyboardBuilder()
    kb.add(btn)
    return kb
