from typing import Optional

from sqlmodel import Field, SQLModel, Session, create_engine, select
from sqlalchemy import exc


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[str] = Field(default=None, description='User identifier in Telegram')
    warns: Optional[int] = Field(default=0, description='Number of user\'s warnings')
    bans: Optional[int] = Field(default=0, description='Number of user\'s bangs')
    kicks: Optional[int] = Field(default=0, description='Number of user\'s kicks')
    mutes: Optional[int] = Field(default=0, description='Number of user\'s mutes')


def get_user(engine: create_engine, user_id: str) -> Optional[User, None]:
    with Session(engine) as session:
        try:
            user = session.exec(select(User).where(User.user_id == user_id)).one()
        except exc.NoResultFound:
            return None
    return user


def create_user(engine: create_engine, data: dict):
    user = User(**data)
    with Session(engine) as session:
        session.add(user)
        session.commit()


def update_user(engine: create_engine, user_id: str, data: dict) -> bool:
    user = get_user(engine, user_id)
    with Session(engine) as session:
        try:
            user = User(**data)
            session.add(user)
            session.commit()
        except exc.CompileError:
            return False
    return True


def delete_user(engine: create_engine, user_id: str) -> bool:
    user = get_user(engine, user_id)
    with Session(engine) as session:
        try:
            session.delete(user)
            session.commit()
        except exc.CompileError:
            return False
    return True


def create_database(engine: create_engine) -> None:
    SQLModel.metadata.create_all(engine)


def get_engine(path: str) -> create_engine:
    return create_engine(path, echo=True)
