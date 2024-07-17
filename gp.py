import discord
import botsecrets
import util
import bot
from datetime import datetime, timezone, timedelta

"""
mongo db
database    Vewem
collection  gp
{
    _id: randomly generated mongo id
    user_id: discord user id
    username: discord username
    amount: amount of gp
    daily: timestamp of last claimed
}
"""


# checks for entry in database, else creates one
async def check_create(user_id: int, username: str):
    entry = bot.mg_gp.find_one({'user_id': user_id})
    if entry is None:
        # new user, create new user
        bot.mg_gp.insert_one({'user_id': user_id, 'username': username, 'amount': 0, 'daily': None})
        entry = bot.mg_gp.find_one({'user_id': user_id})

    return entry


@bot.tree.command(name='gp', description='show your gp', guild=discord.Object(id=botsecrets.guild_id))
async def gp(interaction: discord.Interaction, user: discord.User = None):
    if user is None:
        user = interaction.user

    money = (await check_create(user.id, user.name)).get('amount')

    if money == 0:
        await interaction.response.send_message('bitch u broke')
    else:
        await interaction.response.send_message(f'you have `{money}` gp')


@bot.tree.command(name='daily', description='claim daily gp', guild=discord.Object(id=botsecrets.guild_id))
async def daily(interaction: discord.Interaction):
    now = datetime.now(timezone.utc).replace(tzinfo=None, microsecond=0)
    reset = util.get_daily_reset()
    entry = await check_create(interaction.user.id, interaction.user.name)

    if entry['daily'] is not None and entry['daily'] > reset:
        next_reset = reset + timedelta(days=1)
        await interaction.response.send_message(f'available {util.get_rel_timestamp(next_reset)}')
        return

    money = entry['amount'] + 1000
    bot.mg_gp.update_one({'user_id': interaction.user.id}, {'$set': {'amount': money, 'daily': now}})

    await interaction.response.send_message(f'claimed `1000` gp! your new balance is `{money}`')


@bot.tree.command(name='ranking', description='whos got da money 🤑', guild=discord.Object(id=botsecrets.guild_id))
async def ranking(interaction: discord.Interaction):
    embed = discord.Embed(url='https://github.com/Phlana/qbot')
    embed.description = ''

    entries = bot.mg_gp.find().sort('amount', -1)
    rank = 0
    for entry in entries:
        rank += 1
        embed.description += f'{rank} - {entry["username"]}: `{entry["amount"]}`\n'

    await interaction.response.send_message(embed=embed)
