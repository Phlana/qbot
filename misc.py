import discord
import bot
import botsecrets
import random


@bot.tree.command(name='choose', description='randomly choose (comma separated)',
                  guild=discord.Object(id=botsecrets.guild_id))
async def choose(interaction: discord.Interaction, choices_str: str):
    choices = [c.strip() for c in choices_str.split(',')]
    result = random.choice(choices)
    choices_str = ', '.join(choices)

    user = interaction.user
    embed = discord.Embed()
    embed.set_author(name=f'{user.display_name} used choose {choices_str}', icon_url=user.display_avatar.url)
    embed.colour = user.colour
    embed.description = f'chose {result}'

    await interaction.response.send_message(embed=embed)


@bot.tree.command(name='roll', description='get a random number up to limit',
                  guild=discord.Object(id=botsecrets.guild_id))
async def roll(interaction: discord.Interaction, limit: int = 100):
    result = str(random.randint(1, limit))

    user = interaction.user
    embed = discord.Embed()
    embed.set_author(name=f'{user.display_name} used roll {limit}', icon_url=user.display_avatar.url)
    embed.colour = user.colour
    embed.description = f'rolled {result}'

    await interaction.response.send_message(embed=embed)


@bot.tree.command(name='avatar', description='fetch a users avatar', guild=discord.Object(id=botsecrets.guild_id))
async def avatar(interaction: discord.Interaction, user: discord.User = None):
    # no user was specified so use command invoker
    if not user:
        user = interaction.user

    embed = discord.Embed()
    embed.set_image(url=user.avatar.url)

    await interaction.response.send_message(f'{user.display_name}\'s avatar: {user.avatar.url}', embed=embed)


@bot.tree.command(name='display_avatar', description='fetch a users display avatar',
                  guild=discord.Object(id=botsecrets.guild_id))
async def display_avatar(interaction: discord.Interaction, user: discord.User = None):
    # no user was specified so use command invoker
    if not user:
        user = interaction.user

    embed = discord.Embed()
    embed.set_image(url=user.display_avatar.url)

    await interaction.response.send_message(f'{user.display_name}\'s display avatar: {user.display_avatar.url}',
                                            embed=embed)


@bot.tree.command(name='cheese')
async def cheese(interaction: discord.Interaction):
    embed = discord.Embed()
    embed.set_image(url='https://em-content.zobj.net/thumbs/120/twitter/322/cheese-wedge_1f9c0.png')

    await interaction.response.send_message(embed=embed)
