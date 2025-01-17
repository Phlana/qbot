import discord
import bot
import botsecrets
import requests
import random
import mongo
from pymongo import ReturnDocument


@bot.tree.command(
    name='meow',
    description='meow meow meow meow meow meow meow',
    guild=discord.Object(id=botsecrets.guild_id)
)
async def meow(interaction: discord.Interaction):
    mg_cats = mongo.get_cats(interaction.guild.id)

    # preroll for rarity of cat
    roll = random.randint(1, 100)
    image_objs = []
    rarity = ''
    color = None
    if roll <= 40:
        image_objs = get_common()
        rarity = 'common'
        color = '#65655d'
    if 40 < roll <= 70:
        image_objs = get_uncommon()
        rarity = 'uncommon'
        color = '#4a8612'
    if 70 < roll <= 95:
        image_objs = get_rare()
        rarity = 'rare'
        color = '#1c6ea0'
    if 95 < roll:
        image_objs = get_purple()
        rarity = 'purple'
        color = '#ce32fd'

    # imgur objects composition:
    # [{'id': 'xxxxxxx', 'title': None, 'description': None, 'datetime': 1715305311, 'type': 'image/jpeg',
    # 'animated': False, 'width': 3036, 'height': 4048, 'size': 1118694, 'views': 56, 'bandwidth': 62646864,
    # 'vote': None, 'favorite': False, 'nsfw': None, 'section': None, 'account_url': None, 'account_id': None,
    # 'is_ad': False, 'in_most_viral': False, 'has_sound': False, 'tags': [], 'ad_type': 0, 'ad_url': '',
    # 'edited': '0', 'in_gallery': False, 'link': 'https://i.imgur.com/xxxxxxx.jpg'}]

    choice = random.choice(image_objs)

    # update seen counts
    record = mg_cats.find_one({'id': choice['id']})
    if record is None:
        record = {'id': choice['id']}

    if record.get('num_seen') is None:
        record['num_seen'] = 1
    else:
        record['num_seen'] += 1

    if record.get('user_seen') is None:
        record['user_seen'] = []

    # find user id
    found = False
    user_seen = 1
    for user in record['user_seen']:
        if user['id'] == interaction.user.id:
            user['count'] += 1
            found = True
            user_seen = user['count']
            break

    if not found:
        record['user_seen'].append({'id': interaction.user.id, 'count': 1})

    mg_cats.update_one(
        {'id': choice['id']},
        {'$set': record},
        upsert=True
    )

    link = choice['link']
    embed = discord.Embed(url='https://github.com/Phlana/qbot')
    embed.title = f'you got a{"n" if rarity == "uncommon" else ""} {rarity}!'
    if color is not None:
        embed.colour = discord.Color.from_str(color)
    embed.description = f'seen {record["num_seen"]} time{"" if record["num_seen"] == 1 else "s"} total\n' \
                        f'seen {user_seen} time{"" if user_seen == 1 else "s"} by you'
    embed.set_image(url=link)

    await interaction.response.send_message(embed=embed)


def get_common():
    response = requests.request(
        'GET',
        'https://api.imgur.com/3/album/' + botsecrets.commons + '/images',
        headers={'Authorization': 'Client-ID ' + botsecrets.imgur_client_id},
        data={},
        files={}
    )
    return response.json()['data']


def get_uncommon():
    response = requests.request(
        'GET',
        'https://api.imgur.com/3/album/' + botsecrets.uncommons + '/images',
        headers={'Authorization': 'Client-ID ' + botsecrets.imgur_client_id},
        data={},
        files={}
    )
    return response.json()['data']


def get_rare():
    response = requests.request(
        'GET',
        'https://api.imgur.com/3/album/' + botsecrets.rares + '/images',
        headers={'Authorization': 'Client-ID ' + botsecrets.imgur_client_id},
        data={},
        files={}
    )
    return response.json()['data']


def get_purple():
    response = requests.request(
        'GET',
        'https://api.imgur.com/3/album/' + botsecrets.purples + '/images',
        headers={'Authorization': 'Client-ID ' + botsecrets.imgur_client_id},
        data={},
        files={}
    )
    return response.json()['data']


# @bot.tree.command(name='cats', description='shows number of times cat has appeared')
# async def cats(interaction: discord.Interaction):
#     # each imgur link is 25 characters
#     # embeds have a description character limit of 4096
#     # 32 char per link
#     embed = discord.Embed(url='https://github.com/Phlana/qbot')
#     embed.description = ''
#     await interaction.response.send_message(embed=embed)
