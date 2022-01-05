import config
import logging
from datetime import timedelta

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

from filters import IsAdminFilter
from database import create_database, get_engine, get_user, update_user, create_user, User


class BanState(StatesGroup):
    """
    State class that represents ban process
    """
    Time = State()
    AdminID = State()


# log level
logging.basicConfig(level=logging.INFO)

# bot init
bot = Bot(token=config.TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# activate filters
dp.filters_factory.bind(IsAdminFilter)

# SQLModel engine
engine: object


async def work_with_user(user_id: str, field_name: str) -> int:
    seconds: int
    user = get_user(engine, user_id)
    if user:
        update_user(engine, user_id, field_name, getattr(user, field_name) + 1)
        seconds = (getattr(user, field_name) + 1) * 32
    else:
        user = create_user(engine, {'user_id': user_id, field_name: 1})
        seconds = getattr(user, field_name) * 32
    return seconds


@dp.message_handler(is_admin=True, commands=['ban'], commands_prefix='!/', state='*')
async def prepare_ban(message: types.Message, state: FSMContext):
    if not message.reply_to_message:
        await message.reply('This command need to be as reply on message')
        return
    # await message.bot.delete_message(config.GROUP_ID, message.message_id)
    # await message.bot.kick_chat_member(chat_id=config.GROUP_ID, user_id=message.reply_to_message.from_user.id)

    # await message.reply_to_message.reply('User has been banned')
    await state.update_data({'AdminID': message.from_user.id})
    await BanState.Time.set()
    await message.reply_to_message.reply('Write the time in days to ban this user.')


@dp.message_handler(state=BanState.Time)
async def finish_ban(message: types.Message, state: FSMContext) -> types.Message:
    text = message.text
    if text.isdigit():
        text = int(text)
    else:
        return await message.answer('It should be an integer')
    data = await state.get_data()
    if message.from_user.id == data['AdminID']:
        # ban user
        await state.finish()
        return await message.answer('User has been banned')
    return await message.answer('It needs to be the administrator')


@dp.message_handler(is_admin=True, commands=['kick'], commands_prefix='!/')
async def kick_user(message: types.Message):
    if not message.reply_to_message:
        return await message.reply('This command need to be as reply on message')
    await bot.delete_message(message.chat.id, message.message_id)

    user_id = message.reply_to_message.from_user.id
    seconds = await work_with_user(user_id, 'kicks')

    await bot.kick_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id,
                               until_date=timedelta(seconds=seconds))
    return await message.reply_to_message.reply(f'User has been kicked for the {seconds} seconds')


@dp.message_handler(is_admin=True, commands=['mute'], commands_prefix='!/')
async def mute_user(message: types.Message):
    if not message.reply_to_message:
        return await message.reply('This command need to be as reply on message')
    await bot.delete_message(message.chat.id, message.message_id)

    user_id = message.reply_to_message.from_user.id
    seconds = await work_with_user(user_id, 'mutes')

    await bot.restrict_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id,
                                   until_date=timedelta(seconds=seconds),
                                   permissions=types.chat_permissions.ChatPermissions(can_send_messages=False,
                                                                                      can_send_polls=False,
                                                                                      can_send_other_messages=False,
                                                                                      can_send_media_messages=False))
    return await message.reply_to_message.reply(f'User has been muted for the {seconds} seconds')


@dp.message_handler(commands=['dice'])
async def role_dice(message: types.Message) -> types.Message:
    """
    This handler will be called when user sends `/dice` command
    """
    return await message.answer_dice()


@dp.message_handler(content_types=['new_chat_members'])
async def on_user_joined(message: types.Message):
    await message.delete()


@dp.message_handler()
async def filter_messages(message: types.Message):
    if 'bad word' in message.text:
        await message.delete()


if __name__ == '__main__':
    sqlite_file_name = 'database.db'
    sqlite_url = f'sqlite:///{sqlite_file_name}'
    engine = get_engine(sqlite_url)
    create_database(engine)
    executor.start_polling(dp, skip_updates=True)
