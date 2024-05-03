import asyncio
import random
from typing import Any

from sqlalchemy import select, update, delete, insert, exc, Row
from sqlalchemy.exc import IntegrityError

from src.database._base import Database, Users, get_db, Comunication
from src.database.questionnaires import Questionnaire
from src.utils.location import haversine

select
update
delete
insert


class User:
    """Пользователь бота"""
    _db: Database
    _table_users = Users
    _table_comunication = Comunication
    id: int

    def __init__(self, id: int, db: Database = None):
        if not db:
            db = get_db()
        self._db = db
        self.id = id

    async def is_exists(self):
        query = select(self._table_users.photos_id).where(self._table_users.id == self.id)

        if await self._db.fetchval(query):
            return True
        else:
            return False

    async def insert_id_user(self, id: int):
        db = self._db
        query = insert(self._table_users).values(id=id)
        try:
            await db.execute(query)
        except IntegrityError:
            pass

    async def name(self):
        query = select(self._table_users.name).where(self._table_users.id == self.id)
        return await self._db.fetchval(query)

    async def get_age(self):
        query = select(self._table_users.age).where(self._table_users.id == self.id)
        return await self._db.fetchval(query)

    async def earn(self):
        query = select(self._table_users.earn).where(self._table_users.id == self.id)
        res = await self._db.fetchval(query)
        return res

    async def hide_earn(self) -> bool:
        query = select(self._table_users.hide_earn).where(self._table_users.id == self.id)
        res = await self._db.fetchval(query)
        return res

    async def zodiac_sign(self):
        query = select(self._table_users.zodiac_sign).where(self._table_users.id == self.id)
        return await self._db.fetchval(query)

    async def get_location(self, city: bool = False):
        if city:
            query = select(self._table_users.city).where(self._table_users.id == self.id)
        else:
            query = select(self._table_users.location).where(self._table_users.id == self.id)

        data = await self._db.fetchval(query)

        return data

    async def get_photos(self) -> dict:
        query = select(self._table_users.photos_id).where(self._table_users.id == self.id)
        return await self._db.fetchval(query)

    async def get_gender(self):
        query = select(self._table_users.gender).where(self._table_users.id == self.id)
        return await self._db.fetchval(query)

    async def description(self):
        query = select(self._table_users.description).where(self._table_users.id == self.id)
        return await self._db.fetchval(query)

    async def height(self):
        query = select(self._table_users.height).where(self._table_users.id == self.id)
        return await self._db.fetchval(query)

    async def field_of_activity(self) -> str:
        query = select(self._table_users.field_of_activity).where(self._table_users.id == self.id)
        return await self._db.fetchval(query)

    async def change_photos(self, photos_id: dict[str, list[str]]):
        query = update(self._table_users).values(photos_id=photos_id).where(self._table_users.id == self.id)
        return await self._db.execute(query)

    async def change_description(self, description):
        query = update(User._table_users).values(description=description).where(self._table_users.id == self.id)
        return await self._db.execute(query)

    async def set_cause_hide_questionnaire(self, cause: str):
        query = update(self._table_users).values(cause_hiden_questionnaire=cause).where(
            self._table_users.id == self.id
        )
        return await self._db.execute(query=query)

    async def get_cause_hide_questionnaire(self) -> str:
        query = select(self._table_users.cause_hiden_questionnaire).where(
            self._table_users.id == self.id
        )
        return await self._db.fetchval(query=query)

    async def insert_full_info_user(
            self,
            name: str,
            gender: str,
            age: int,
            zodiac_sign: str,
            height: int,
            location: str,
            photos_id: list[str],
            description: str,
            city: str,
            username: str,
            gender_interests: str,
            field_of_activity: str = False,
            earn: int = None
    ) -> None:
        """
        :param gender_interests: Кого ищет пользователль
        :param field_of_activity: Сфера деятельности
        :param username: Username
        :param city: Город, где проживает
        :param name: Имя пользователя (Костя, Константин или Константин Павлович)
        :param gender: Пол
        :param age: Возраст
        :param zodiac_sign:  Знак зодиака
        :param height: Рост в сантиметрах
        :param earn: Заработок
        :param location:  Геолокация
        :param photos_id:  File id фотографий пользователей
        :param description: Описание анкеты
        """

        db = self._db

        query = insert(self._table_users).values(
            id=self.id,
            username=username,
            name=name,
            gender=gender,
            age=age,
            zodiac_sign=zodiac_sign,
            earn=earn,
            field_of_activity=field_of_activity,
            photos_id=photos_id,
            height=height,
            location=location,
            city=city,
            description=description,
            gender_interests=gender_interests,
        )

        try:
            await db.execute(query)
        except exc.IntegrityError:
            query = update(self._table_users).values(
                name=name,
                gender=gender,
                username=username,
                age=age,
                zodiac_sign=zodiac_sign,
                earn=earn,
                photos_id=photos_id,
                height=height,
                location=location,
                description=description,
                gender_interests=gender_interests,
                city=city
            ).where(self._table_users.id == self.id)
            await db.execute(query)

    async def delete_user(self, user_id: int):
        db = self._db
        query = delete(self._table_users).where(self._table_users.id == user_id)
        await db.execute(query=query)

    async def update_user(self, **columns: Any):
        db = self._db
        query = update(self._table_users).values(**columns)
        await db.execute(query)

    async def get_name(self):
        query = select(self._table_users.name).where(self._table_users.id == self.id)
        return await self._db.fetchval(query)

    async def get_likes_for_me(self) -> list[dict[str, int]]:
        query = select(self._table_comunication.from_id).where(self._table_comunication.for_id == self.id,
                                                               self._table_comunication.type == 'like')
        res = await self._db.fetch(query)
        return [{"id": id[0]} for id in res]

    async def hide_questionnaire(self, cause: str):
        await self.set_cause_hide_questionnaire(cause=cause)

        query = update(self._table_users).values(disabled=True, hiden_questionnaire=True).where(
            self._table_users.id == self.id
        )
        return await self._db.execute(query)

    async def open_questionnaire(self):
        query = update(self._table_users).values(disabled=False,
                                                 hiden_questionnaire=False,
                                                 cause_hiden_questionnaire=None).where(
            self._table_users.id == self.id
        )
        return await self._db.execute(query)

    async def is_hiden_questionnaire(self) -> bool:
        query = select(self._table_users.hiden_questionnaire).where(self._table_users.id == self.id)
        return await self._db.fetchval(query)

    async def get_messages_for_me(self) -> list[dict[str, int | Any]]:
        query = select(self._table_comunication.content,
                       self._table_comunication.from_id).where(self._table_comunication.for_id == self.id,
                                                               self._table_comunication.type == 'message')
        res = await self._db.fetch(query)
        data = []

        index = 0
        for row in res:
            if not row[0] or not row[1]:
                continue

            data.append({})
            for item in row:
                if isinstance(item, int):
                    data[index]["id"] = item
                elif isinstance(item, str):
                    data[index]["message"] = item
            index += 1

        try:
            data.remove({})
        except ValueError:
            pass

        return data

        # return [
        #     {"id": data[0], "message": data[1]} for data in res
        # ]

    async def delete_message_for_me(self, user_id: int) -> None:
        query = delete(self._table_comunication).where(self._table_comunication.from_id == user_id,
                                                       self._table_comunication.type == 'message')
        return await self._db.execute(query)

    async def delete_like_for_me(self, user_id: int) -> None:
        query = delete(self._table_comunication).where(self._table_comunication.from_id == user_id,
                                                       self._table_comunication.type == 'like')
        return await self._db.execute(query)

    async def is_too_active_to_me(self, content_type: str, user_id: int) -> bool:
        query_for = select(self._table_comunication.id_row).where(self._table_comunication.for_id == self.id,
                                                                  self._table_comunication.from_id == user_id,
                                                                  self._table_comunication.type == content_type)
        query_from = select(self._table_comunication.id_row).where(self._table_comunication.from_id == self.id,
                                                                   self._table_comunication.for_id == user_id,
                                                                   self._table_comunication.type == content_type)
        found_for_me = await self._db.fetchval(query_for)
        found_from_me = await self._db.fetchval(query_from)

        if found_for_me or found_from_me:
            return True

        return False

    async def swift_earn_permission(self):
        query_select = select(self._table_users.hide_earn).where(self._table_users.id == self.id)
        hide_earn = await self._db.fetchval(query_select)

        query_update = update(self._table_users).values(hide_earn=not hide_earn).where(self._table_users.id == self.id)
        await self._db.execute(query_update)
        return not hide_earn

    async def delete_active_for_me(self, content_type: str) -> None:
        query = delete(self._table_comunication).where(self._table_comunication.for_id == self.id,
                                                       self._table_comunication.type == content_type)
        await self._db.execute(query)

    async def set_like_for(self, user_id_for_like: int) -> bool:
        query = insert(self._table_comunication).values(type='like', from_id=self.id, for_id=user_id_for_like)
        await self._db.execute(query)
        return await self.is_too_active_to_me("message", user_id=user_id_for_like)

    async def set_message_for(self, user_id_for_message: int, msg: str) -> bool:
        await self.set_like_for(user_id_for_like=user_id_for_message)
        query = insert(self._table_comunication).values(type='message',
                                                        from_id=self.id,
                                                        for_id=user_id_for_message,
                                                        content=msg)
        await self._db.execute(query)

        return await self.is_too_active_to_me("message", user_id=user_id_for_message)

    async def set_filter_by_age(self, from_value: int, to_value: int):
        value = [from_value, to_value]
        query = update(self._table_users).values(filter_by_age=value).where(
            self._table_users.id == self.id
        )

        await self._db.execute(query=query)

    async def set_filter_by_height(self, from_value: int, to_value: int):
        value = [from_value, to_value]
        query = update(self._table_users).values(filter_by_height=value).where(
            self._table_users.id == self.id
        )

        await self._db.execute(query=query)

    async def set_filter_by_distance(self, to_value: int | float):
        query = update(self._table_users).values(filter_by_distance=to_value).where(
            self._table_users.id == self.id
        )

        await self._db.execute(query=query)

    async def set_filter_by_city(self, city: str):
        query = update(self._table_users).values(filter_by_city=city).where(
            self._table_users.id == self.id
        )

        await self._db.execute(query=query)

    async def set_filter_by_activity(self, activity: str):
        query = update(self._table_users).values(filter_by_activity=activity).where(
            self._table_users.id == self.id
        )

        await self._db.execute(query=query)

    async def get_filter_by_age(self):
        query = select(self._table_users.filter_by_age).where(
            self._table_users.id == self.id
        )

        return await self._db.fetchval(query=query)

    async def get_filter_by_height(self):
        query = select(self._table_users.filter_by_height).where(
            self._table_users.id == self.id
        )

        return await self._db.fetchval(query=query)

    async def get_filter_by_distance(self):
        query = select(self._table_users.filter_by_distance).where(
            self._table_users.id == self.id
        )

        return await self._db.fetchval(query=query)

    async def get_filter_by_city(self):
        query = select(self._table_users.filter_by_city).where(
            self._table_users.id == self.id
        )

        return await self._db.fetchval(query=query)

    async def get_filter_by_activity(self):
        query = select(self._table_users.filter_by_activity).where(
            self._table_users.id == self.id
        )

        return await self._db.fetchval(query=query)

    async def get_gender_interests(self):
        query = select(self._table_users.gender_interests).where(self._table_users.id == self.id)
        return await self._db.fetchval(query)

    async def clear_filters(self):
        query = update(self._table_users).values(filter_by_distance=None,
                                                 filter_by_age=None,
                                                 filter_by_height=None,
                                                 filter_by_city=None,
                                                 filter_by_activity=None).where(self._table_users.id == self.id)
        return await self._db.execute(query)


