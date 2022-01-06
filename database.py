from typing import Optional, Union
import logging

from sqlmodel import Field, SQLModel, Session, create_engine, select
from sqlalchemy import exc


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[str] = Field(default=None, description='User identifier in Telegram')
    warns: Optional[int] = Field(default=0, description='Number of user\'s warnings')
    kicks: Optional[int] = Field(default=0, description='Number of user\'s kicks')
    mutes: Optional[int] = Field(default=0, description='Number of user\'s mutes')


def get_user(engine: create_engine, user_id: str) -> Union[User, None]:
    logging.info('Getting an user')
    with Session(engine) as session:
        try:
            user = session.exec(select(User).where(User.user_id == user_id)).one()
        except exc.NoResultFound:
            logging.warning('User was not founded')
            return None
    logging.info('User was founded')
    return user


def create_user(engine: create_engine, data: dict) -> Union[User, None]:
    logging.info('Creating an user')
    user = User(**data)
    with Session(engine) as session:
        try:
            session.add(user)
            session.commit()
            session.refresh(user)
            logging.info('User was created')
        except exc.CompileError:
            logging.warning('User was not created')
            return None
    return user


def update_user(engine: create_engine, user_id: str, field_name: str, value: int) -> bool:
    logging.info('Updating an user')
    user = get_user(engine, user_id)
    with Session(engine) as session:
        try:
            setattr(user, field_name, value)
            session.add(user)
            session.commit()
            logging.info('User was updating')
        except exc.CompileError:
            logging.warning('User was not updating')
            return False
    return True


def delete_user(engine: create_engine, user_id: str) -> bool:
    logging.info('Deleting an user')
    user = get_user(engine, user_id)
    with Session(engine) as session:
        try:
            session.delete(user)
            session.commit()
            logging.info('User was deleting')
        except exc.CompileError:
            logging.warning('User was not deleting')
            return False
    return True


def create_database(engine: create_engine) -> None:
    SQLModel.metadata.create_all(engine)


def get_engine(path: str) -> create_engine:
    return create_engine(path, echo=False)
