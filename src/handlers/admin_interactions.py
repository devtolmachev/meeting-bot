from aiogram import Dispatcher
from aiogram.types import CallbackQuery

from src.etc.bot import bot
from src.markups import *


async def freeze_questionnaire(call: CallbackQuery):
    user_id = int(call.data.split('hide_questionnaire_')[1].split('=')[0])
    user = User(user_id)

    if call.data.count('strangers_indecent_photos'):
        cause = "🔞 Чужие или не приличные фото"
    elif call.data.count('rudeness_in_description'):
        cause = "🤬 Грубость в описании"
    elif call.data.count('rudeness_in_communication'):
        cause = "💢 Грубость в общении"

    await user.hide_questionnaire(cause=cause)
    text = f"На вашу анкету поступила жалоба: <b>{cause}</b>.\n\n" \
           f"Ваша анкета не показывается другим пользователям, до тех пор пока вы не исправите ошибку."
    await bot.send_message(user_id, text, reply_markup=get_correct_mp(user_id).as_markup())
    await call.answer("Анкета отключена", show_alert=True)


def register_admin_interaction_handlers(_dp: Dispatcher):
    _dp.callback_query.register(freeze_questionnaire, lambda call: call.data.startswith('hide_questionnaire'))
