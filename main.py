import botsecrets
import discord
import bot
import quotes
import misc


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


bot.client.run(botsecrets.token)

if __name__ == '__main__':
    pass
