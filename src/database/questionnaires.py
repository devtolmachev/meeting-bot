from aiogram.utils.media_group import MediaGroupBuilder


class Questionnaire:

    def __init__(self,
                 id: int,
                 username: str,
                 name: str,
                 age: int,
                 location: dict,
                 description: str,
                 photos_id: dict,
                 zodiac_sign: str,
                 height: int,
                 earn: str,
                 city: str,
                 gender: str,
                 field_of_activity: str,
                 hide_earn: bool = False):
        self.gender = gender
        self.id = id
        self.name = name
        self.age = age
        self.location = location
        self.description = description
        self.photos_id = photos_id
        self.username = username
        self.zodiac_sign = zodiac_sign
        self.field_of_activity = field_of_activity
        self.hide_earn = hide_earn
        self.earn = earn,
        self.height = height
        self.city = city

    def get_questionnaire(self) -> MediaGroupBuilder:
        text = (f"{self.name}, {self.age}, {self.city}\n\n"
                f"Рост: {self.height}\n"
                f"Знак зодиака: {self.zodiac_sign}\n"
                f"Сфера деятельности: {self.field_of_activity}\n"
                f"Зарабатываю: {self.earn[0]}\n\n"
                f"О себе: {self.description}")

        if self.hide_earn or not self.earn[0]:
            text = text.replace(f'Зарабатываю: {self.earn[0]}\n\n',
                                'Зарабатываю: <i>Не указано</i>\n\n')
        if not self.description:
            text = text.replace(f'О себе: {self.description}',
                                'О себе: <i>Не указано</i>')
        if not self.city:
            text = text.replace(f", {self.city}",
                                ', <i>Город не указан</i>\n')
        if not self.zodiac_sign:
            text = text.replace(f"Знак зодиака: {self.zodiac_sign}\n",
                                'Знак зодиака: <i>Не указан</i>\n')
        if not self.field_of_activity:
            text = text.replace(f"Сфера деятельности: {self.field_of_activity}\n",
                                'Сфера деятельности: <i>Не указана</i>\n')

        mgb = MediaGroupBuilder()
        media = self.photos_id
        for media_type in media:
            for media_file in media[media_type]:
                if media_type == 'photo':
                    mgb.add_photo(media_file)
                elif media_type == 'video':
                    mgb.add_video(media_file)

        mgb.caption = text

        return mgb
