from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton


def get_complaint_report_mp(questionnaire_id: int) -> InlineKeyboardBuilder:
    btn = InlineKeyboardButton(text="Отправить жалобу на анкету", callback_data=f"complaint_for_{questionnaire_id}")
    kb = InlineKeyboardBuilder()
    kb.add(btn)
    return kb


def get_choice_complaint(questionnaire_id: int) -> InlineKeyboardBuilder:
    texts = [["🔞 Чужие или не приличные фото", "strangers_indecent_photos"],
             ["🤬 Грубость в описании", "rudeness_in_description"],
             ["💢 Грубость в общении", "rudeness_in_communication"]]
    kb = InlineKeyboardBuilder()
    for v in texts:
        btn = InlineKeyboardButton(text=v[0], callback_data=f"block_report_{v[1]}_{questionnaire_id}")
        kb.add(btn)

    kb.adjust(1)
    return kb


def get_correct_mp(questionnaire_id: int) -> InlineKeyboardBuilder:
    text = "Исправить анкету"
    callback_data = f'correct_questionnaire_{questionnaire_id}'
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text=text, callback_data=callback_data))
    return kb


def get_freeze_questionnaire_mp(questionnaire_id: int, cause: str) -> InlineKeyboardBuilder:
    btn = InlineKeyboardButton(text="Заморозить анкету",
                               callback_data=f"hide_questionnaire_{questionnaire_id}={cause}")
    kb = InlineKeyboardBuilder()
    kb.add(btn)
    return kb
