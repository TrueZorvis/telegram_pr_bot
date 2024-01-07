import enum

from aiogram.filters.callback_data import CallbackData


class PostCDAction(enum.IntEnum):
    CREATE = 0
    GET = 1
    STATS = 2
    DELETE = 3
    PR = 4


class PostCD(CallbackData, prefix='post'):
    action: PostCDAction
    post_id: int = None
