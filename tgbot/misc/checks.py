from tgbot.services.database import get_user

from typing import Tuple


async def check_warns(user_id: str, engine: object) -> Tuple[bool, int]:
    """
    If user has 3 warns, it will be as ban
    :param user_id: user's specific identifier
    :return: is it a ban and number of warns
    """
    user = get_user(engine, user_id)
    warns = user.warns
    if warns == 3:
        return True, 0
    return False, user.warns
