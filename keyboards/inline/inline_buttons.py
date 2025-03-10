from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def become_member_buttons(must_member: dict):
    become_member = InlineKeyboardMarkup(row_width=1)
    for channel, title in must_member.items():
        channel_link = f'https://{channel}.t.me'
        button = InlineKeyboardButton(text=title, url=f"{channel_link}")
        become_member.insert(button)

    check_button = InlineKeyboardButton(
        text='🔔 Obuna bo\'ldim', callback_data="check_button")
    become_member.insert(check_button)
    return become_member


register_button = InlineKeyboardMarkup().add(
    InlineKeyboardButton("📌 Ro‘yxatdan o‘tish",
                         callback_data="register_user")
)

payment_button = InlineKeyboardMarkup().add(
    InlineKeyboardButton("🖇 To'lov chekini yuborish",
                         callback_data="payment")
)
