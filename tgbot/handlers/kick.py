from aiogram.types import Message, ChatType

from tgbot.misc.seconds import work_with_user
from loader import dp

from datetime import timedelta
import logging


@dp.message_handler(is_admin=True, commands=['kick'], commands_prefix='!/',
                    chat_type=[ChatType.GROUP, ChatType.SUPERGROUP])
async def kick_user(message: Message):
    logger = logging.getLogger(__name__)
    logger.info('Handler executed')
    if not message.reply_to_message:
        return await message.reply('This command need to be as reply on message')
    await message.delete()

    user_id = message.reply_to_message.from_user.id
    engine = message.bot.get('engine')
    seconds = await work_with_user(user_id, 'kicks', engine)

    await message.bot.ban_chat_member(chat_id=message.chat.id, user_id=user_id, until_date=timedelta(seconds=seconds))
    return await message.reply_to_message.reply(f'User has been kicked for the {seconds} seconds')