class AllUsers:
    _db: Database
    _table_comunication = Comunication
    _table_users = Users

    def __init__(self, database: Database = None, url_db: str = None):
        if not database:
            database = get_db(url=url_db)

        self._db = database

    async def get_ids_all_users(self) -> list:
        query = select(self._table_users.id)
        users_ids = [value[0] for value in await self._db.fetch(query)]
        return users_ids

    async def get_questionnaire_by_id(self, user_id: int) -> Questionnaire:
        query = select(self._table_users.id,
                       self._table_users.name,
                       self._table_users.age,
                       self._table_users.city,
                       self._table_users.description,
                       self._table_users.photos_id,
                       self._table_users.zodiac_sign,
                       self._table_users.hide_earn,
                       self._table_users.height,
                       self._table_users.earn,
                       self._table_users.username,
                       self._table_users.field_of_activity,
                       self._table_users.gender).where(self._table_users.id == user_id)

        data = await self._db.fetch(query=query)
        if isinstance(data, Row):
            data = (data,)

        questionnaires = []
        for row in data:
            questionnaire = {}

            questionnaire["id"] = row[0]
            questionnaire["name"] = row[1]
            questionnaire["age"] = row[2]
            questionnaire["location"] = row[3]
            questionnaire["city"] = row[3]
            questionnaire["description"] = row[4]
            questionnaire["photos_id"] = row[5]
            questionnaire["zodiac_sign"] = row[6]
            questionnaire["hide_earn"] = row[7]
            questionnaire["height"] = row[8]
            questionnaire["earn"] = row[9]
            questionnaire["username"] = row[10]
            questionnaire["field_of_activity"] = row[11]
            questionnaire["gender"] = row[12]

            questionnaires.append(questionnaire)

        random.shuffle(questionnaires)

        return [Questionnaire(**user) for user in questionnaires][0]

    async def get_users_questionnaires(self,
                                       my_user_id: int,
                                       limit: int | None = 50,
                                       skip: list[int] | None = None,
                                       user_id: int = None) -> list[Questionnaire]:
        user = User(my_user_id)

        city = await user.get_filter_by_city()
        height = await user.get_filter_by_height()
        activity = await user.get_filter_by_activity()
        age = await user.get_filter_by_age()
        distance = await user.get_filter_by_distance()
        my_coordinates = await user.get_location()
        gender_interests = await user.get_gender_interests()

        query = select(self._table_users.id,
                       self._table_users.name,
                       self._table_users.age,
                       self._table_users.city,
                       self._table_users.description,
                       self._table_users.photos_id,
                       self._table_users.zodiac_sign,
                       self._table_users.hide_earn,
                       self._table_users.height,
                       self._table_users.earn,
                       self._table_users.username,
                       self._table_users.field_of_activity,
                       self._table_users.location,
                       self._table_users.gender).where(self._table_users.id != my_user_id)

        if not user_id:
            query = query.where(self._table_users.hiden_questionnaire == False)
            if gender_interests != 'Все равно':
                if gender_interests.lower().count('парни'):
                    gender = 'Я парень'
                    query = query.where(self._table_users.gender == gender)
                elif gender_interests.lower().count('девушки'):
                    gender = 'Я девушка'
                    query = query.where(self._table_users.gender == gender)

            if activity:
                query = query.where(self._table_users.field_of_activity == activity)
            if age:
                query = query.where(self._table_users.age >= age[0],
                                    self._table_users.age <= age[1])
            if height:
                query = query.where(self._table_users.height >= height[0],
                                    self._table_users.height <= height[1])
            if city:
                query = query.where(self._table_users.city == city)
        if limit:
            query = query.limit(limit)
        if skip:
            query = query.filter(self._table_users.id.not_in(skip))
        if user_id:
            query = query.where(self._table_users.id == user_id)

        data = await self._db.fetch(query)

        if isinstance(data, Row):
            data = (data,)

        questionnaires = []
        for row in data:
            if distance:
                if haversine(pos1=my_coordinates, pos2=row[12]) > distance:
                    continue

            questionnaire = {}

            questionnaire["id"] = row[0]
            questionnaire["name"] = row[1]
            questionnaire["age"] = row[2]
            questionnaire["city"] = row[3]
            questionnaire["description"] = row[4]
            questionnaire["photos_id"] = row[5]
            questionnaire["zodiac_sign"] = row[6]
            questionnaire["hide_earn"] = row[7]
            questionnaire["height"] = row[8]
            questionnaire["earn"] = row[9]
            questionnaire["username"] = row[10]
            questionnaire["field_of_activity"] = row[11]
            questionnaire["location"] = row[12]
            questionnaire["gender"] = row[13]

            questionnaires.append(questionnaire)

        random.shuffle(questionnaires)
        data = [Questionnaire(**user) for user in questionnaires]
        random.shuffle(data)
        return data


async def main():
    user = User(0, get_db())
    # print(await user.is_exists())
    # users = AllUsers()
    # for questionnaire in await users.get_users_questionnaires(skip=[]):
    #     print(questionnaire.get_questionnaire())
    # print(await user.get_messages_for_me())
    questionnaires = await AllUsers().get_users_questionnaires(0, limit=None)
    for q in questionnaires:
        print(f"Name: {q.name}, Field_of_activity: {q.field_of_activity}, Id: {q.id}, Age: {q.age}, "
              f"Sity: {q.city}, Height: {q.height}, Gender: {q.gender}")
    print(len(questionnaires))
    ...


if __name__ == '__main__':
    asyncio.run(main())
