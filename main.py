import asyncio
import logging
import os
import traceback

from aiogram.types import BotCommandScopeDefault, BotCommand, ErrorEvent, FSInputFile

from src.database._base import Database
from src.etc.bot import bot, dp, developer_id
from src.etc.filenames import FN_SINGLE_ERROR, FN_FIX_ERRORS
from src.handlers.general import register_general_handlers
from src.utils.middleware import AlbumMiddleware


@dp.error()
async def write_and_send_error(event: ErrorEvent):
    if os.path.exists(FN_FIX_ERRORS) and os.path.getsize(FN_FIX_ERRORS) >= 10000000:
        await bot.send_document(developer_id, FSInputFile(FN_SINGLE_ERROR))
        os.remove(FN_FIX_ERRORS)

    with open(FN_SINGLE_ERROR, 'w') as f:
        f.write(traceback.format_exc())

    with open(FN_FIX_ERRORS, 'a') as f:
        f.write(traceback.format_exc())

    msg = await bot.send_document(developer_id, FSInputFile(FN_SINGLE_ERROR))
    await bot.send_message(developer_id, str(event.exception), reply_to_message_id=msg.message_id)


async def main():
    logging.basicConfig(level=logging.INFO)
    register_general_handlers()
    await Database()
    commands = [
        BotCommand(command='/start', description='Начало'),
        BotCommand(command='/settings', description='Настройки профиля'),
        BotCommand(command='/subscribe', description='Подписка'),
        BotCommand(command='/filter', description='Установить фильтр на просмотр анкет'),
        BotCommand(command='/clear_filters', description='Удалить фильтры')
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())
    dp.message.middleware(AlbumMiddleware())
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
