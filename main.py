import botsecrets
import discord
import bot
import quotes


@bot.client.event
async def setup_hook():
    await bot.tree.sync()


@bot.client.event
async def on_ready():
    await bot.tree.sync(guild=discord.Object(id=botsecrets.guild_id))
    print(f'We have logged in as {bot.client.user}')


@bot.client.event
async def on_message(message):
    if message.author == bot.client.user:
        return

    if message.content.lower().find('im ') >= 0 and len(message.content) < 25:
        lower_content = message.content.lower()
        index = lower_content.find('im ')
        if index != 0:
            if lower_content[index - 1] == ' ':
                await message.channel.send('hi ' + message.content[index + 3:])
        else:
            await message.channel.send('hi ' + message.content[index + 3:])


@bot.tree.command(name='test', description='dont look\n🙈', guild=discord.Object(id=botsecrets.guild_id))
async def test(interaction):
    async for message in interaction.channel.history(limit=1):
        # print(message)
        link = 'https://discord.com/channels/{}/{}/{}'.format(botsecrets.guild_id, message.channel.id, message.id)
        # print(link)
        print(message.attachments)
        # [{
        #   "id":"971289156930134026",
        #   "url":"https://cdn.discordapp.com/attachments/964377185311940668/971289156930134026/unknown.png",
        #   "proxy_url":"https://media.discordapp.net/attachments/964377185311940668/971289156930134026/unknown.png",
        #   "filename":"unknown.png",
        #   "width":747,
        #   "height":488,
        #   "size":230922
        # }]
        print(message.embeds)
        # [{
        #   "url":"https://www.youtube.com/watch?v=TQcGnEhciNY",
        #   "type":"video",
        #   "title":"Chance the Rapper - I Love My Wife (BONUS TRACK)",
        #   "description":"i made this it's a parody please do not sue\n\ntwitter: www.twitter.com/charliewinsmore\ntwitch: www.twitch.tv/charliewinsmore",
        #   "color":16711680,
        #   "thumbnail":{
        #     "url":"https://i.ytimg.com/vi/TQcGnEhciNY/maxresdefault.jpg",
        #     "proxy_url":"https://images-ext-1.discordapp.net/external/cC0RWlVtyy8aHRaOZ_lwr090ia1jnNJoBiwF33JTk2w/https/i.ytimg.com/vi/TQcGnEhciNY/maxresdefault.jpg",
        #     "width":1280,
        #     "height":720
        #   },
        #   "video":{
        #     "url":"https://www.youtube.com/embed/TQcGnEhciNY",
        #     "width":1280,
        #     "height":720
        #   },
        #   "provider":{
        #     "url":"https://www.youtube.com",
        #     "name":"YouTube"
        #   },
        #   "author":{
        #     "url":"https://www.youtube.com/channel/UCweqeK26PLExyiHjHmujFjw",
        #     "name":"charliewinsmore"
        #   }
        # }]

        row_author = {
            'id': message.author.id,
            'username': message.author.display_name,
            'avatar': message.author.display_avatar,
            'discriminator': message.author.discriminator,
            'bot': message.author.bot,
        }

        row_attachments = []
        for attachment in message.attachments:
            row_attachment = {
                'id': attachment.id,
                'url': attachment.url,
                'proxy_url': attachment.proxy_url,
                'filename': attachment.filename,
                'width': attachment.width,
                'height': attachment.height,
                'size': attachment.size,
            }
            row_attachments.append(row_attachment)

        row_embeds = []
        for embed in message.embeds:
            row_embed = {
                'url': embed.url,
                'type': embed.type,
                'title': embed.title,
                'description': embed.description,
                'color': embed.color,
            }
            row_embeds.append(row_embed)

        timestamp = message.created_at.strftime('%Y-%m-%dT%H:%M:%S.%f%z')
        edited_timestamp = timestamp[:-2] + ':' + timestamp[-2:]

        row = {
            'id': message.id,
            'channel_id': message.channel.id,
            'content': message.content,
            'timestamp': edited_timestamp,
            'author': row_author,
            'attachments': row_attachments,
            'embeds': row_embeds,
        }
        print(row)

    pass
# https://discord.com/channels/162616223719358465/1065114333471838279/1091595353637257216


bot.client.run(botsecrets.token)

if __name__ == '__main__':
    pass
