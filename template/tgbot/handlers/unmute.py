from aiogram import Dispatcher
from aiogram.types import Message, chat_permissions


async def unmute_user(message: Message):
    if not message.reply_to_message:
        return await message.reply('This command need to be as reply on message')
    await message.delete()

    user_id = message.reply_to_message.from_user.id
    await message.bot.restrict_chat_member(chat_id=message.chat.id, user_id=user_id,
                                           permissions=chat_permissions.ChatPermissions(can_send_messages=True,
                                                                                        can_send_polls=True,
                                                                                        can_send_other_messages=True,
                                                                                        can_send_media_messages=True))
    return await message.reply_to_message.reply('User has been unmuted')


def register_unmute(dp: Dispatcher):
    dp.register_message_handler(unmute_user, is_admin=True, commands=['unmute'], commands_prefix='!/')
