# This example requires the 'message_content' intent.

import secrets
import discord
from discord import app_commands
import json
import random
import codecs


intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=secrets.guild_id))
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower().find('im ') >= 0:
        content = message.content.lower()
        index = content.find('im ')
        msg = ""
        if index != 0:
            if content[index - 1] == ' ':
                msg = 'hi ' + content[index + 3:]
        else:
            msg = 'hi ' + content[index + 3:]

        if msg != "":
            await message.channel.send(msg)


@tree.command(name='quote', description='post a random quote', guild=discord.Object(id=secrets.guild_id))
async def quote(interaction):
    with codecs.open('server.json', 'r', 'utf-8') as file:
        data = json.load(file)

    quotes = data['Quotes']
    num_quotes = len(quotes)
    random_index = random.randint(0, num_quotes-1)

    q = quotes[random_index]
    embed = await format_quote(q)

    await interaction.response.send_message(embed=embed)


async def format_quote(q):
    author = q['author']
    link = 'https://discord.com/channels/' + secrets.guild_id + '/' + q['channel_id'] + '/' + q['id']
    img_link = await get_avatar_from_id(int(author['id']))
    embed = discord.Embed()
    embed.set_author(name=author['username'], url=link, icon_url=img_link)
    # embed.timestamp = q['timestamp']

    content = q['content']
    if content == "":
        embed.description = 'image quote (wip)'
    else:
        embed.description = q['content']

    print(embed.description)
    return embed


async def get_avatar_from_id(user_id):
    user = await client.fetch_user(user_id)
    return user.avatar


@tree.command(name='convo', description='make a conversation', guild=discord.Object(id=secrets.guild_id))
async def convo(interaction):
    await interaction.response.send_message("wip")
    pass

client.run(secrets.token)
