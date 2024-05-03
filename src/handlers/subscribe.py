from aiogram import F
from aiogram.enums import ContentType
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, LabeledPrice, PreCheckoutQuery

from src.etc.bot import dp, bot
from src.etc.payments import provider_token
from src.markups import *


@dp.message(Command('subscribe'))
async def get_subscribe_info(msg: Message):
    text = ("Подписка позволяет делать поиск по следующим пунктам:\n\n"
            "<b>"
            "1. По геолокации. (Пример: до 5км)\n"
            "2. По предпринимателям. (Пример: только предприниматели)\n"
            "3. По возрасту. (Пример: от 20 до 25)\n"
            "4. По городу. (Пример: только Москва)\n"
            "5. По росту. (Пример: от 170 до 180)"
            "</b>")

    await bot.send_message(msg.from_user.id, text, reply_markup=get_subscribe_btn().as_markup())


@dp.callback_query(lambda call: call.data == 'get_subscribe')
async def get_subscribe(call: CallbackQuery, state: FSMContext):
    return await call.answer('Скоро...', show_alert=True)
    photo_url = ('https://img.freepik.com/premium-vector/robot-icon-bot-sign-design-chatbot-symbol-concept-voice'
                 '-support-service-bot-online-support-bot-vector-stock-illustration_100456-34.jpg?w=2000')

    await bot.send_invoice(
        chat_id=call.from_user.id,
        title='Оплата подписки',
        description='Получи возможность искать себе пару по фильтрам',
        payload='test',
        provider_token=provider_token,
        currency='RUB',
        prices=[
            LabeledPrice(
                label='Поиск по 5 параметрам',
                amount=50000
            ),
            LabeledPrice(
                label='НДС',
                amount=5000
            )
        ],
        max_tip_amount=50000,
        suggested_tip_amounts=[1000, 2000, 4000, 5000],
        start_parameter=str(call.from_user.id),
        photo_url=photo_url,
        photo_size=100,
        photo_width=500,
        photo_height=500,
        need_name=True,
        need_email=False,
        need_phone_number=True,
        need_shipping_address=False,
        is_flexible=False,
        disable_notification=False,
        request_timeout=15
    )


@dp.pre_checkout_query
async def pre_checkout_query(pcq: PreCheckoutQuery, state: FSMContext):
    await bot.answer_pre_checkout_query(pcq.id, ok=True)


@dp.message(F.successful_payment)
async def successfull_payment(msg: Message, state: FSMContext):
    await bot.send_message(msg.from_user.id, "Ваша подписка оплачена. Отправьте /start")


def register_pay_handlers():
    ...
