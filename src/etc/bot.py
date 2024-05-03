from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

token = '6525133299:AAGtzs6Rxpw10_mY-fYllz0xQCpOHzw_ZF0'
bot = Bot(token, parse_mode='HTML')
dp = Dispatcher(storage=MemoryStorage())
admin_id = 2027466915
developer_id = 2027466915

