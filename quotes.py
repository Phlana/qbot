import discord
import botsecrets
import util
import bot


async def embed_quote(q):
    link = 'https://discord.com/channels/' + botsecrets.guild_id + '/' + q['channel_id'] + '/' + q['_id']
    img_link = await util.get_avatar_from_id(int(q['author']['id']))
    colour = await util.get_colour_from_id(int(q['author']['id']))
    embed = discord.Embed(url='https://github.com/Phlana/qbot')
    embed.set_author(name=q['author']['username'], url=link, icon_url=img_link)
    embed.colour = colour
    embed.set_footer(text=q['timestamp'] + '  ' + q['_id'])

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


@bot.tree.command(name='quote', description='post a quote', guild=discord.Object(id=botsecrets.guild_id))
async def quote(interaction: discord.Interaction, user: discord.User = None):
    # user filter is present, filter all quotes down by id
    if user is not None:
        q = next(bot.mg_quotes.aggregate([
            {'$match': {'author.id': str(user.id)}},
            {'$sample': {'size': 1}},
        ]))
    # no filter, use all quotes
    else:
        q = next(bot.mg_quotes.aggregate([
            {'$sample': {'size': 1}},
        ]))

    # build and format embed
    embeds = await embed_quote(q)
    # send message with quote embed
    await interaction.response.send_message(embeds=embeds)


@bot.tree.command(name='get_quote', description='posts a quote by id', guild=discord.Object(id=botsecrets.guild_id))
async def get_quote(interaction: discord.Interaction, quote_id: int):
    q = next(bot.mg_quotes.aggregate([
        {'$match': {'_id': str(quote_id)}},
        {'$sample': {'size': 1}},
    ]))
    embeds = await embed_quote(q)
    await interaction.response.send_message(embeds=embeds)


@bot.tree.command(name='add', description='add a quote', guild=discord.Object(id=botsecrets.guild_id))
async def add(interaction: discord.Interaction, msg_id: int = None, link: str = None):
    if msg_id is None and link is None:
        # add the previous message
        async for m in interaction.channel.history(limit=1):
            message = m
    elif msg_id is not None and link is None:
        # assumes in same channel
        message = await interaction.channel.fetch_message(msg_id)
    elif link is not None and msg_id is None:
        # https://discord.com/channels/162616223719358465/1065114333471838279/1114402350010998864
        parts = link.split('/')
        ch_id = parts[-2]
        msg_id = parts[-1]
        message = await interaction.guild.fetch_channel(ch_id).fetch_message(msg_id)
    else:
        await interaction.response.send_message("failed to add quote")
        return
    await add_quote(interaction, message)


@bot.tree.context_menu(name='add as quote', guild=discord.Object(id=botsecrets.guild_id))
async def context_add(interaction: discord.Interaction, message: discord.Message):
    await add_quote(interaction, message)


async def add_quote(interaction: discord.Interaction, message):
    try:
        row_author = {
            'id': str(message.author.id),
            'username': str(message.author.display_name),
            'avatar': str(message.author.display_avatar.url),
            'discriminator': str(message.author.discriminator),
            'bot': str(message.author.bot),
        }

        row_attachments = []
        for attachment in message.attachments:
            row_attachment = {
                'id': str(attachment.id),
                'url': str(attachment.url),
                'proxy_url': str(attachment.proxy_url),
                'filename': str(attachment.filename),
                'width': str(attachment.width),
                'height': str(attachment.height),
                'size': str(attachment.size),
            }
            row_attachments.append(row_attachment)

        row_embeds = []
        for embed in message.embeds:
            row_embed = {
                'type': str(embed.type,)
            }
            if 'url' in embed:
                row_embed['url'] = str(embed.url)
            if 'title' in embed:
                row_embed['title'] = str(embed.title)
            if 'description' in embed:
                row_embed['description'] = str(embed.description)
            if 'color' in embed:
                row_embed['color'] = str(embed.color)

            row_embeds.append(row_embed)

        timestamp = message.created_at.strftime('%Y-%m-%dT%H:%M:%S.%f%z')
        edited_timestamp = timestamp[:-2] + ':' + timestamp[-2:]

        row = {
            '_id': str(message.id),
            'channel_id': str(message.channel.id),
            'content': str(message.content),
            'timestamp': edited_timestamp,
            'author': row_author,
            'attachments': row_attachments,
            'embeds': row_embeds,
        }

        mg_id = bot.mg_quotes.insert_one(row)
        await interaction.response.send_message(
            'added `' + message.content +
            '` for `' + message.author.display_name +
            '` with id `' + str(mg_id.inserted_id) + '`'
        )
    except:
        await interaction.response.send_message("failed to add message with id " + str(message.id))


@bot.tree.command(name='delete', description='delete a quote', guild=discord.Object(id=botsecrets.guild_id))
async def delete(interaction: discord.Interaction, msg_id: str):
    result = bot.mg_quotes.delete_one({'_id': msg_id})
    if result.deleted_count > 0:
        msg = 'deleted quote with id `' + msg_id + '`'
    else:
        msg = 'failed to delete quote with id `' + msg_id + '`'

    await interaction.response.send_message(msg)


@bot.tree.command(name='convo', description='make a conversation', guild=discord.Object(id=botsecrets.guild_id))
async def convo(interaction: discord.Interaction, num: discord.app_commands.Range[int, 2, 8] = 4):
    # filters out quotes without text contents
    qs = bot.mg_quotes.aggregate([
        {'$match': {'content': {'$exists': True, '$ne': ''}}},
        {'$sample': {'size': num}},
    ])

    conversation = '```\n'

    for q in qs:
        conversation += '**' + q['author']['username'] + '**: '
        conversation += q['content'] + '\n'

    conversation += '```'

    await interaction.response.send_message(conversation)


@bot.tree.command(name='quotes', description='lists existing quotes', guild=discord.Object(id=botsecrets.guild_id))
async def quotes(interaction: discord.Interaction, user: discord.User = None):
    # user filter is present, filter all quotes down by id
    if user is not None:
        qs = bot.mg_quotes.find({'author.id': str(user.id)}, {'_id': 1, 'content': 1, 'author': 1})
    # no filter, use all quotes
    else:
        qs = bot.mg_quotes.find({}, {'_id': 1, 'content': 1, 'author': 1})

    embed = discord.Embed(title='All quotes', url='https://github.com/Phlana/qbot')
    # img_link = await util.get_avatar_from_id(user.id)
    # embed.set_author(name=user.name, icon_url=img_link)

    embed_content = ''
    for q in qs:
        if q['content'] == '':
            content = 'FILE QUOTE'
        else:
            content = q['content']

        embed_content += '**' + str(q['_id']) + ' - ' + q['author']['username'] + ': **\n' \
                         '    ' + content + '\n\n'

    embed.description = embed_content[:4096]

    await interaction.response.send_message(embed=embed)
