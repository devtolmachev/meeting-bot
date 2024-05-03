from aiogram.exceptions import TelegramBadRequest
from aiogram.filters.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from src.database.questionnaires import Questionnaire
from src.database.user import AllUsers
from src.etc.bot import bot, admin_id, dp
from src.markups import *


class WatchQuestionnaire(StatesGroup):
    wait_message = State()
    main = State()


async def check_and_replace_photo_url(messages: list[Message], questionnaire: Questionnaire):
    if isinstance(questionnaire.photos_id.get('photo'), list) and \
            any([not photo.count('://') for photo in questionnaire.photos_id["photo"]]):
        return
    if isinstance(questionnaire.photos_id.get('video'), list) and \
            any([not photo.count('://') for photo in questionnaire.photos_id["video"]]):
        return

    medias = {}
    user = User(questionnaire.id)
    for msg in messages:
        if msg.photo:
            if not medias.get('photo'):
                medias["photo"] = []
            medias["photo"].append(msg.photo[-1].file_id)
        elif msg.video:
            if not medias.get('video'):
                medias["video"] = []
            medias["video"].append(msg.video.file_id)

    await user.change_photos(photos_id=medias)


async def watch_questionnaires_loop(msg: Message,
                                    state: FSMContext,
                                    custom_questionnaire: list[Questionnaire] = None,
                                    only_send: bool = True):
    if msg.text == '💤':
        await state.clear()
        text = (f"1. Заполнить анкету заново.\n"
                f"2. Изменить фото/видео.\n"
                f"3. Изменить текст анкеты.\n"
                f"4. Смотреть анкеты.\n"
                f"5. Посмотреть мою анкету")
        return await bot.send_message(msg.from_user.id, text, reply_markup=get_general_keyboard(5))

    user = User(msg.from_user.id)
    data = await state.get_data()

    previous_questionnaire: Questionnaire = data.get("previous_questionnaire")
    content_type: str = data.get("content_type")

    if content_type == 'messages':
        messages: list[dict[str, int]] = (await state.get_data()).get("messages")
    elif content_type == 'likes':
        likes: list[dict[str, int]] = (await state.get_data()).get("likes")

    if msg.text == '❤️':
        if previous_questionnaire.username != '@test_username':
            if await user.is_too_active_to_me('like', previous_questionnaire.id):
                await user.delete_like_for_me(previous_questionnaire.id)
                text = (f'Кажется мы свели вас кое с кем. Это человек которому вы недавно ставили лайк.\n\n'
                        f'Так что напишите ему @{msg.from_user.username}, тут нечего стесняться')
                kb = None
                await bot.send_message(msg.from_user.id, f'Теперь вы можете написать '
                                                         f'@{previous_questionnaire.username}, так как он тоже '
                                                         f'проявлял знаки внимания к вам')
            else:
                text = "Пользователь поставил вам лайк, показать его анкету?"
                kb = show_likes_for_me_markup()
                await user.set_like_for(previous_questionnaire.id)

            await bot.send_message(previous_questionnaire.id, text, reply_markup=kb)

    elif msg.text == '💌':
        text = 'Напиши сообщение для этого пользователя, и мы отправим ему сообщение.'
        kb = ReplyKeyboardBuilder()
        kb.add(get_cancel_btn())

        await bot.send_message(msg.from_user.id, text, reply_markup=kb.as_markup(resize_keyboard=True))

        await state.set_state(WatchQuestionnaire.wait_message)
        return await state.update_data(questionnaire_msg_user=previous_questionnaire)

    elif msg.text == '👎':
        if content_type == 'messages':
            await user.delete_message_for_me(user_id=previous_questionnaire.id)
        elif content_type == 'likes':
            await user.delete_like_for_me(user_id=previous_questionnaire.id)

    elif only_send is False:
        return await bot.send_message(msg.from_user.id, "Нет такого варианта ответа")

    custom_questionnaires: list[Questionnaire] = (await state.get_data()).get("custom_questionnaires")
    if custom_questionnaires:
        questionnaire = custom_questionnaires[0]
        custom_questionnaires.pop(0)
        await state.update_data(custom_questionnaires=custom_questionnaires)

    else:
        skip: list = (await state.get_data()).get("skip_questionnaires_ids") or []
        try:
            all_questionnaires = await AllUsers().get_users_questionnaires(
                my_user_id=msg.from_user.id, skip=skip
            )

            questionnaire = all_questionnaires[0]
        except IndexError:
            await bot.send_message(
                msg.from_user.id,
                "Поиск анкет закончен, попробуйте через пару часов"
            )
            return await reset_questionnaires(msg=msg, state=state)
        skip.append(questionnaire.id)
        await state.update_data(skip_questionnaires_ids=skip)

    await state.update_data(previous_questionnaire=questionnaire)

    if not (await state.get_data()).get("custom_questionnaires") and (await state.get_data()).get("content_type"):
        if content_type == 'messages':
            word = 'Сообщения'

        elif content_type == 'likes':
            word = 'Лайки'

        await bot.send_message(msg.from_user.id, f"{word} закончились, но они еще будут!")
        return await reset_questionnaires(msg=msg, state=state)

    else:
        try:
            msgs = await bot.send_media_group(msg.from_user.id, questionnaire.get_questionnaire().build())
        except TelegramBadRequest as tbr:
            await bot.send_message(msg.from_user.id, "Не удается отправить анкету, смотрите следующую")
            raise tbr
        else:
            await check_and_replace_photo_url(messages=msgs, questionnaire=questionnaire)
            await bot.send_message(msg.from_user.id, "Вы можете пожаловаться на анкету",
                                   reply_markup=get_complaint_report_mp(questionnaire.id).as_markup())

    if content_type == 'messages' and messages:
        await bot.send_message(msg.from_user.id, messages[0]["message"])
        messages.pop(0)
        await state.update_data(messages=messages)
    elif content_type == 'likes' and likes:
        likes.pop(0)
        await state.update_data(likes=likes)


