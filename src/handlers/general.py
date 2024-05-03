from aiogram import F
from aiogram.filters import CommandStart

from src.database.user import AllUsers
from src.handlers.admin_interactions import register_admin_interaction_handlers
from src.handlers.profile_interaction import register_profile_interaction_handlers
from src.handlers.profile_settings import register_profile_handlers
from src.handlers.registration import *
from src.handlers.subscribe import register_pay_handlers
from src.handlers.watch_questionnaire import (WatchQuestionnaire,
                                              register_watch_questionnaire_handlers)
from src.markups import *


@dp.message(F.text.lower().count('отмена'))
async def cancel_ms(msg: Message, state: FSMContext):
    await state.clear()
    await bot.send_message(msg.from_user.id, '✅')


@dp.message(F.text == 'Вернуться назад')
async def go_back(msg: Message, state: FSMContext):
    await cancel_ms(msg=msg, state=state)
    await start(msg=msg, state=state)


@dp.message(CommandStart())
async def start(msg: Message, state: FSMContext):
    user = User(msg.from_user.id)
    if await user.is_exists():
        return await start_existing_user(msg, state)

    text = "Приветствую вас, здесь вы сможете найти свою вторую половинку 👩‍❤️‍👨"
    await bot.send_message(msg.from_user.id, text, reply_markup=inline.get_start_btn().as_markup())


async def start_existing_user(msg: Message, state: FSMContext):
    text = (f"1. Заполнить анкету заново.\n"
            f"2. Изменить фото/видео.\n"
            f"3. Изменить текст анкеты.\n"
            f"4. Смотреть анкеты.")

    if await User(msg.from_user.id).is_hiden_questionnaire():
        cause = await User(msg.from_user.id).get_cause_hide_questionnaire()
        await bot.send_message(msg.from_user.id, "Ваша анкета скрыта в поиске по причине:\n"
                                                 f"<i>{cause}</i>.\nПожалуйста, измените анкету.")

    await view_questionnaire(msg=msg, state=state, all_done=False)

    kb = get_general_keyboard(4)
    await bot.send_message(msg.from_user.id, text, reply_markup=kb)


@dp.message(F.text == '1')
async def register_again(msg: Message, state: FSMContext):
    await state.update_data(change=True)
    await registration_handler(call=msg, state=state)


@dp.message(F.text == '2')
async def change_my_media(msg: Message, state: FSMContext):
    text = 'Пришли фото или запиши видео 👍 (до 15 сек)'

    btn = get_cancel_btn()
    kb = ReplyKeyboardMarkup(keyboard=[[btn]], resize_keyboard=True)

    await state.set_state(RegistrationStates.photos_id)
    await state.update_data(change_photos=True)
    await bot.send_message(
        msg.from_user.id,
        text,
        reply_markup=kb
    )


@dp.message(F.text == '3')
async def change_description(msg: Message, state: FSMContext):
    text = "Расскажи о себе, кого хочешь найти, чем предлагаешь заняться"
    kb = ReplyKeyboardMarkup(keyboard=[[get_cancel_btn()]], resize_keyboard=True)

    await bot.send_message(msg.from_user.id, text, reply_markup=kb)
    await state.set_state(RegistrationStates.change_description)


@dp.message(F.text == '4')
async def watch_questionnaires(msg: Message, state: FSMContext):
    await state.set_state(WatchQuestionnaire.main)
    await bot.send_message(msg.from_user.id, '💼💌', reply_markup=get_watch_questionnaire_markup())

    users = AllUsers()
    try:
        questionnaire_user = (await users.get_users_questionnaires(
            my_user_id=msg.from_user.id
        ))[0]
    except IndexError:
        return await bot.send_message(msg.from_user.id, "Анкет сейчас нет, повторите позже")

    await state.update_data(previous_questionnaire=questionnaire_user)

    data = await state.update_data(skip_questionnaires_ids=[0, questionnaire_user.id])
    await bot.send_media_group(msg.from_user.id, questionnaire_user.get_questionnaire().build())
    await bot.send_message(msg.from_user.id, "Вы можете пожаловаться на анкету",
                           reply_markup=get_complaint_report_mp(questionnaire_user.id).as_markup())


@dp.message(F.text == '5')
async def view_my_questionnaire(msg: Message, state: FSMContext):
    return await start(msg=msg, state=state)


@dp.message(RegistrationStates.change_description)
async def change_description(msg: Message, state: FSMContext):
    await get_description(msg=msg, state=state, change=True)
    await start(msg=msg, state=state)
    await state.clear()


