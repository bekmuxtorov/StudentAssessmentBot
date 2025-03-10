from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove

from loader import dp, db
from states.RegisterState import FSMRegister
from keyboards.default.default_buttons import phone_button, main_button
from data.config import FREE_TRIAL_PERIOD


@dp.callback_query_handler(text="register_user")
async def register_user(call: types.CallbackQuery, state: FSMContext):
    """
    Ro‘yxatdan o‘tish jarayonini boshlaydi.
    """
    await call.message.answer("Iltimos, to‘liq ismingizni yuboring:")
    await state.set_state(FSMRegister.full_name)
    await call.answer()


@dp.message_handler(state=FSMRegister.full_name)
async def process_full_name(message: types.Message, state: FSMContext):
    """
    Foydalanuvchidan ismini qabul qiladi va keyingi bosqichga o‘tadi.
    """
    await state.update_data(full_name=message.text)
    await message.answer("Iltimos, telefon raqamingizni kiriting yoki quyidagi tugma orqali ulashing:", reply_markup=phone_button)
    await state.set_state(FSMRegister.phone_number)


@dp.message_handler(lambda message: message.contact, content_types=types.ContentType.CONTACT, state=FSMRegister.phone_number)
async def process_phone_number_contact(message: types.Message, state: FSMContext):
    """
    Foydalanuvchi tugma orqali telefon raqamini ulashgan holatda ishlaydi.
    """
    phone_number = message.contact.phone_number
    await finalize_registration(message, state, phone_number)


@dp.message_handler(state=FSMRegister.phone_number)
async def process_phone_number_text(message: types.Message, state: FSMContext):
    """
    Foydalanuvchi qo‘lda telefon raqamini kiritgan holatda ishlaydi.
    """
    phone_number = message.text.strip()

    # Telefon raqami valid ekanligini tekshiramiz
    if not phone_number.startswith("+") or not phone_number[1:].isdigit():
        await message.answer("📌 Iltimos, telefon raqamingizni to‘g‘ri formatda kiriting. Masalan: +998901234567")
        return

    await finalize_registration(message, state, phone_number)


async def finalize_registration(message: types.Message, state: FSMContext, phone_number: str):
    """
    Foydalanuvchini bazaga saqlaydi va ro‘yxatdan o‘tishni yakunlaydi.
    """
    user_data = await state.get_data()
    try:
        await db.add_user(
            full_name=user_data["full_name"],
            phone_number=phone_number,
            telegram_id=message.from_user.id
        )

        await message.answer(f"✅ Siz muvaffaqiyatli ro‘yxatdan o‘tdingiz!\n\nBotdan {FREE_TRIAL_PERIOD} kun davomida bepul to'liq foydalan olasiz!", reply_markup=ReplyKeyboardRemove())
        await message.answer("💡 Asosiy oyna", reply_markup=main_button)
        await state.finish()

    except Exception as e:
        error_message = str(e)

        if "UNIQUE constraint failed: Users.telegram_id" in error_message or "duplicate key value violates unique constraint" in error_message:
            await message.answer("⚠ Siz allaqachon ro‘yxatdan o‘tgansiz. Botdan foydalanishingiz mumkin!")
        else:
            await message.answer("❌ Ro‘yxatdan o‘tishda xatolik yuz berdi. Iltimos, keyinroq urinib ko‘ring yoki administratorga murojaat qiling.")

        await state.finish()
