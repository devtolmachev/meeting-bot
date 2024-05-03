from datetime import datetime, date


class Zodiac:
    date_: date

    def __init__(self, date_: datetime | date):
        year = datetime.now().date().year
        month = date_.month
        day = date_.day

        date_ = datetime(year, month, day).date()

        self.date_ = date_

    @property
    def zodiac_sign(self) -> str:
        date = self.date_
        year = datetime.now().date().year

        if datetime(year, 3, 21).date() <= date <= datetime(year, 4, 20).date():
            return "Овен"
        elif datetime(year, 4, 21).date() <= date <= datetime(year, 5, 21).date():
            return 'Телец'
        elif datetime(year, 5, 22).date() <= date <= datetime(year, 6, 21).date():
            return 'Близнецы'
        elif datetime(year, 6, 22).date() <= date <= datetime(year, 7, 22).date():
            return 'Рак'
        elif datetime(year, 7, 23).date() <= date <= datetime(year, 8, 23).date():
            return 'Лев'
        elif datetime(year, 8, 24).date() <= date <= datetime(year, 9, 22).date():
            return 'Дева'
        elif datetime(year, 9, 23).date() <= date <= datetime(year, 10, 23).date():
            return 'Весы'
        elif datetime(year, 10, 24).date() <= date <= datetime(year, 11, 22).date():
            return 'Скорпион'
        elif datetime(year, 11, 23).date() <= date <= datetime(year, 12, 21).date():
            return 'Стрелец'
        elif datetime(year, 12, 22).date() <= date <= datetime(year, 1, 20).date():
            return 'Козерог'
        elif datetime(year, 1, 21).date() <= date <= datetime(year, 2, 18).date():
            return 'Водолей'
        elif datetime(year, 2, 19).date() <= date <= datetime(year, 3, 20).date():
            return 'Рыбы'


if __name__ == '__main__':
    date = datetime.strptime('07.10.2005', '%d.%m.%Y').date()
    z = Zodiac(date)
    print(z.zodiac_sign)
