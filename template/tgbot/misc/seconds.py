from template.tgbot.services.database import get_user, update_user, create_user


async def work_with_user(user_id: str, field_name: str, engine: object) -> int:
    """
    Get seconds for user
    :param user_id: user's specific identifier
    :param field_name: mute, warn or kick
    :return: number of seconds
    """
    seconds: int
    user = get_user(engine, user_id)
    if user:
        update_user(engine, user_id, field_name, getattr(user, field_name) + 1)
        seconds = (getattr(user, field_name) + 1) * 32
    else:
        user = create_user(engine, {'user_id': user_id, field_name: 1})
        seconds = getattr(user, field_name) * 32
    return seconds
