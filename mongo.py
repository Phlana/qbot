import bot


def connect(guild_id: int):
    return bot.mg_client[str(guild_id)]


def get_quotes(guild_id: int):
    mg_db = connect(guild_id)
    return mg_db['quotes']


def get_cats(guild_id: int):
    mg_db = connect(guild_id)
    return mg_db['cats']


def get_gp(guild_id: int):
    mg_db = connect(guild_id)
    return mg_db['gp']


def get_fake(guild_id: int):
    mg_db = connect(guild_id)
    return mg_db['nonexist']
