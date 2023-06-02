import discord
import json
import codecs
import random
import botsecrets
from util import get_avatar_from_id
import bot


def open_json():
    with codecs.open('server.json', 'r', 'utf-8') as file:
        return json.load(file)


@bot.tree.command(name='quote', description='post a quote', guild=discord.Object(id=botsecrets.guild_id))
async def quote(interaction, user: discord.User = None):
    data = open_json()

    # user filter is present, filter all quotes down by id
    if user is not None:
        quotes_list = list(filter(lambda d: int(d['author']['id']) == user.id, data['Quotes']))
    # no filter, use all quotes
    else:
        quotes_list = data['Quotes']

    # pick a random quote from available
    random_index = random.randint(0, len(quotes_list)-1)
    # build and format embed
    embeds = await embed_quote(quotes_list[random_index])
    # send message with quote embed
    await interaction.response.send_message(embeds=embeds)


async def embed_quote(q):
    link = 'https://discord.com/channels/' + botsecrets.guild_id + '/' + q['channel_id'] + '/' + q['id']
    img_link = await get_avatar_from_id(int(q['author']['id']))
    embed = discord.Embed(url='https://github.com/Phlana/qbot')
    embed.set_author(name=q['author']['username'], url=link, icon_url=img_link)
    embed.set_footer(text=q['timestamp'])

    if q['content']:
        embed.description = q['content']

    embeds = []
    if len(q['attachments']) > 0:
        for i, a in enumerate(q['attachments']):
            if i == 0:
                img_embed = embed.set_image(url=a['url'])
            else:
                img_embed = discord.Embed(url='https://github.com/Phlana/qbot').set_image(url=a['url'])
            embeds.append(img_embed)
    else:
        embeds.append(embed)

    return embeds


@bot.tree.command(name='add', description='add a quote', guild=discord.Object(id=botsecrets.guild_id))
async def add(interaction, link: str = None):
    if link is None:
        # add the previous message
        message = next(interaction.channel.history(limit=1))
    else:
        message = None
    await add_quote(message)


@bot.tree.context_menu(name='add as quote', guild=discord.Object(id=botsecrets.guild_id))
async def context_add(interaction, message: discord.Message):
    await add_quote(message)
    await interaction.response.send_message("shut up nigga")


async def add_quote(message):
    print(message)


@bot.tree.command(name='convo', description='make a conversation', guild=discord.Object(id=botsecrets.guild_id))
async def convo(interaction, num: discord.app_commands.Range[int, 2, 8] = 4):
    data = open_json()
    # filters out quotes without text contents
    quotes_list = list(filter(lambda d: d['content'], data['Quotes']))

    conversation = '```\n'

    for _ in range(num):
        # pick a random quote from available
        rand_i = random.randint(0, len(quotes_list)-1)
        conversation += '**' + quotes_list[rand_i]['author']['username'] + '**: '
        conversation += quotes_list[rand_i]['content'] + '\n'

    conversation += '```'

    await interaction.response.send_message(conversation)


# @bot.tree.command(name='quotes', description='lists existing quotes', guild=discord.Object(id=botsecrets.guild_id))
# async def quotes(interaction, user: discord.User = None):
#     data = open_json()
#
#     # user filter is present, filter all quotes down by id
#     if user is not None:
#         quotes_list = list(filter(lambda d: int(d['author']['id']) == user.id, data['Quotes']))
#     # no filter, use all quotes
#     else:
#         quotes_list = data['Quotes']
#
#     pass
