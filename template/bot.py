import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from tgbot.services.database import get_engine, create_database
from tgbot.config import load_config
from tgbot.filters.admin import AdminFilter
from tgbot.handlers.admin import register_admin
from tgbot.handlers.echo import register_echo
from tgbot.handlers.help import register_help
from tgbot.handlers.start import register_start

logger = logging.getLogger(__name__)


def register_all_middlewares(dp):
    pass


def register_all_filters(dp):
    pass
    # dp.filters_factory.bind(AdminFilter)


def register_all_handlers(dp):
    register_start(dp)
    register_help(dp)
    register_admin(dp)
    register_echo(dp)


def create_db():
    sqlite_file_name = 'database.db'
    sqlite_url = f'sqlite:///{sqlite_file_name}'
    engine = get_engine(sqlite_url)
    create_database(engine)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")
    config = load_config(".env")

    storage = MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(bot, storage=storage)

    bot['config'] = config

    register_all_middlewares(dp)
    register_all_filters(dp)
    register_all_handlers(dp)

    create_db()

    # start
    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
