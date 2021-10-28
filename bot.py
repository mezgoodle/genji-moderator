import config
import logging

from aiogram import Bot, Dispatcher, executor, types

from filters import IsAdminFilter

# log level
logging.basicConfig(level=logging.INFO)

# bot init
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)

# activate filters
dp.filters_factory.bind(IsAdminFilter)


@dp.message_handler(is_admin=True, commands=['ban'], commands_prefix='!/')
async def cmd_ban(message: types.Message):
    if not message.reply_to_message:
        await message.reply('This command need to be as reply on message')
        return
    # await message.bot.delete_message(config.GROUP_ID, message.message_id)
    # await message.bot.kick_chat_member(chat_id=config.GROUP_ID, user_id=message.reply_to_message.from_user.id)

    # await message.reply_to_message.reply('User has been banned')
    await message.reply_to_message.reply('My blade is ready to be unleashed.')


@dp.message_handler(is_admin=True, commands=['kick'], commands_prefix='!/')
async def cmd_ban(message: types.Message):
    if not message.reply_to_message:
        await message.reply('This command need to be as reply on message')
        return
    await bot.delete_message(config.GROUP_ID, message.message_id)
    await message.bot.ban_chat_member(chat_id=config.GROUP_ID, user_id=message.reply_to_message.from_user.id)

    await message.reply_to_message.reply('User has been kicked')
    # await message.reply_to_message.reply('My blade is ready to be unleashed.')


@dp.message_handler(content_types=['new_chat_members'])
async def on_user_joined(message: types.Message):
    await message.delete()


@dp.message_handler()
async def filter_messages(message: types.Message):
    if 'bad word' in message.text:
        await message.delete()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
