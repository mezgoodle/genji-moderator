from aiogram.types import Message

from loader import dp

import logging


@dp.message_handler(commands=['admins'])
async def admins_command(message: Message) -> Message:
    logger = logging.getLogger(__name__)
    logger.info('Handler executed')
    chat_id = message.chat.id
    admins = await message.bot.get_chat_administrators(chat_id)
    text = ''
    for admin in admins:
        text += f'@{admin.user.username} '
    return await message.answer(text, disable_notification=True)
