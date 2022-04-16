from aiogram.types import Message

from tgbot.misc.seconds import work_with_user
from tgbot.misc.checks import check_warns
from loader import dp

from datetime import timedelta
import logging


@dp.message_handler(is_admin=True, commands=['warn'], commands_prefix='!/')
async def warn_user(message: Message):
    logger = logging.getLogger(__name__)
    logger.info('Handler executed')
    if not message.reply_to_message:
        return await message.reply('This command need to be as reply on message')
    await message.delete()

    user_id = message.reply_to_message.from_user.id
    engine = message.bot.get('engine')
    _ = await work_with_user(user_id, 'warns', engine)
    ban, warns = await check_warns(user_id, engine)
    if ban:
        await message.bot.ban_chat_member(chat_id=message.chat.id, user_id=user_id, until_date=timedelta(seconds=29))
        return await message.reply_to_message.reply('User has been banned because of his three warns')
    return await message.reply_to_message.reply(f'Now user has {warns} warn(s)')