@dp.message(RegistrationStates.all_done)
async def verify_questionnaire(msg: Message, state: FSMContext):
    data = await state.get_data()
    user = User(msg.from_user.id)

    if not await user.is_exists() or data.get("change") is True:
        name = data["name"]
        age = data["age"]
        earn = data["earn"]
        zodiac_sign = data["zodiac_sign"]
        city = data["city"]
        description = data["description"]
        height = data["height"]
        field_of_activity = data["field_of_activity"]
        gender_interests = data['gender_interests']
        gender = data["gender"]
        location = data["location"]
        photos_id = data["media_files"]
    else:
        name = await user.name()
        age = await user.get_age()
        earn = await user.earn()
        gender_interests = await user.get_gender_interests()
        zodiac_sign = await user.zodiac_sign()
        city = await user.get_location(city=True)
        description = await user.description()
        height = await user.height()
        field_of_activity = await user.field_of_activity()
        gender = await user.get_gender()
        location = await user.get_location()
        photos_id = await user.get_photos()

    if msg.text == 'Да':
        user = User(msg.from_user.id)

        await user.insert_full_info_user(
            name=name,
            gender=gender,
            age=age,
            zodiac_sign=zodiac_sign,
            height=height,
            location=location,
            photos_id=photos_id,
            description=description,
            field_of_activity=field_of_activity,
            earn=earn,
            city=city,
            username=msg.from_user.username,
            gender_interests=gender_interests
        )
        await state.clear()
        text = (f"Анкета сохранена\n\n"
                f"1. Заполнить анкету заново.\n"
                f"2. Изменить фото/видео.\n"
                f"3. Изменить текст анкеты.\n"
                f"4. Смотреть анкеты.\n"
                f"5. Посмотреть мою анкету")
        await bot.send_message(msg.from_user.id, text, reply_markup=get_general_keyboard(5))

        if await user.is_hiden_questionnaire():
            await user.open_questionnaire()
            await bot.send_message(msg.from_user.id, "Ваша анкета вновь показывается для пользователей")

    elif msg.text == 'Изменить анкету':
        await state.clear()
        return await registration_handler(msg, state)


async def skip_active_users(msg: Message, state: FSMContext):
    user = User(msg.from_user.id)

    if msg.text.count("сообщения"):
        content_type = 'message'
    elif msg.text.count('лайки'):
        content_type = 'like'

    await user.delete_active_for_me(content_type=content_type)
    await start(msg=msg, state=state)


async def show_active_users(msg: Message, state: FSMContext):
    user = User(msg.from_user.id)
    questionnaires = []

    if msg.text.count("сообщения"):
        data = await user.get_messages_for_me()
        if not data:
            text = "Сообщений пока нет, но не растраивайтесь, они обязательно будут!"
            await bot.send_message(msg.from_user.id, text)
            return await start(msg=msg, state=state)

        await state.update_data(messages=data)
        content_type = 'messages'

    elif msg.text.count('лайки'):
        data = await user.get_likes_for_me()
        if not data:
            text = "Лайков пока нет, но не растраивайтесь, они обязательно будут!"
            await bot.send_message(msg.from_user.id, text)
            return await start(msg=msg, state=state)

        await state.update_data(likes=data)
        content_type = 'likes'

    else:
        raise NotImplementedError

    await state.set_state(WatchQuestionnaire.main)
    await bot.send_message(msg.from_user.id, '💼❤️', reply_markup=get_watch_questionnaire_markup())

    for item in data:
        questionnaires.extend(await AllUsers().get_users_questionnaires(
            my_user_id=msg.from_user.id,
            user_id=item["id"]
        ))

    await state.update_data(custom_questionnaires=questionnaires)
    await state.update_data(skip_questionnaires_ids=[questionnaires[0].id])
    await state.update_data(previous_questionnaire=questionnaires[0])
    await state.update_data(content_type=content_type)

    await bot.send_media_group(msg.from_user.id, questionnaires[0].get_questionnaire().build())

    if data[0].get('message'):
        message = f"<b>Сообщение от пользователя:</b> {data[0]['message']}"
        await bot.send_message(msg.from_user.id, message, reply_markup=get_watch_questionnaire_markup())


def register_general_handlers():
    dp.message.register(skip_active_users, F.text.startswith('Не показывать'))
    dp.message.register(show_active_users, F.text.startswith('Показать'))
    register_registration_handlers()
    register_watch_questionnaire_handlers()
    register_pay_handlers()
    register_profile_handlers(_dp=dp)
    register_admin_interaction_handlers(_dp=dp)
    register_profile_interaction_handlers(_dp=dp)
