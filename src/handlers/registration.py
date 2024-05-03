from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message
from aiogram.types import ReplyKeyboardRemove
from aiogram.utils.media_group import MediaGroupBuilder

from src.database.user import User
from src.etc.bot import bot, dp
from src.markups import get_general_keyboard
from src.markups.reply.registration import *
from src.utils.location import get_city


class RegistrationStates(StatesGroup):
    city_manual = State()
    name = State()
    change_description = State()
    all_done = State()
    gender = State()
    gender_interests = State()
    age = State()
    zodiac_sign = State()
    height = State()
    earn = State()
    location = State()
    photos_id = State()
    description = State()
    field_of_activity = State()


@dp.callback_query(lambda call: call.data == 'registration')
async def registration_handler(call: CallbackQuery | Message, state: FSMContext):
    if isinstance(call, CallbackQuery):
        await call.answer()

    await state.set_state(RegistrationStates.name)

    text = "Как вас зовут?"
    await bot.send_message(call.from_user.id, text, reply_markup=ReplyKeyboardRemove())


@dp.message(RegistrationStates.name)
async def get_age(msg: Message, state: FSMContext):
    name = msg.text

    await state.update_data(name=name)

    await state.set_state(RegistrationStates.age)
    # text = "Расскажи о себе и кого хочешь найти, чем предлагаешь заняться. Это поможет лучше подобрать тебе компанию."
    text = 'Сколько вам лет?'
    await bot.send_message(msg.from_user.id, text)


@dp.message(RegistrationStates.age)
async def get_age(msg: Message, state: FSMContext):
    if not msg.text or not msg.text.isdigit():
        return await bot.send_message(msg.from_user.id, "Укажи правильный возраст, только цифры")
    elif int(msg.text) < 18:
        return await bot.send_message(msg.from_user.id, "Пользователю должно быть не менее 18 лет")

    await state.update_data(age=int(msg.text))

    await state.set_state(RegistrationStates.gender)
    text = "Теперь определимся с полом"
    await bot.send_message(msg.from_user.id, text, reply_markup=get_gender_markup())


@dp.message(RegistrationStates.gender)
async def get_age(msg: Message, state: FSMContext):
    if msg.text not in ['Я парень', 'Я девушка']:
        return await bot.send_message(msg.from_user.id, "Нет такого варианта ответа")

    await state.update_data(gender=msg.text)

    await state.set_state(RegistrationStates.gender_interests)
    text = "Кто вам интересен?"
    await bot.send_message(msg.from_user.id, text, reply_markup=get_gender_interests_markup())


@dp.message(RegistrationStates.gender_interests)
async def get_age(msg: Message, state: FSMContext):
    if msg.text not in ['Парни', 'Девушки', 'Все равно']:
        return await bot.send_message(msg.from_user.id, "Нет такого варианта ответа")

    await state.update_data(gender_interests=msg.text)

    await state.set_state(RegistrationStates.height)
    text = "Напишите ваш рост"
    await bot.send_message(msg.from_user.id, text, reply_markup=ReplyKeyboardRemove())


@dp.message(RegistrationStates.height)
async def get_age(msg: Message, state: FSMContext):
    if not msg.text or not msg.text.isdigit():
        text = 'Напиши свой рост в цифрах, например 170'
        return await bot.send_message(msg.from_user.id, text)
    elif int(msg.text) <= 40:
        text = "Рост должен быть больше 40см"
        return await bot.send_message(msg.from_user.id, text)

    await state.update_data(height=int(msg.text))

    text = "Выберите свой знак зодиака"
    await state.set_state(RegistrationStates.zodiac_sign)

    kb = get_zodiacs_signs_markup()
    skip_btn = get_skip_markup().keyboard[0][0]
    kb.keyboard.append([skip_btn])
    await bot.send_message(msg.from_user.id, text, reply_markup=kb)


@dp.message(RegistrationStates.zodiac_sign)
async def verify_zodiac_sign(msg: Message, state: FSMContext):
    zodiac_signest = [
        btn.text for row in get_zodiacs_signs_markup().keyboard
        for btn in row
    ]

    markup = get_location_markup()
    skip_btn = get_skip_markup().keyboard[0][0]
    markup.keyboard.append([skip_btn])

    if msg.text == 'Пропустить':
        await state.update_data(zodiac_sign=None)

    elif msg.text in zodiac_signest:
        await state.update_data(zodiac_sign=msg.text)

    else:
        return await bot.send_message(msg.from_user.id, "Нет такого варианта ответа")

    text = "Отправьте свою геолокацию, это нужно для поиска анкет рядом"
    await bot.send_message(msg.from_user.id, text, reply_markup=markup)
    await state.set_state(RegistrationStates.location)


