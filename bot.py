import logging
import os
from datetime import timedelta
from typing import Tuple

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import config
from database import create_database, get_engine, get_user, update_user, create_user
from filters import IsAdminFilter

# log level
logging.basicConfig(level=logging.INFO)

# bot init
bot = Bot(token=config.TELEGRAM_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# activate filters
dp.filters_factory.bind(IsAdminFilter)

# SQLModel engine
engine: object


async def work_with_user(user_id: str, field_name: str) -> int:
    """
    Get seconds for user
    :param user_id: user's specific identifier
    :param field_name: mute, warn or kick
    :return: number of seconds
    """
    seconds: int
    user = get_user(engine, user_id)
    if user:
        update_user(engine, user_id, field_name, getattr(user, field_name) + 1)
        seconds = (getattr(user, field_name) + 1) * 32
    else:
        user = create_user(engine, {'user_id': user_id, field_name: 1})
        seconds = getattr(user, field_name) * 32
    return seconds


async def check_warns(user_id: str) -> Tuple[bool, int]:
    """
    If user has 3 warns, it will be as ban
    :param user_id: user's specific identifier
    :return: is it a ban and number of warns
    """
    user = get_user(engine, user_id)
    warns = user.warns
    if warns == 3:
        return True, 0
    return False, user.warns


@dp.message_handler(is_admin=True, commands=['ban'], commands_prefix='!/')
async def ban_user(message: types.Message):
    if not message.reply_to_message:
        await message.reply('This command need to be as reply on message')
        return
    await bot.delete_message(message.chat.id, message.message_id)

    await bot.ban_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id,
                              until_date=timedelta(seconds=29))
    return await message.reply_to_message.reply('User has been banned')


@dp.message_handler(is_admin=True, commands=['unban'], commands_prefix='!/')
async def unban_user(message: types.Message):
    if not message.reply_to_message:
        await message.reply('This command need to be as reply on message')
        return
    await bot.delete_message(message.chat.id, message.message_id)

    await bot.unban_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id,
                                only_if_banned=True)
    username = message.reply_to_message.from_user.username
    return await message.reply_to_message.reply(f'User @{username} has been unbanned')


@dp.message_handler(is_admin=True, commands=['kick'], commands_prefix='!/')
async def kick_user(message: types.Message):
    if not message.reply_to_message:
        return await message.reply('This command need to be as reply on message')
    await bot.delete_message(message.chat.id, message.message_id)

    user_id = message.reply_to_message.from_user.id
    seconds = await work_with_user(user_id, 'kicks')

    await bot.ban_chat_member(chat_id=message.chat.id, user_id=user_id, until_date=timedelta(seconds=seconds))
    return await message.reply_to_message.reply(f'User has been kicked for the {seconds} seconds')


@dp.message_handler(is_admin=True, commands=['warn'], commands_prefix='!/')
async def kick_user(message: types.Message):
    if not message.reply_to_message:
        return await message.reply('This command need to be as reply on message')
    await bot.delete_message(message.chat.id, message.message_id)

    user_id = message.reply_to_message.from_user.id
    _ = await work_with_user(user_id, 'warns')
    ban, warns = await check_warns(user_id)
    if ban:
        await bot.ban_chat_member(chat_id=message.chat.id, user_id=user_id, until_date=timedelta(seconds=29))
        return await message.reply_to_message.reply(f'User has been banned because of his three warns')
    return await message.reply_to_message.reply(f'Now user has {warns} warn(s)')


@dp.message_handler(is_admin=True, commands=['mute'], commands_prefix='!/')
async def mute_user(message: types.Message):
    if not message.reply_to_message:
        return await message.reply('This command need to be as reply on message')
    await bot.delete_message(message.chat.id, message.message_id)

    user_id = message.reply_to_message.from_user.id
    seconds = await work_with_user(user_id, 'mutes')

    await bot.restrict_chat_member(chat_id=message.chat.id, user_id=user_id,
                                   until_date=timedelta(seconds=seconds),
                                   permissions=types.chat_permissions.ChatPermissions(can_send_messages=False,
                                                                                      can_send_polls=False,
                                                                                      can_send_other_messages=False,
                                                                                      can_send_media_messages=False))
    return await message.reply_to_message.reply(f'User has been muted for the {seconds} seconds')


@dp.message_handler(is_admin=True, commands=['unmute'], commands_prefix='!/')
async def unmute_user(message: types.Message):
    if not message.reply_to_message:
        return await message.reply('This command need to be as reply on message')
    await bot.delete_message(message.chat.id, message.message_id)

    user_id = message.reply_to_message.from_user.id
    await bot.restrict_chat_member(chat_id=message.chat.id, user_id=user_id,
                                   permissions=types.chat_permissions.ChatPermissions(can_send_messages=True,
                                                                                      can_send_polls=True,
                                                                                      can_send_other_messages=True,
                                                                                      can_send_media_messages=True))
    return await message.reply_to_message.reply(f'User has been unmuted')


@dp.message_handler(commands=['dice'])
async def role_dice(message: types.Message) -> types.Message:
    """
    This handler will be called when user sends `/dice` command
    """
    return await message.answer_dice()


@dp.message_handler(commands=['admins'])
async def admins_command(message: types.Message) -> types.Message:
    """
    This handler will be called when user sends `/admins` command
    """
    chat_id = message.chat.id
    members = await bot.get_chat_administrators(chat_id)
    msg = ''
    for member in members:
        msg += f'@{member.user.username} '
    return await message.answer(msg)


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message) -> types.Message:
    """
    This handler will be called when user sends `/start` command
    """
    return await message.answer('Add a bot to the chat, give the administrator permissions and use it')


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message) -> types.Message:
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


@dp.message_handler(content_types=['new_chat_members'])
async def on_user_joined(message: types.Message):
    await message.delete()


# Webhook settings
HEROKU_APP_NAME = os.getenv('HEROKU_APP_NAME')
WEBHOOK_HOST = f'https://{HEROKU_APP_NAME}.herokuapp.com'
WEBHOOK_PATH = f'/webhook/{config.TELEGRAM_TOKEN}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

# Webserver settings
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = int(os.getenv('PORT', 5000))


# Functions for webhooks
async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)


async def on_shutdown(dp):
    logging.warning('Shutting down..')
    logging.warning('Bye!')


if __name__ == '__main__':

    sqlite_file_name = 'database.db'
    sqlite_url = f'sqlite:///{sqlite_file_name}'
    engine = get_engine(sqlite_url)
    create_database(engine)

    executor.start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT
    )
