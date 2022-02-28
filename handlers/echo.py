from loader import dp

@dp.message_handler()
async def echo(message):
    await message.answer(message.text)
