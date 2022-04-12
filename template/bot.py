import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from tgbot.services.database import get_engine, create_database
from tgbot.config import load_config
from tgbot.filters.admin import IsAdminFilter
from tgbot.handlers.admins import register_admins
from tgbot.handlers.help import register_help
from tgbot.handlers.start import register_start
from tgbot.handlers.dice import register_dice
from tgbot.handlers.mute import register_mute
from tgbot.handlers.warn import register_warn
from tgbot.handlers.kick import register_kick
from tgbot.handlers.ban import register_ban

logger = logging.getLogger(__name__)


def register_all_middlewares(dp):
    pass


def register_all_filters(dp):
    dp.filters_factory.bind(IsAdminFilter)


def register_all_handlers(dp):
    register_start(dp)
    register_mute(dp)
    register_ban(dp)
    register_kick(dp)
    register_warn(dp)
    register_help(dp)
    register_dice(dp)
    register_admins(dp)


def create_db(bot: Bot):
    sqlite_file_name = 'database.db'
    sqlite_url = f'sqlite:///{sqlite_file_name}'
    engine = get_engine(sqlite_url)
    create_database(engine)
    bot['engine'] = engine


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

    create_db(bot)

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
