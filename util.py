import bot


async def get_avatar_from_id(user_id):
    user = await bot.client.fetch_user(user_id)
    return user.avatar
