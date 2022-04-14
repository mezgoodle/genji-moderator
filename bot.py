import logging
import os

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from tgbot.services.database import get_engine, create_database
from tgbot.config import load_config
from tgbot.services.setting_commands import set_default_commands
from tgbot.filters.admin import IsAdminFilter
from tgbot.handlers.admins import register_admins
from tgbot.handlers.help import register_help
from tgbot.handlers.start import register_start
from tgbot.handlers.dice import register_dice
from tgbot.handlers.mute import register_mute
from tgbot.handlers.warn import register_warn
from tgbot.handlers.kick import register_kick
from tgbot.handlers.ban import register_ban
from tgbot.handlers.new_chat_members import register_join

logger = logging.getLogger(__name__)
config = load_config()
storage = MemoryStorage()
bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
dp = Dispatcher(bot, storage=storage)
bot['config'] = config
# TODO: set up filters for chat type - group only


def register_all_middlewares(dp):
    pass


def register_all_filters():
    dp.filters_factory.bind(IsAdminFilter)


def register_all_handlers():
    register_start(dp)
    register_mute(dp)
    register_ban(dp)
    register_kick(dp)
    register_warn(dp)
    register_help(dp)
    register_dice(dp)
    register_admins(dp)
    register_join(dp)


async def set_all_default_commands():
    await set_default_commands(bot)


def create_db():
    sqlite_file_name = 'database.db'
    sqlite_url = f'sqlite:///{sqlite_file_name}'
    engine = get_engine(sqlite_url)
    create_database(engine)
    bot['engine'] = engine


# Webhook settings
HEROKU_APP_NAME = os.getenv('HEROKU_APP_NAME')
WEBHOOK_HOST = f'https://{HEROKU_APP_NAME}.herokuapp.com'
WEBHOOK_PATH = f'/webhook/{config.tg_bot.token}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

# Webserver settings
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = int(os.getenv('PORT', 5000))


# Functions for webhooks
async def on_startup(dp: Dispatcher):
    await set_all_default_commands()
    await bot.set_webhook(WEBHOOK_URL)


async def on_shutdown(dp: Dispatcher):
    await dp.storage.close()
    await dp.storage.wait_closed()
    logging.warning('Shutting down..')
    logging.warning('Bye!')


# async def main():
#     logging.basicConfig(
#         level=logging.INFO,
#         format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
#     )
#     logger.info("Starting bot")
#     config = load_config()
#
#     storage = MemoryStorage()
#     bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
#     dp = Dispatcher(bot, storage=storage)
#
#     bot['config'] = config
#
#     register_all_middlewares(dp)
#     register_all_filters(dp)
#     register_all_handlers(dp)
#
#     create_db(bot)
#
#     await set_all_default_commands(bot)
#
#     # Webhook settings
#     HEROKU_APP_NAME = os.getenv('HEROKU_APP_NAME')
#     WEBHOOK_HOST = f'https://{HEROKU_APP_NAME}.herokuapp.com'
#     WEBHOOK_PATH = f'/webhook/{config.tg_bot.token}'
#     WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'
#
#     # Webserver settings
#     WEBAPP_HOST = '0.0.0.0'
#     WEBAPP_PORT = int(os.getenv('PORT', 5000))
#
#     # start
#     try:
#         start_webhook(
#             dispatcher=dp,
#             webhook_path=WEBHOOK_PATH,
#             on_shutdown=on_shutdown,
#             on_startup=on_startup(bot, WEBHOOK_URL),
#             skip_updates=True,
#             host=WEBAPP_HOST,
#             port=WEBAPP_PORT
#         )
#     finally:
#         await dp.storage.close()
#         await dp.storage.wait_closed()


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")

    register_all_middlewares(dp)
    register_all_filters()
    register_all_handlers()

    create_db()

    executor.start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_shutdown=on_shutdown,
        on_startup=on_startup,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT
    )
