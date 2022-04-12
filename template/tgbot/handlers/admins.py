from aiogram import Dispatcher
from aiogram.types import Message


async def admins_command(message: Message) -> Message:
    """
    This handler will be called when user sends `/admins` command
    """
    chat_id = message.chat.id
    admins = await message.bot.get_chat_administrators(chat_id)
    text = ''
    for admin in admins:
        text += f'@{admin.user.username} '
    return await message.answer(text, disable_notification=True)


def register_admins(dp: Dispatcher):
    dp.register_message_handler(admins_command, commands=['admins'], state="*")
