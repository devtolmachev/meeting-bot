from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardButton


def get_gender_markup() -> ReplyKeyboardMarkup:
    btn1 = KeyboardButton(text="Я девушка")
    btn2 = KeyboardButton(text="Я парень")
    return ReplyKeyboardBuilder().add(btn1, btn2).as_markup(resize_keyboard=True)


def get_skip_markup() -> ReplyKeyboardMarkup:
    btn1 = KeyboardButton(text="Пропустить")
    return ReplyKeyboardBuilder().add(btn1).as_markup(resize_keyboard=True)


def get_field_of_activity_markup() -> ReplyKeyboardMarkup:
    fields_of_activity = [
        "Наёмный сотрудник",
        'Руководящая должность',
        "Предприниматель",
        "Артист",
        "Блогер",
        "Чиновник"
    ]

    kb = ReplyKeyboardBuilder()
    for text in fields_of_activity:
        kb.add(KeyboardButton(text=text))

    kb.adjust(3)
    return kb.as_markup(resize_keyboard=True)


def get_gender_interests_markup() -> ReplyKeyboardMarkup:
    btn1 = KeyboardButton(text="Девушки")
    btn2 = KeyboardButton(text="Парни")
    btn3 = KeyboardButton(text="Все равно")
    return ReplyKeyboardBuilder().add(btn1, btn2, btn3).as_markup(resize_keyboard=True)


def get_location_markup() -> ReplyKeyboardMarkup:
    btn = KeyboardButton(text='📍 Отправить мои координаты', request_location=True)
    b = ReplyKeyboardBuilder()
    b.add(btn)
    b.adjust(1)
    return b.as_markup(resize_keyboard=True)


def get_all_cool_markup() -> ReplyKeyboardMarkup:
    btn1 = KeyboardButton(text='Да')
    btn2 = KeyboardButton(text='Изменить анкету')
    b = ReplyKeyboardBuilder()
    b.add(btn1, btn2)
    return b.as_markup(resize_keyboard=True)


def get_yes_or_no_markup() -> ReplyKeyboardMarkup:
    btn1 = KeyboardButton(text='Да')
    btn2 = KeyboardButton(text='Нет')
    b = ReplyKeyboardBuilder()
    b.add(btn1, btn2)
    return b.as_markup(resize_keyboard=True)


def get_set_photos_btn() -> ReplyKeyboardMarkup:
    btn = KeyboardButton(text='Это все, сохранить фото')
    b = ReplyKeyboardBuilder()
    b.add(btn)
    return b.as_markup(resize_keyboard=True)


def get_earn_markup() -> ReplyKeyboardMarkup:
    btn1 = KeyboardButton(text='До 100.000 рублей')
    btn2 = KeyboardButton(text='До 500.000 рублей')
    btn3 = KeyboardButton(text='До 1.000.000 рублей')
    btn4 = KeyboardButton(text='Больше 1.000.000 рублей')
    b = ReplyKeyboardBuilder()
    b.add(btn1, btn2, btn3, btn4)
    b.adjust(2)
    return b.as_markup(resize_keyboard=True)


def get_zodiacs_signs_markup() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    zodiacs_signs = [
        'Овен',
        'Телец',
        'Близнецы',
        'Рак',
        'Лев',
        'Дева',
        'Весы',
        'Скорпион',
        'Стрелец',
        'Козерог',
        'Водолей',
        'Рыбы'
    ]
    for text in zodiacs_signs:
        kb.add(KeyboardButton(text=text))

    kb.adjust(3)
    return kb.as_markup(resize_keyboard=True)