from aiogram import Dispatcher
from aiogram.types import Message

from template.tgbot.misc.seconds import work_with_user
from template.tgbot.misc.checks import check_warns

from datetime import timedelta


async def warn_user(message: Message):
    if not message.reply_to_message:
        return await message.reply('This command need to be as reply on message')
    await message.delete()

    user_id = message.reply_to_message.from_user.id
    engine = message.bot.get('engine')
    _ = await work_with_user(user_id, 'warns', engine)
    ban, warns = await check_warns(user_id, engine)
    if ban:
        await message.bot.ban_chat_member(chat_id=message.chat.id, user_id=user_id, until_date=timedelta(seconds=29))
        return await message.reply_to_message.reply('User has been banned because of his three warns')
    return await message.reply_to_message.reply(f'Now user has {warns} warn(s)')


def register_warn(dp: Dispatcher):
    dp.register_message_handler(warn_user, is_admin=True, commands=['warn'], commands_prefix='!/')
