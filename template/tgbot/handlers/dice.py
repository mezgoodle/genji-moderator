from aiogram import Dispatcher
from aiogram.types import Message


async def role_dice(message: Message) -> Message:
    """
    This handler will be called when user sends `/dice` command
    """
    return await message.answer_dice()


def register_dice(dp: Dispatcher):
    dp.register_message_handler(role_dice, commands=['dice'], state="*")


