from aiogram.types import CallbackQuery, Message
from aiogram.types import InlineKeyboardMarkup

from core.states import FState
from loader import dp, bot, config


@dp.callback_query_handler(state=FState.looking)
async def options(callback_query: CallbackQuery):
    _message = await callback_query.message.edit_reply_markup(InlineKeyboardMarkup())
    if callback_query.data == 'report':
        await bot.send_message(callback_query.from_user.id, 'Опишите жалобу: ')
        await FState.reporting.set()


@dp.message_handler(state=FState.reporting)
async def report(message: Message):
    await bot.send_message(config.bot.admin,
                           f'Репорт от пользователя '
                           f'{message.from_user.username} (id {message.from_user.id}):\n{message.text}'
                           )
    await message.answer(text='Жалоба отправлена!')
    await FState.looking.set()
