from aiogram.types import Message

from datetime import timedelta

from loader import dp

import logging


@dp.message_handler(is_admin=True, commands=['ban'], commands_prefix='!/')
async def ban_user(message: Message):
    logger = logging.getLogger(__name__)
    logger.info('Handler executed')
    if not message.reply_to_message:
        await message.reply('This command need to be as reply on message')
        return
    await message.delete()

    await message.bot.ban_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id,
                                      until_date=timedelta(seconds=29))
    return await message.reply_to_message.reply('User has been banned')


@dp.message_handler(is_admin=True, commands=['unban'], commands_prefix='!/')
async def unban_user(message: Message):
    logger = logging.getLogger(__name__)
    logger.info('Handler executed')
    if not message.reply_to_message:
        await message.reply('This command need to be as reply on message')
        return
    await message.delete()

    await message.bot.unban_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id,
                                        only_if_banned=True)
    username = message.reply_to_message.from_user.username
    return await message.reply_to_message.reply(f'User @{username} has been unbanned')
