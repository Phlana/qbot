import discord
import botsecrets
import util
import bot
import mongo
from datetime import datetime, timezone, timedelta
# import asyncio

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
async def check_create(database, user_id: int, username: str):
    entry = database.find_one({'user_id': user_id})
    if entry is None:
        # new user, create new user
        database.insert_one({'user_id': user_id, 'username': username, 'amount': 0, 'daily': None})
        entry = database.find_one({'user_id': user_id})

    return entry


@bot.tree.command(name='gp', description='show your gp', guild=discord.Object(id=botsecrets.guild_id))
async def gp(interaction: discord.Interaction, user: discord.User = None):
    mg_gp = mongo.get_gp(interaction.guild.id)

    if user is None:
        user = interaction.user

    money = (await check_create(mg_gp, user.id, user.name)).get('amount')

    if money == 0:
        await interaction.response.send_message('bitch u broke')
    else:
        await interaction.response.send_message(f'you have `{money}` gp')


@bot.tree.command(name='daily', description='claim daily gp', guild=discord.Object(id=botsecrets.guild_id))
async def daily(interaction: discord.Interaction):
    mg_gp = mongo.get_gp(interaction.guild.id)

    now = datetime.now(timezone.utc).replace(tzinfo=None, microsecond=0)
    reset = util.get_daily_reset()
    entry = await check_create(mg_gp, interaction.user.id, interaction.user.name)

    if entry['daily'] is not None and entry['daily'] > reset:
        next_reset = reset + timedelta(days=1)
        await interaction.response.send_message(f'available {util.get_rel_timestamp(next_reset)}')
        return

    money = entry['amount'] + 1000
    mg_gp.update_one({'user_id': interaction.user.id}, {'$set': {'amount': money, 'daily': now}})

    await interaction.response.send_message(f'claimed `1000` gp! your new balance is `{money}`')


@bot.tree.command(name='ranking', description='whos got da money 🤑', guild=discord.Object(id=botsecrets.guild_id))
async def ranking(interaction: discord.Interaction):
    mg_gp = mongo.get_gp(interaction.guild.id)

    embed = discord.Embed(url='https://github.com/Phlana/qbot')
    embed.title = 'top 10 money havers'
    embed.description = ''

    entries = mg_gp.find().sort('amount', -1)
    rank = 0
    for entry in entries:
        rank += 1
        embed.description += f'{rank} - {entry["username"]}: `{entry["amount"]}`\n'
        if rank == 10:
            break

    await interaction.response.send_message(embed=embed)


# class voteView(discord.ui.View):
#     def __init__(self):
#         super().__init__(timeout=5)
#
#         self.yes_button = discord.ui.Button(style=discord.ButtonStyle.primary, emoji=util.thumbs_up)
#         self.yes_button.callback = self.yes_callback
#         self.add_item(self.yes_button)
#
#         self.no_button = discord.ui.Button(style=discord.ButtonStyle.primary, emoji=util.middle_finger)
#         self.no_button.callback = self.no_callback
#         self.add_item(self.no_button)
#
#         self.yes = 0
#         self.no = 0
#         self.seen = []
#
#     async def yes_callback(self, interaction: discord.Interaction):
#         if interaction.user.id in self.seen:
#             return
#
#         self.seen.append(interaction.user.id)
#         self.yes += 1
#         await interaction.response.send_message("yes")
#
#     async def no_callback(self, interaction: discord.Interaction):
#         if interaction.user.id in self.seen:
#             return
#
#         self.seen.append(interaction.user.id)
#         self.no += 1
#         await interaction.response.edit_message("no")
#
#     @discord.ui.button(label='stop', style=discord.ButtonStyle.danger)
#     async def stop_callback(self, interaction: discord.Interaction, button: discord.Button):
#         self.clear_items()
#         self.stop()
#
#     async def on_timeout(self):
#         print('timed out')
#         self.clear_items()
#         self.stop()
#
#
# @bot.tree.command(name='idiot', description='this guys a fucking idiot!!', guild=discord.Object(id=botsecrets.guild_id))
# async def idiot(interaction: discord.Interaction, user: discord.User):
#     view = voteView()
#
#     embed = discord.Embed()
#     embed.set_thumbnail(url=user.display_avatar.url)
#     embed.description = f'is <@{user.id}> an idiot?\n\n'
#
#     await interaction.response.send_message(embed=embed, view=view)
#
#     # message: discord.Message = await interaction.original_response()
#     # print(message)
#     # await message.add_reaction(util.thumbs_up)
#     # await message.add_reaction(util.middle_finger)
#     #
#     # await asyncio.sleep(5)
#     #
#     # # get and tally up reactions
#     # message2 = await interaction.original_response()
#     # print(message2)
#     # reactions = message2.reactions
#     # print(reactions)
#     # for reaction in reactions:
#     #     print(reaction)
#     #     print(reaction.emoji)
#     #     print(reaction.count)
