import asyncio
import random

import numpy as np

from src.database import User


async def main():
    cities_list = ['Москва', 'Волгоград', 'Питер', 'Нижний новгород',
                   'Калуга', 'Воронеж', 'Тюмень', 'Тула', 'Казань', 'Сочи',
                   'Иркутск', 'Краснодар']
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
    gender = ['Я девушка', "Я парень"]
    gender_interests = ['Девушки', 'Парни', "Все равно"]
    earn = ['До 100.000 рублей',
            'До 500.000 рублей',
            'До 1.000.000 рублей',
            'Более 1.000.000 рублей']

    for i in range(1000):
        user = User(round(random.randint(1000000000, 9999999999), 0))
        random.shuffle(fields_of_activity)
        random.shuffle(list(earn))
        random.shuffle(zodiac_list)
        random.shuffle(cities_list)
        names = random.choice([names_man_list, names_woman_list])
        gender = 'Я девушка' if names == names_woman_list else 'Я парень'

        x, y = (np.random.rand(2) - 0.5) * 10
        # min = -5.5
        # max = 5.5
        #
        # x = min + (max - min) * random.random()
        # y = min + (max - min) * random.random()
        coordinates = {"lat": x, 'long': y}
        gender_interest = random.choice(gender_interests)
        ear = random.choice(list(earn))
        field_of_activity = random.choice(fields_of_activity)
        zodiac = random.choice(zodiac_list)
        name = random.choice(names)
        try:
            city = random.choice(list(cities_list))
            photos = {"photo": ["AgACAgIAAxkBAAIXHWUifiF2FWslQq99pw3niW4pFxjJAALdzDEbjXIZSYPWdHxhaoMPAQADAgADeQADMAQ"]}

            await user.insert_full_info_user(name=name, gender=gender,
                                             age=round(random.randint(18, 30), 0),
                                             zodiac_sign=zodiac,
                                             height=round(random.randint(150, 195), 0),
                                             location=coordinates,
                                             photos_id=photos,
                                             description=None,
                                             city=city,
                                             gender_interests=gender_interest,
                                             username='@test_username',
                                             field_of_activity=field_of_activity,
                                             earn=ear)
        except Exception:
            print('пропуск')
            continue


if __name__ == '__main__':
    asyncio.run(main())
