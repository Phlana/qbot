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

    # todo: preroll for rarity of cat
    image_objs = get_common()
    # imgur objects:
    # [{'id': 'xxxxxxx', 'title': None, 'description': None, 'datetime': 1715305311, 'type': 'image/jpeg',
    # 'animated': False, 'width': 3036, 'height': 4048, 'size': 1118694, 'views': 56, 'bandwidth': 62646864,
    # 'vote': None, 'favorite': False, 'nsfw': None, 'section': None, 'account_url': None, 'account_id': None,
    # 'is_ad': False, 'in_most_viral': False, 'has_sound': False, 'tags': [], 'ad_type': 0, 'ad_url': '',
    # 'edited': '0', 'in_gallery': False, 'link': 'https://i.imgur.com/xxxxxxx.jpg'}]

    choice = random.choice(image_objs)

    # update cat count
    result = mg_cats.find_one_and_update(
        {'id': choice['id']},
        {
            '$setOnInsert': {'id': choice['id']},
            '$inc': {'num_seen': 1},
        },
        upsert=True,
        return_document=ReturnDocument.AFTER
    )
    link = choice['link']
    embed = discord.Embed(url='https://github.com/Phlana/qbot')
    embed.title = f'seen {result["num_seen"]} time{"" if result["num_seen"] == 1 else "s"}'
    embed.set_image(url=link)

    await interaction.response.send_message(embed=embed)


def get_common():
    response = requests.request(
        'GET',
        'https://api.imgur.com/3/album/' + botsecrets.imgur_cat_album_hash + '/images',
        headers={'Authorization': 'Client-ID ' + botsecrets.imgur_client_id},
        data={},
        files={}
    )
    return response.json()['data']


# todo: change hash for new album
def get_rare():
    response = requests.request(
        'GET',
        'https://api.imgur.com/3/album/' + botsecrets.imgur_cat_album_hash + '/images',
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
