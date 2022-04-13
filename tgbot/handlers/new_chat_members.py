from aiogram import Dispatcher
from aiogram.types import Message


async def on_user_joined(message: Message):
    await message.delete()


def register_join(dp: Dispatcher):
    dp.register_message_handler(on_user_joined, content_types=['new_chat_members'])
