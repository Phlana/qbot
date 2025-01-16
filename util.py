import bot
from datetime import datetime, timezone, timedelta


thumbs_up = '\N{THUMBS UP SIGN}'
middle_finger = '🖕'


async def get_avatar_from_id(user_id):
    user = await bot.client.fetch_user(user_id)
    return user.avatar


async def get_colour_from_id(user_id):
    user = await bot.client.fetch_user(user_id)
    return user.colour


def get_daily_reset():
    now_utc = datetime.now(timezone.utc)
    reset_utc = now_utc - timedelta(days=1)
    return reset_utc.replace(tzinfo=None, hour=18, minute=0, second=0, microsecond=0)


def get_rel_timestamp(dt: datetime) -> str:
    return f'<t:{int(dt.timestamp())}:R>'
