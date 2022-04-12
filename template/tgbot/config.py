import os
from dataclasses import dataclass


@dataclass
class TgBot:
    token: str


@dataclass
class Config:
    tg_bot: TgBot


def load_config(path: str = None) -> Config:
    return Config(
        tg_bot=TgBot(
            token=os.getenv('BOT_TOKEN', 'bot_token')
        ),
    )
