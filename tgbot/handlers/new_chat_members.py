from aiogram.types import Message, ChatType

from loader import dp

import logging


@dp.message_handler(content_types=['new_chat_members'], chat_type=[ChatType.GROUP, ChatType.SUPERGROUP])
async def on_user_joined(message: Message):
    logger = logging.getLogger(__name__)
    logger.info('Handler executed')
    await message.delete()
