import logging
from typing import Union

from sqlalchemy import exc
from sqlmodel import SQLModel, Session, create_engine, select

from template.tgbot.models.models import User


def get_user(engine: create_engine, user_id: str) -> Union[User, None]:
    """
    Function for getting user from database
    :param engine: sqlmodel's engine
    :param user_id: user's specific identifier
    :return: User instance or nothing
    """
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
    """
    Function for creating row in database
    :param engine: sqlmodel's engine
    :param data: dictionary with data that represents user
    :return: Created user instance or nothing
    """
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
    """
    Function for updating row in database
    :param engine: sqlmodel's engine
    :param user_id: user's specific identifier
    :param field_name: field name to update
    :param value: new value
    :return: Result of updating in boolean format
    """
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
    """
    Function for deleting row in database
    :param engine: sqlmodel's engine
    :param user_id: user's specific identifier
    :return: Result of deleting in boolean format
    """
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
    """
    Create database with the SQLModel
    :param engine: sqlmodel's engine
    :return: nothing to return
    """
    SQLModel.metadata.create_all(engine)


def get_engine(path: str) -> create_engine:
    """
    Function for connecting to the database-file
    :param path: path to the file
    :return: sqlmodel's engine
    """
    return create_engine(path, echo=False)
