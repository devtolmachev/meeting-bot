from aiogram.utils.keyboard import KeyboardButton, ReplyKeyboardBuilder


def get_filters_mp():
    texts = ["Поиск по возрасту",
             "Поиск по предпринимателям",
             "Поиск по росту",
             "Поиск по расстоянию",
             "Поиск по городу"]
    kb = ReplyKeyboardBuilder()
    for text in texts:
        kb.add(KeyboardButton(text=text))

    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)
