import functools
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.utils.executor import start_webhook, start_polling

from loader import dp
from tgbot.services.database import get_engine, create_database
from tgbot.config import load_config
from tgbot.services.setting_commands import set_default_commands
from tgbot.filters.admin import IsAdminFilter

logger = logging.getLogger(__name__)


def register_all_middlewares(dispatcher: Dispatcher):
    logger.info('Registering middlewares')


def register_all_filters(dispatcher: Dispatcher) -> None:
    logger.info('Registering filters')
    dispatcher.filters_factory.bind(IsAdminFilter)


def register_all_handlers(dispatcher: Dispatcher):
    from tgbot import handlers
    logger.info('Registering handlers')


async def set_all_default_commands(bot: Bot):
    await set_default_commands(bot)
    logger.info('Registering commands')


def create_db(bot: Bot):
    sqlite_file_name = 'database.db'
    sqlite_url = f'sqlite:///{sqlite_file_name}'
    engine = get_engine(sqlite_url)
    create_database(engine)
    bot['engine'] = engine
    logger.info('Database was created')


async def on_startup(dispatcher: Dispatcher, webhook_url: str = None):
    register_all_middlewares(dispatcher)
    register_all_filters(dispatcher)
    register_all_handlers(dispatcher)
    create_db(dispatcher.bot)
    await set_all_default_commands(dispatcher.bot)

    # Get current webhook status
    webhook = await dispatcher.bot.get_webhook_info()

    if webhook_url:
        await dispatcher.bot.set_webhook(webhook_url)
        logger.info('Webhook was set')
    elif webhook.url:
        await dispatcher.bot.delete_webhook()
        logger.info('Webhook was deleted')
    logger.info('Bot started')


async def on_shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()
    logger.info('Bot shutdown')


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")

    config = load_config()

    # Webhook settings
    HEROKU_APP_NAME = os.getenv('HEROKU_APP_NAME')
    WEBHOOK_HOST = f'https://{HEROKU_APP_NAME}.herokuapp.com'
    WEBHOOK_PATH = f'/webhook/{config.tg_bot.token}'
    WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'
    # Webserver settings
    WEBAPP_HOST = '0.0.0.0'
    WEBAPP_PORT = int(os.getenv('PORT', 5000))

    # start_polling(
    #     dispatcher=dp,
    #     on_startup=on_startup,
    #     on_shutdown=on_shutdown,
    #     skip_updates=True,
    # )

    start_webhook(
        dispatcher=dp,
        on_startup=functools.partial(on_startup, webhook_url=WEBHOOK_URL),
        on_shutdown=on_shutdown,
        webhook_path=WEBHOOK_PATH,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT
    )
