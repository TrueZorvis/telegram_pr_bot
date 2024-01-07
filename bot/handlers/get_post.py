from aiogram import types
from sqlalchemy.orm import sessionmaker

from bot.db import Post
from bot.db.post import get_post
from bot.structures.callback_data_factories import PostCD
from bot.structures.keyboards.posts_board import POSTS_EDIT_BOARD


async def menu_posts_get(call: types.CallbackQuery, callback_data: PostCD, session_maker: sessionmaker) -> None:
    post: Post = await get_post(post_id=callback_data.post_id, session_maker=session_maker)
    await call.message.edit_text(
        "<b>Пост</b>\n\n{text}\n\n<s>---</s>\n\n{stats}".format(text=post.text, stats=post.stats),
        reply_markup=POSTS_EDIT_BOARD
    )