@dp.message(RegistrationStates.location)
async def get_age(msg: Message, state: FSMContext):
    if msg.text != 'Пропустить' and msg.text:
        return await bot.send_message(msg.from_user.id, "Нет такого варианта ответа")

    elif msg.text == 'Пропустить':
        await state.update_data(location=None)
        await state.update_data(city=None)

    elif not msg.location:
        text = "Отправьте мне вашу геолокацию, это нужно для поиска людей рядом с вами"
        return await bot.send_message(msg.from_user.id, text)

    elif msg.location:
        await state.update_data(location={"lat": msg.location.latitude,
                                          "long": msg.location.longitude})

        try:
            city = await get_city(
                lat=msg.location.latitude,
                long=msg.location.longitude
            )
        except NotImplementedError:
            await bot.send_message(msg.from_user.id, "Не удалось определить город. Напишите свой город")
            return await state.set_state(RegistrationStates.city_manual)

        await state.update_data(city=city)

    await state.set_state(RegistrationStates.field_of_activity)
    text = "Какая у вас сфера деятельности? Выберите ответ из списка"

    mp = get_field_of_activity_markup()
    mp.keyboard.append([get_skip_markup().keyboard[0][0]])
    await bot.send_message(msg.from_user.id, text, reply_markup=mp)


@dp.message(RegistrationStates.city_manual)
async def write_city_manual(msg: Message, state: FSMContext):
    if not msg.text or msg.text.isdigit():
        return await bot.send_message(msg.from_user.id, "Напиши свой город")

    await state.update_data(city=msg.text)
    await state.set_state(RegistrationStates.field_of_activity)
    text = "Какая у тебя сфера деятельности? Выбери ответ из списка"
    mp = get_field_of_activity_markup()
    mp.keyboard.append([get_skip_markup().keyboard[0][0]])
    await bot.send_message(msg.from_user.id, text, reply_markup=mp)


@dp.message(RegistrationStates.field_of_activity)
async def choice_filed_of_activity(msg: Message, state: FSMContext):
    if msg.text == 'Пропустить':
        await state.update_data(field_of_activity=None)

    elif msg.text not in [btn.text for row in get_field_of_activity_markup().keyboard
                          for btn in row]:
        return await bot.send_message(msg.from_user.id, "Нет такого варианта ответа")

    else:
        await state.update_data(field_of_activity=msg.text)

    await state.set_state(RegistrationStates.earn)

    text = 'Сколько вы зарабатываете? Заработок всегда можно скрыть в анкете'

    kb = get_earn_markup()
    btn_skip = get_skip_markup().keyboard[0][0]
    kb.keyboard.append([btn_skip])
    await bot.send_message(msg.from_user.id, text, reply_markup=kb)


@dp.message(RegistrationStates.earn)
async def set_earn_people(msg: Message, state: FSMContext):
    if msg.text == 'Пропустить':
        await state.update_data(earn=None)

    elif msg.text in [btn.text for row in get_earn_markup().keyboard
                      for btn in row]:
        await state.update_data(earn=msg.text)

    else:
        text = 'Нет такого варианта ответа'
        return await bot.send_message(msg.from_user.id, text)

    await state.set_state(RegistrationStates.description)
    text = "Расскажи о себе, своих достижениях и увлечениях. Кого хочешь найти?"
    await bot.send_message(msg.from_user.id, text, reply_markup=get_skip_markup())


@dp.message(RegistrationStates.description)
async def get_description(msg: Message, state: FSMContext, change: bool = False):
    if msg.text == 'Пропустить':
        await state.update_data(description=None)
    elif not msg.text:
        return await bot.send_message(msg.from_user.id, "Пришли текст")
    else:
        if len(msg.text) < 3:
            return await bot.send_message(msg.from_user.id,
                                          "Напиши о себе что-нибудь поинтереснее")

        await state.update_data(description=msg.text)

        if change:
            user = User(msg.from_user.id)
            await user.change_description(description=msg.text)
            return await bot.send_message(msg.from_user.id, "Описание обновлено!")

    await state.set_state(RegistrationStates.photos_id)
    text = "Теперь отправь свои фотографии или видео"
    await bot.send_message(msg.from_user.id, text, reply_markup=ReplyKeyboardRemove())


