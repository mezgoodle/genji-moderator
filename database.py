from typing import Optional

from sqlmodel import Field, SQLModel, create_engine, Session


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[str] = Field(default=None, description='User identifier in Telegram')
    warns: Optional[int] = Field(default=0, description='Number of user\'s warnings')
    bans: Optional[int] = Field(default=0, description='Number of user\'s bangs')
    kicks: Optional[int] = Field(default=0, description='Number of user\'s kicks')
    mutes: Optional[int] = Field(default=0, description='Number of user\'s mutes')


def get_user():
    pass


def create_user(engine: create_engine, data: dict):
    user = User(**data)
    with Session(engine) as session:
        session.add(user)
        session.commit()


def update_user():
    pass


def delete_user():
    pass


def create_database(engine: create_engine) -> None:
    SQLModel.metadata.create_all(engine)


def get_engine(path: str) -> create_engine:
    return create_engine(path, echo=True)
