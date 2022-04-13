from aiogram import Dispatcher
from aiogram.types import Message

from datetime import timedelta


async def ban_user(message: Message):
    if not message.reply_to_message:
        await message.reply('This command need to be as reply on message')
        return
    await message.delete()

    await message.bot.ban_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id,
                                      until_date=timedelta(seconds=29))
    return await message.reply_to_message.reply('User has been banned')


async def unban_user(message: Message):
    if not message.reply_to_message:
        await message.reply('This command need to be as reply on message')
        return
    await message.delete()

    await message.bot.unban_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id,
                                        only_if_banned=True)
    username = message.reply_to_message.from_user.username
    return await message.reply_to_message.reply(f'User @{username} has been unbanned')


def register_ban(dp: Dispatcher):
    dp.register_message_handler(ban_user, is_admin=True, commands=['ban'], commands_prefix='!/')
    dp.register_message_handler(unban_user, is_admin=True, commands=['unban'], commands_prefix='!/')
