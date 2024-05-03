from aiogram import Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.handlers.registration import registration_handler


async def correct_questionnaire(call: CallbackQuery, state: FSMContext):
    await state.update_data(change=True)
    await registration_handler(call=call, state=state)


def register_profile_interaction_handlers(_dp: Dispatcher):
    _dp.callback_query.register(correct_questionnaire, lambda c: c.data.startswith('correct_questionnaire_'))
