import discord
import bot
import botsecrets
import random
import gp


@bot.tree.command(name='choose', description='randomly choose (comma separated)')
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


@bot.tree.command(name='roll', description='get a random number up to limit')
async def roll(interaction: discord.Interaction, limit: int = 100):
    result = str(random.randint(1, limit))

    user = interaction.user
    embed = discord.Embed()
    embed.set_author(name=f'{user.display_name} used roll {limit}', icon_url=user.display_avatar.url)
    embed.colour = user.colour
    embed.description = f'rolled {result}'

    await interaction.response.send_message(embed=embed)


@bot.tree.command(name='avatar', description='fetch a users avatar')
async def avatar(interaction: discord.Interaction, user: discord.User = None):
    # no user was specified so use command invoker
    if not user:
        user = interaction.user

    embed = discord.Embed()
    embed.set_image(url=user.avatar.url)

    await interaction.response.send_message(f'{user.display_name}\'s avatar: {user.avatar.url}', embed=embed)


@bot.tree.command(name='display_avatar', description='fetch a users display avatar')
async def display_avatar(interaction: discord.Interaction, user: discord.User = None):
    # no user was specified so use command invoker
    if not user:
        user = interaction.user

    embed = discord.Embed()
    embed.set_image(url=user.display_avatar.url)

    await interaction.response.send_message(f'{user.display_name}\'s display avatar: {user.display_avatar.url}',
                                            embed=embed)


@bot.tree.command(name='cheese', description='cheesed to meet u')
async def cheese(interaction: discord.Interaction):
    path = "media/creamery/"
    cheese_names = [
        "actually_additions.png",
        "ad_astra.png",
        "apple.png",
        "emojidex.png",
        "facebook.png",
        "google.png",
        "huawei.png",
        "icons8.png",
        "joypixels.png",
        "leaf_blower_revolution.png",
        "lg.png",
        "microsoft_teams.png",
        "openmoji.png",
        "playstation.png",
        "samsung.png",
        "skype.png",
        "toss_face.png",
        "twitter.png",
        "twitter_sticker.png",
        "whatsapp.png",
        "windows.png",
    ]
    choice_name = random.choice(cheese_names)
    img = discord.File(path + choice_name)

    if choice_name == "skype.png":
        # stinky cheese you lose 100-200 gp
        entry = await gp.check_create(interaction.user.id, interaction.user.name)
        amount = random.randint(100, 200)
        bot.mg_gp.update_one({'user_id': interaction.user.id}, {'$set': {'amount': entry['amount'] - amount}})

        await interaction.response.send_message(f'the cheese is so stinky you lose `{amount}` gp', file=img)
    else:
        await interaction.response.send_message(file=img)


@bot.tree.command(name='gm', description='good morning!')
async def gm(interaction: discord.Interaction):
    vid = discord.File("media/suisei/suisei_gm.mp4")
    await interaction.response.send_message(file=vid)


@bot.tree.command(name='gn', description='good night!')
async def gn(interaction: discord.Interaction):
    vid = discord.File("media/suisei/suisei_gn.mp4")
    await interaction.response.send_message(file=vid)
