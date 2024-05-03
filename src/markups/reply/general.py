from aiogram.utils.keyboard import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardBuilder


def get_general_keyboard(numbers: int = 4, premium: bool = False) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    for text in range(1, numbers + 1):
        btn = KeyboardButton(text=str(text))
        kb.add(btn)

    kb.adjust(5)

    if premium is True:
        texts = ['Поиск по растоянию', 'Поиск по росту',
                 'Поиск по городу', 'Поиск по возрасту',
                 'Поиск по предпринимателям']
        for text in texts:
            kb.add(KeyboardButton(text=text))

        kb.adjust(3)

    return kb.as_markup(resize_keyboard=True)


def get_cancel_btn():
    btn = KeyboardButton(text='Вернуться назад')
    return btn
