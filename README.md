<h1 id="project-title" align="center">
  genji-moderator <img alt="logo" width="40" height="40" src="https://raw.githubusercontent.com/mezgoodle/images/master/MezidiaLogoTransparent.png" /><br>
  <img alt="language" src="https://img.shields.io/badge/language-python-brightgreen?style=flat-square" />
  <img alt="Github issues" src="https://img.shields.io/github/issues/mezgoodle/genji-moderator?style=flat-square" />
  <img alt="GitHub closed issues" src="https://img.shields.io/github/issues-closed/mezgoodle/genji-moderator?style=flat-square" />
  <img alt="GitHub pull requests" src="https://img.shields.io/github/issues-pr/mezgoodle/genji-moderator?style=flat-square" />
  <img alt="GitHub closed pull requests" src="https://img.shields.io/github/issues-pr-closed/mezgoodle/genji-moderator?style=flat-square" />
  <img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/mezgoodle/genji-moderator?style=flat-square">
</h1>

<p align="center">
    🌟Hello everyone! This is the repository of Telegram bot on Python "genji-moderator".🌟
</p>

![Mezidia logo](https://raw.githubusercontent.com/mezgoodle/images/master/genji.jpg)

## Motivation :exclamation:

It was my  old idea to build a bot-moderator in Telegram. One time I saw 
[this](https://www.youtube.com/watch?v=I8K3iYcxPl0) video and started to code. So now you can see the result.

## Build status :hammer:

Here you can see build status of [continuous integration](https://en.wikipedia.org/wiki/Continuous_integration):

[![Python application](https://github.com/mezgoodle/genji-moderator/actions/workflows/python-app.yml/badge.svg)](https://github.com/mezgoodle/genji-moderator/actions/workflows/python-app.yml)

## Badges :mega:

Other badges

[![Theme](https://img.shields.io/badge/Theme-Bot-brightgreen?style=flat-square)](https://core.telegram.org/bots)
[![Platform](https://img.shields.io/badge/Platform-Telegram-brightgreen?style=flat-square)](https://core.telegram.org/)
 
## Screenshots :camera:

Include logo/demo screenshot etc.

## Tech/framework used :wrench:

**Built with**

- [aiogram](https://github.com/aiogram/aiogram)
- [sqlmodel](https://sqlmodel.tiangolo.com/)

## Features :muscle:

With my bot you can **mute**, **kick** or **ban** users in your _Telegram chats_. Also you can **warn** members of chat.

## Code Example :pushpin:

- SQLModel's model:

```python
from typing import Optional

from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    """
    Model that represents User in database
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[str] = Field(default=None, description='User identifier in Telegram')
    warns: Optional[int] = Field(default=0, description='Number of user\'s warnings')
    kicks: Optional[int] = Field(default=0, description='Number of user\'s kicks')
    mutes: Optional[int] = Field(default=0, description='Number of user\'s mutes')
```

- aiogram's filter:

```python
from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


class IsAdminFilter(BoundFilter):
    key = 'is_admin'

    def __init__(self, is_admin):
        self.is_admin = is_admin

    async def check(self, message: types.Message):
        member = await message.bot.get_chat_member(message.chat.id, message.from_user.id)
        return member.is_chat_admin()
```

## Installation :computer:

1. Clone this repository:

```bash
git clone https://github.com/mezgoodle/genji-moderator.git
```

2. Install packages:

```bash
pip install -r requirements.txt
```

## Fast usage :dash:

1. Change in `config.py` variable value to your _Telegram token_:

```python
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN', 'change_here')
```

2. Change the way to start the bot:

> change webhook to long_polling

```python
from aiogram import  executor

...

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
```

## Contribute :running:

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. 
Also look at the [CONTRIBUTING.md](https://github.com/mezgoodle/genji-moderator/blob/master/CONTRIBUTING.md).

## License :bookmark:

MIT © [mezgoodle](https://github.com/mezgoodle)
