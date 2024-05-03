from aiogram import F, Dispatcher
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove

from src.etc.bot import bot
from src.markups import *


class SearchStates(StatesGroup):
    filter_by_distance = State()
    filter_by_city = State()
    filter_by_height = State()
    filter_by_age = State()


async def profile_settings(msg: Message, state: FSMContext):
    user = User(msg.from_user.id)

    earn_is_hiden = False if await user.hide_earn() is False else True
    if earn_is_hiden is False:
        word = "показывается"

    else:
        word = "не показывается"

    text = f"Настройки профиля @{msg.from_user.username}\n\n" \
           f"Ваш заработок {word} в анкете, чтобы изменить эту настройку, " \
           f"нажмите на кнопку ниже"

    kb = await get_hide_earn_btn(msg.from_user.id)
    await bot.send_message(msg.from_user.id, text, reply_markup=kb.as_markup())


async def shift_earn_view_in_profile(call: CallbackQuery, state: FSMContext):
    await call.answer()

    user = User(call.from_user.id)
    hide_earn = await user.swift_earn_permission()

    if hide_earn:
        word = 'скрыт'
    else:
        word = 'открыт'

    text = f"Заработок {word} в вашей анкете для пользователей"
    await bot.send_message(call.from_user.id, text)


async def filter_questionnaire(msg: Message, state: FSMContext):
    if msg.text.count('расстоянию'):
        await state.set_state(SearchStates.filter_by_distance)
        text = ('Пришлите максимальное расстояние предлагаемых анкет. Километры - км, метры - м. (Например: 5 км. Это '
                'означает что вы будете '
                'видеть анкету с расстоянием до 5 км)')
        await bot.send_message(msg.from_user.id, text)
    elif msg.text.count('возрасту'):
        text = 'Напишите сообщение формата: "18 25". В данном примере вы ставите фильтр на анкеты от 18, и до 25 лет'
        await state.set_state(SearchStates.filter_by_age)
        await bot.send_message(msg.from_user.id, text)

    elif msg.text.count('городу'):
        await state.set_state(SearchStates.filter_by_city)
        text = "Напишите город из которого вы хотите видеть анкеты"
        await bot.send_message(msg.from_user.id, text)

    elif msg.text.count('росту'):
        text = ("Напишите сообщение формата: 160 180. В данном примере "
                "вы будете смотреть анкеты от 160см роста и до 180см")
        await state.set_state(SearchStates.filter_by_height)
        await bot.send_message(msg.from_user.id, text)

    elif msg.text.count('предпринимателям'):
        user = User(msg.from_user.id)
        await user.set_filter_by_activity('Предприниматель')
        await bot.send_message(msg.from_user.id, "Фильтр по предпринимателям установлен. Отправьте /start")
    else:
        return await bot.send_message(msg.from_user.id, "Нет такого варианта ответа")


async def filter_by_distance(msg: Message, state: FSMContext):
    if not msg.text or len(msg.text.split()) != 2 or msg.text.split() == 2 and msg.text.split()[1] not in ['км', "м"] \
            and not msg.text[0].isdigit():
        return await bot.send_message(msg.from_user.id, "Нет такого варианта ответа")

    value = msg.text.split()[1]
    distance = int(msg.text.split()[0])

    if value == 'км':
        distance = int(distance * 1000)

    user = User(msg.from_user.id)
    await user.set_filter_by_distance(distance)
    await state.clear()
    await bot.send_message(msg.from_user.id, f"Отлично, теперь вы будите видеть анкету, которые находятся "
                                             f"не дальше {msg.text} от вас! Отпрвьте /start",
                           reply_markup=ReplyKeyboardRemove())


async def filter_by_city(msg: Message, state: FSMContext):
    if not msg.text:
        return await bot.send_message(msg.from_user.id, "Нет такого варианта ответа")

    city = f"{msg.text[0].upper()}{msg.text[1:].lower()}"
    user = User(msg.from_user.id)

    await user.set_filter_by_city(city)
    await state.clear()

    await bot.send_message(msg.from_user.id,
                           f"Отлично! Теперь вы будете видеть анкету из города: {city}. "
                           f"Отпрвьте /start",
                           reply_markup=ReplyKeyboardRemove())


async def filter_by_age(msg: Message, state: FSMContext):
    if not msg.text or len(msg.text.split()) != 2 or all(not item.isdigit() for item in msg.text.split()):
        return await bot.send_message(msg.from_user.id, "Нет такого варианта ответа")

    user = User(msg.from_user.id)
    from_value = int(msg.text.split()[0])
    to_value = int(msg.text.split()[1])
    await user.set_filter_by_age(from_value=from_value, to_value=to_value)
    await state.clear()
    await bot.send_message(msg.from_user.id, f"Теперь вы будете видеть анкеты от {from_value} лет, до "
                                             f"{to_value} лет. Отпрвьте /start",
                           reply_markup=ReplyKeyboardRemove())


async def filter_by_height(msg: Message, state: FSMContext):
    if not msg.text or len(msg.text.split()) != 2 or all(not item.isdigit() for item in msg.text.split()):
        return await bot.send_message(msg.from_user.id, "Нет такого варианта ответа")

    user = User(msg.from_user.id)
    from_value = int(msg.text.split()[0])
    to_value = int(msg.text.split()[1])

    await user.set_filter_by_height(from_value=from_value, to_value=to_value)
    await state.clear()

    await bot.send_message(msg.from_user.id,
                           f"Теперь вы будете видеть анкеты у которых рост от {from_value} см,"
                           f" и до {to_value} см. Отпрвьте /start",
                           reply_markup=ReplyKeyboardRemove())


async def set_filters_on_watch_questionnaires(msg: Message, state: FSMContext):
    text = ("Вы можете установить фильтр на поиск анкет. Например вы можете искать анкеты с расстоянием до 10км, "
            "искать только людей с Москвы или Калуги, а также искать людей по возрасту или росту")
    await bot.send_message(msg.from_user.id, text, reply_markup=get_filters_mp())


async def clear_filters_user(msg: Message, state: FSMContext):
    text = "Все фильтры очищены. Отправьте /start"
    user = User(msg.from_user.id)
    await user.clear_filters()
    await bot.send_message(msg.from_user.id, text)


def register_profile_handlers(_dp: Dispatcher):
    _dp.message.register(clear_filters_user, Command('clear_filters'))
    _dp.message.register(set_filters_on_watch_questionnaires, Command('filter'))
    _dp.message.register(filter_by_height, SearchStates.filter_by_height)
    _dp.message.register(filter_by_age, SearchStates.filter_by_age)
    _dp.message.register(filter_by_city, SearchStates.filter_by_city)
    _dp.message.register(filter_by_distance, SearchStates.filter_by_distance)
    _dp.message.register(filter_questionnaire, F.text.count('Поиск по'))
    _dp.callback_query.register(shift_earn_view_in_profile, lambda call: call.data.count('_earn'))
    _dp.callback_query.register(profile_settings, lambda call: call.data.count('_earn'))
