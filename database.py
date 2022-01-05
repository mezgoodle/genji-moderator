from typing import Optional

from sqlmodel import Field, SQLModel, create_engine


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[str] = Field(default=None, description='User identifier in Telegram')
    warns: Optional[int] = Field(default=0, description='Number of user\'s warnings')
    bans: Optional[int] = Field(default=0, description='Number of user\'s bangs')
    kicks: Optional[int] = Field(default=0, description='Number of user\'s kicks')
    mutes: Optional[int] = Field(default=0, description='Number of user\'s mutes')


def create_database(engine: create_engine):
    SQLModel.metadata.create_all(engine)
