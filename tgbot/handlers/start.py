from aiogram.types import Message
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp

import logging


@dp.message_handler(CommandStart())
async def start_command(message: Message) -> Message:
    logger = logging.getLogger(__name__)
    logger.info('Handler executed')
    return await message.answer('Add a bot to the chat, give the administrator permissions and use it')
