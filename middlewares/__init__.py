from aiogram import Dispatcher

from loader import dp
from .throttling import ThrottlingMiddleware
from .checking_is_member import Asosiy_checking


if __name__ == "middlewares":
    dp.middleware.setup(Asosiy_checking())
    dp.middleware.setup(ThrottlingMiddleware())
