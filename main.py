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
        lower_content = message.content.lower()
        index = lower_content.find('im ')
        if index != 0:
            if lower_content[index - 1] == ' ':
                await message.channel.send('hi ' + message.content[index + 3:])
        else:
            await message.channel.send('hi ' + message.content[index + 3:])


@tree.command(name='quote', description='post a quote', guild=discord.Object(id=secrets.guild_id))
async def quote(interaction, user: discord.User = None):
    with codecs.open('server.json', 'r', 'utf-8') as file:
        data = json.load(file)

    # user filter is present, filter all quotes down by id
    if user is not None:
        quotes = list(filter(lambda d: int(d['author']['id']) == user.id, data['Quotes']))
    # no filter, use all quotes
    else:
        quotes = data['Quotes']

    # pick a random quote from available
    random_index = random.randint(0, len(quotes)-1)
    # build and format embed
    embeds = await embed_quote(quotes[random_index])
    # send message with quote embed
    await interaction.response.send_message(embeds=embeds)


async def embed_quote(q):
    link = 'https://discord.com/channels/' + secrets.guild_id + '/' + q['channel_id'] + '/' + q['id']
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


async def get_avatar_from_id(user_id):
    user = await client.fetch_user(user_id)
    return user.avatar


@tree.command(name='convo', description='make a conversation', guild=discord.Object(id=secrets.guild_id))
async def convo(interaction):
    await interaction.response.send_message("wip")
    pass

client.run(secrets.token)
