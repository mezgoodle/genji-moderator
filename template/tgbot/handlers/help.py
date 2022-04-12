from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.dispatcher.filters.builtin import CommandHelp


async def help_command(message: Message) -> Message:
    """
    This handler will be called when user sends `/help` command
    """
    return await message.answer("""
User's command:
    /help - get commands
    /admins - get chat admins
    /dice - roll a dice
Administrator's command:
    !warn - give a user warn
    !kick - kick a user
    !ban - ban a user
    !mute - mute a user
    !unmute, !unban - opposite commands
""")


def register_help(dp: Dispatcher):
    dp.register_message_handler(help_command, CommandHelp(), state="*")