@dp.message(RegistrationStates.photos_id)
async def get_photos(msg: Message, state: FSMContext, album: list[Message],
                     cancel_btn: KeyboardButton = None):
    if msg.text == 'Это все, сохранить фото':
        return await view_questionnaire(msg, state)

    elif msg.text == 'Вернуться назад':
        await state.clear()
        return await view_questionnaire(msg=msg, state=state, all_done=False)

    elif not msg.photo and not msg.video:
        text = 'Отправь фото или видео до 15 секунд'
        return await bot.send_message(msg.from_user.id, text)

    user = User(msg.from_user.id)
    data = await state.get_data()
    media_group: MediaGroupBuilder = (await state.get_data()).get("media_group") or MediaGroupBuilder()
    media_files: dict = (await state.get_data()).get("media_files") or {}

    if msg.media_group_id:
        for message in album:
            if len([file for key in media_files for file in media_files[key]]) < 10:
                if message.photo:
                    if not media_files.get("photo"):
                        media_files["photo"] = []

                    media_files["photo"].append(message.photo[-1].file_id)
                    media_group.add_photo(message.photo[-1].file_id)

                elif message.video:
                    if message.video.duration > 15:
                        return await bot.send_message(msg.from_user.id, "Видео должно быть не более 15 секунд!")

                    if not media_files.get("video"):
                        media_files["video"] = []

                    media_files["video"].append(message.video.file_id)
                    media_group.add_video(message.video.file_id)

    elif msg.video:
        if len([file for key in media_files for file in media_files[key]]) < 10:
            if msg.video.duration > 15:
                return await bot.send_message(msg.from_user.id, "Видео должно быть не более 15 секунд!")

            if not media_files.get("video"):
                media_files["video"] = []

            media_files["video"].append(msg.video.file_id)
            media_group.add_video(msg.video.file_id)

    elif msg.photo:
        if len([file for key in media_files for file in media_files[key]]) < 10:
            if not media_files.get("photo"):
                media_files["photo"] = []

            media_files["photo"].append(msg.photo[-1].file_id)
            media_group.add_photo(msg.photo[-1].file_id)

    if len([file for key in media_files for file in media_files[key]]) >= 10:
        while len([file for key in media_files for file in media_files[key]]) != 10:
            if not media_files.get('photo'):
                media_files["video"].pop(-1)
            else:
                media_files["photo"].pop(-1)

    await state.update_data(media_group=media_group)
    await state.update_data(media_files=media_files)

    if len([file for key in media_files for file in media_files[key]]) >= 10:
        return await view_questionnaire(msg, state)

    elif msg.video or msg.photo or album:
        text = f"Фото добавлено – {len([file for key in media_files for file in media_files[key]])} из 10. Еще одно?"
        kb = get_set_photos_btn()
        await bot.send_message(msg.from_user.id, text, reply_markup=kb)

    elif msg.text == 'Это все, сохранить фото':
        return await view_questionnaire(msg=msg, state=state)

    elif msg.text == 'Вернуться назад':
        text = (f"1. Заполнить анкету заново.\n"
                f"2. Изменить фото/видео.\n"
                f"3. Изменить текст анкеты.\n"
                f"4. Смотреть анкеты.")
        await state.clear()
        await bot.send_message(msg.from_user.id, text, reply_markup=get_general_keyboard(4))

    else:
        return await bot.send_message(msg.from_user.id, 'Нет такого варианта ответа')


async def view_questionnaire(msg: Message, state: FSMContext, all_done: bool = True):
    data = await state.get_data()
    user = User(msg.from_user.id)

    media_group: MediaGroupBuilder = data.get("media_group")

    if not data.get("media_group") and await user.is_exists():
        media_id = await user.get_photos()
        media_group = MediaGroupBuilder()

        for type_file in media_id:
            for media_file_id in media_id[type_file]:
                if type_file == 'photo':
                    media_group.add_photo(media_file_id)
                elif type_file == 'video':
                    media_group.add_video(media_file_id)

    await bot.send_message(msg.from_user.id, 'Так выглядит твоя анкета:', reply_markup=ReplyKeyboardRemove())

    data = await state.get_data()
    if not await user.is_exists() or data.get("change"):
        name = data["name"]
        age = data["age"]
        earn = data["earn"]
        hide_earn = False
        zodiac_sign = data["zodiac_sign"]
        city = data.get("city")
        description = data["description"]
        height = data["height"]
        field_of_activity = data["field_of_activity"]

    else:
        name = await user.name()
        age = await user.get_age()
        earn = await user.earn()
        zodiac_sign = await user.zodiac_sign()
        city = await user.get_location(city=True)
        description = await user.description()
        hide_earn = await user.hide_earn()
        height = await user.height()
        field_of_activity = await user.field_of_activity()

    media_group.caption = (f'{name}, {age}, {city}\n\n'
                           f'Рост: {height}\n'
                           f'Знак зодиака: {zodiac_sign}\n'
                           f'Сфера детяльности: {field_of_activity}\n'
                           f'Зарабатываю: {earn}\n\n'
                           f'О себе: {description}')

    if hide_earn or not earn:
        media_group.caption = media_group.caption.replace(f'Зарабатываю: {earn}\n',
                                                          'Зарабатываю: <i>Не указано</i>\n')
    if not description:
        media_group.caption = media_group.caption.replace(f'О себе: {description}',
                                                          'О себе: <i>Не указано</i>')
    if not city:
        media_group.caption = media_group.caption.replace(f", {city}",
                                                          ', <i>Город не указан</i>\n')
    if not zodiac_sign:
        media_group.caption = media_group.caption.replace(f"Знак зодиака: {zodiac_sign}\n",
                                                          'Знак зодиака: <i>Не указан</i>\n')
    if not field_of_activity:
        media_group.caption = media_group.caption.replace(f"Сфера детяльности: {field_of_activity}\n",
                                                          'Сфера деятельности: <i>Не указана</i>\n')

    await bot.send_media_group(msg.from_user.id, media_group.build())

    if all_done:
        await bot.send_message(msg.from_user.id, 'Все верно?', reply_markup=get_all_cool_markup())
        await state.set_state(RegistrationStates.all_done)


def register_registration_handlers():
    ...
