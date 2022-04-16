from aiogram.types import Message

from loader import dp

import logging


@dp.message_handler(commands=['dice'])
async def role_dice(message: Message) -> Message:
    logger = logging.getLogger(__name__)
    logger.info('Handler executed')
    return await message.answer_dice()
