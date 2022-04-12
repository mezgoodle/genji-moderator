from aiogram import Dispatcher
from aiogram.types import Message, chat_permissions

from datetime import timedelta
from template.tgbot.misc.seconds import work_with_user


async def mute_user(message: Message):
    if not message.reply_to_message:
        return await message.reply('This command need to be as reply on message')
    await message.delete()

    user_id = message.reply_to_message.from_user.id
    engine = message.bot.get('engine')
    seconds = await work_with_user(user_id, 'mutes', engine)

    await message.bot.restrict_chat_member(chat_id=message.chat.id, user_id=user_id,
                                           until_date=timedelta(seconds=seconds),
                                           permissions=chat_permissions.ChatPermissions(can_send_messages=False,
                                                                                        can_send_polls=False,
                                                                                        can_send_other_messages=False,
                                                                                        can_send_media_messages=False))
    return await message.reply_to_message.reply(f'User has been muted for the {seconds} seconds')


def register_mute(dp: Dispatcher):
    dp.register_message_handler(mute_user, is_admin=True, commands=['mute'], commands_prefix='!/')
