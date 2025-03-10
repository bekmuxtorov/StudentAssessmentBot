from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup

from datetime import datetime, timedelta

from loader import dp, db
from data.config import ADMINS, FREE_TRIAL_PERIOD, CARD_NUMBER, AMOUNT_PER_MONTH, AMOUNT_PER_MONTH_IN_WORD
from keyboards.inline.inline_buttons import register_button, payment_button


async def check_user_subscription(db, telegram_id: int) -> tuple[bool, str, InlineKeyboardMarkup | None]:
    user = await db.select_user(telegram_id=telegram_id)

    if not user:
        return False, "⚡️Botdan foydalanish uchun ro'yxatdan o'tishingiz kerak.\n\nQuyidagi tugma yordamida ro'yxatdan o'tishingiz mumkin.", register_button

    created_date = datetime.strptime(user["created_date"], "%Y-%m-%d %H:%M:%S")

    if datetime.now() - created_date > timedelta(days=FREE_TRIAL_PERIOD):
        payment = await db.select_payment(user_id=user["id"])

        if not payment or datetime.strptime(payment["end_date"], "%Y-%m-%d") < datetime.now():
            text = "📢 Hurmatli foydalanuvchi! Sizning obunangizni davom ettirish uchun to‘lovni amalga oshirishingizni so‘raymiz.\n\n"
            text += "💳 To‘lov rekvizitlari:\n"
            text += f"Karta raqami: <code>{CARD_NUMBER}</code>\n"
            text += "Egasi: A. Muxtorov\n\n"
            text += f"📌 Oylik obuna narxi: {AMOUNT_PER_MONTH} UZS({AMOUNT_PER_MONTH_IN_WORD})"
            text += "✅ To‘lovni amalga oshirgach, chekni quyidagi tugma orqali bizga yuboring."
            text += "Tushunganingiz uchun rahmat! 🤝"
            return False, text, payment_button

    return True, "Siz botdan foydalanishingiz mumkin.", None


@dp.message_handler(CommandStart(), state="*")
async def bot_start(message: types.Message, state: FSMContext):
    await state.finish()

    is_allowed, response_message, keyboard = await check_user_subscription(db, message.from_user.id)

    if not is_allowed:
        await message.answer(response_message, reply_markup=keyboard)
        return

    await message.answer(response_message)


@dp.callback_query_handler(text_contains="check_button")
async def is_member(call: types.CallbackQuery,):
    user_id = call.from_user.id
    await call.message.delete()
    if call.message.chat.type in (types.ChatType.SUPERGROUP, types.ChatType.GROUP):
        await call.message.answer("💡 Guruhdan foydalanishingiz mumkin!")
        return

    is_allowed, response_message, keyboard = await check_user_subscription(db, call.from_user.id)

    if not is_allowed:
        await call.message.answer(response_message, reply_markup=keyboard)
        return

    await call.message.answer(response_message)
