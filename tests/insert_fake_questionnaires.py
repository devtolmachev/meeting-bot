import asyncio
import random
import traceback

import gspread

from src.database._base import get_db
from src.database.user import User


async def main():
    # Указываем путь к JSON
    gc = gspread.service_account(
        filename='/home/daniil/PycharmProjects/meeting_bot/civil-zodiac-401705-642710337f9a.json')
    # Открываем тестовую таблицу
    sh = gc.open("meeting_bot")
    # Выводим значение ячейки A1
    # data = sh.get_worksheet(1).get('A1:E21')
    data = sh.get_worksheet(2).get('A1:E800')
    cities_list = ['Волгоград', 'Питер', 'Нижний новгород',
                   'Калуга', 'Воронеж', 'Тюмень', 'Тула', 'Казань', 'Сочи',
                   'Иркутск', 'Краснодар']
    moscow_set_times = int(len(data) * 0.9)
    names_woman_list = ['Ира', 'Алиса', 'Юля',
                        'Лена', 'Саша', 'Злата', 'Влада',
                        'Кристина']
    names_man_list = ['Вова', 'Альберт', 'Арсений', 'Влад', 'Андрей']
    zodiac_list = ['Овен', 'Телец', 'Близнецы', 'Рак', "Лев", "Дева",
                   "Весы", "Скорпион", "Стрелец", "Козерог", "Водолей",
                   "Рыбы"]
    fields_of_activity = [
        "Наёмный сотрудник",
        'Руководящая должность',
        "Предприниматель",
        "Артист",
        "Блогер",
        "Чиновник"
    ]
    genders = ['Я девушка', "Я парень"]
    gender_interests = ['Девушки', 'Парни', "Все равно"]
    earn = ['До 100.000 рублей',
            'До 500.000 рублей',
            'До 1.000.000 рублей',
            'Более 1.000.000 рублей']

    min = -5.5
    max = 5.5

    x = min + (max - min) * random.random()
    y = min + (max - min) * random.random()
    coordinates = {"lat": x, 'long': y}

    user = User(0)
    for row in data:

        user.id = round(random.randint(1000000000000, 9999999999999), 0)
        if row[2].count('yandex'):
            continue

        gender_interest = random.choice(gender_interests)
        ear = random.choice(list(earn))
        field_of_activity = random.choice(fields_of_activity)
        zodiac = random.choice(zodiac_list)

        if row[0].lower().count('жен'):
            gender = genders[0]
            name = random.choice(names_woman_list)

        elif row[0].lower().count('муж'):
            gender = genders[1]
            name = random.choice(names_man_list)

        else:
            if row[0] == 'Пол':
                continue

            # print(row)
            raise NotImplementedError

        # print(row)

        try:

            if moscow_set_times:
                moscow_set_times -= 1
                city = 'Москва'
            else:
                city = random.choice(list(cities_list))

            photos = {"photo": [row[2]]}

            await user.insert_full_info_user(name=name, gender=gender,
                                             age=int(row[4]),
                                             zodiac_sign=zodiac,
                                             height=int(row[3]),
                                             location=coordinates,
                                             photos_id=photos,
                                             description=str(row[1]),
                                             city=city,
                                             gender_interests=gender_interest,
                                             username='@test_username',
                                             field_of_activity=field_of_activity,
                                             earn=ear)
        except Exception:
            print(traceback.format_exc(), '\n\n')
            continue


if __name__ == '__main__':
    asyncio.run(main())
