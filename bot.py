import config
import logging

from aiogram import Bot, Dispatcher, executor, types

# log level
logging.basicConfig(level=logging.INFO)

# bot init
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)


@dp.message_handler()
async def filter_messages(message: types.Message):
    if 'bad word' in message.text:
        await message.delete()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
