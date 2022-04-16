from aiogram.types import Message

from loader import dp

import logging


@dp.message_handler(content_types=['new_chat_members'])
async def on_user_joined(message: Message):
    logger = logging.getLogger(__name__)
    logger.info('Handler executed')
    await message.delete()
