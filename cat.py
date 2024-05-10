import discord
import bot
import botsecrets
import requests
import random


@bot.tree.command(
    name='meow',
    description='meow meow meow meow meow meow meow',
    guild=discord.Object(id=botsecrets.guild_id)
)
async def meow(interaction: discord.Interaction):
    response = requests.request(
        'GET',
        'https://api.imgur.com/3/album/' + botsecrets.imgur_cat_album_hash + '/images',
        headers={'Authorization': 'Client-ID ' + botsecrets.imgur_client_id},
        data={},
        files={}
    )

    image_objs = response.json()['data']
    choice = random.choice(image_objs)

    await interaction.response.send_message(choice['link'])
