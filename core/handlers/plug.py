from aiogram.types import CallbackQuery

from loader import dp


@dp.callback_query_handler(text=['_'], state='*')
async def plug(callback_query: CallbackQuery):
    await callback_query.answer()