@dp.callback_query(lambda call: call.data.startswith('complaint_for'))
async def complaint_on_questionnaire(call: CallbackQuery):
    questionnaire_id = int(call.data.split('complaint_for_')[1])
    questionnaire_msg = call.message

    await call.message.edit_text(
        questionnaire_msg.text,
        reply_markup=get_choice_complaint(questionnaire_id).as_markup()
    )


@dp.callback_query(lambda call: call.data.startswith("block_report"))
async def block_report_questionnaire(call: CallbackQuery):
    user_id = int(call.data.split('_')[-1])
    questionnaire = await AllUsers().get_questionnaire_by_id(user_id)

    if call.data.count('strangers_indecent_photos'):
        cause = "<b> Чужие или не приличные фото</b>"
        callback_data_clause = 'strangers_indecent_photos'
    elif call.data.count('rudeness_in_description'):
        cause = "<b>🤬 Грубость в описании</b>"
        callback_data_clause = 'rudeness_in_description'
    elif call.data.count('rudeness_in_communication'):
        cause = "<b>💢 Грубость в общении</b>"
        callback_data_clause = 'rudeness_in_communication'

    text = f'Поступила жалоба на анкету:\n' \
           f'Причина: <i>{cause}</i>'

    msg = await bot.send_message(
        chat_id=admin_id,
        text=text,
        reply_markup=get_freeze_questionnaire_mp(user_id, callback_data_clause).as_markup()
    )

    await bot.pin_chat_message(admin_id, msg.message_id)
    await bot.send_media_group(admin_id, questionnaire.get_questionnaire().build())


async def reset_questionnaires(msg: Message, state: FSMContext):
    await state.clear()
    text = (f"1. Заполнить анкету заново.\n"
            f"2. Изменить фото/видео.\n"
            f"3. Изменить текст анкеты.\n"
            f"4. Смотреть анкеты.\n"
            f"5. Посмотреть мою анкету")
    await bot.send_message(msg.from_user.id, text, reply_markup=get_general_keyboard(5))


async def wait_for_message(msg: Message, state: FSMContext):
    questionnaire = (await state.get_data())["questionnaire_msg_user"]
    user = User(msg.from_user.id)

    if msg.text == 'Вернуться назад':
        data: dict = (await state.get_data())
        data.pop('questionnaire_msg_user')

        await state.set_data(data)
        await state.set_state(WatchQuestionnaire.main)
        await bot.send_message(msg.from_user.id, "Отменено", reply_markup=get_watch_questionnaire_markup())
        await watch_questionnaires_loop(msg=msg, state=state)

    else:
        if len(msg.text) <= 3:
            return await bot.send_message(msg.from_user.id, "Сообщение слишком короткое")

        text_for_watcher = "Лайк отправлен, ждем ответа"
        if questionnaire.username != '@test_username':
            if await user.is_too_active_to_me('message', questionnaire.id):
                await user.delete_like_for_me(questionnaire.id)
                await user.delete_message_for_me(questionnaire.id)
                text = (f"Пользователь @{msg.from_user.username} отправил вам встречное сообщение! "
                        f"Есть взаимный интерес.\nА вот кстати и его сообщение:\n"
                        f"<b>{msg.text}</b>")
                kb = None
            else:
                await user.set_message_for(questionnaire.id, msg.text)
                text = "Тебе пришло новое сообщение, показать?"
                kb = show_messages_for_me_markup()

            await bot.send_message(questionnaire.id, text, reply_markup=kb)
            text_for_watcher = (f'Теперь вы можете написать @{questionnaire.username}, '
                                f'так как он тоже проявлял знаки внимания к вам')

        await state.set_state(WatchQuestionnaire.main)
        kb = get_watch_questionnaire_markup()
        await bot.send_message(msg.from_user.id, text_for_watcher, reply_markup=kb)
        await watch_questionnaires_loop(msg=msg, state=state)


def register_watch_questionnaire_handlers():
    dp.message.register(watch_questionnaires_loop, WatchQuestionnaire.main)
    dp.message.register(wait_for_message, WatchQuestionnaire.wait_message)
