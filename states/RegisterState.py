from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMRegister(StatesGroup):
    full_name = State()
    phone_number = State()
