from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.dispatcher.filters.builtin import CommandStart


async def start_command(message: Message) -> Message:
    """
    This handler will be called when user sends `/start` command
    """
    return await message.answer('Add a bot to the chat, give the administrator permissions and use it')


def register_start(dp: Dispatcher):
    dp.register_message_handler(start_command, CommandStart())


