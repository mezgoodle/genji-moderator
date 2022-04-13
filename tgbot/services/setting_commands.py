from aiogram import Bot
from aiogram.types import BotCommand


async def set_default_commands(bot: Bot) -> None:
    commands = [
        BotCommand(command='start', description='Start the bot'),
        BotCommand(command='help', description='Show help'),
        BotCommand(command='admins', description='Show admins of the chat'),
    ]
    await bot.set_my_commands(commands=commands)
