import botsecrets
import discord
import bot
import quotes
import misc
import cat
import gp
import random
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(filename='qbot.log', level=logging.INFO)

tiny_text = {
    "a": "ᴀ",
    "b": "ʙ",
    "c": "ᴄ",
    "d": "ᴅ",
    "e": "ᴇ",
    "f": "ғ",
    "g": "ɢ",
    "h": "ʜ",
    "i": "ɪ",
    "j": "ᴊ",
    "k": "ᴋ",
    "l": "ʟ",
    "m": "ᴍ",
    "n": "ɴ",
    "o": "ᴏ",
    "p": "ᴘ",
    "q": "ǫ",
    "r": "ʀ",
    "s": "s",
    "t": "ᴛ",
    "u": "ᴜ",
    "v": "ᴠ",
    "w": "ᴡ",
    "x": "x",
    "y": "ʏ",
    "z": "ᴢ",
}


@bot.client.event
async def setup_hook():
    await bot.tree.sync()
    await bot.tree.sync(guild=discord.Object(id=botsecrets.guild_id))


@bot.client.event
async def on_ready():
    print(f'logged in as {bot.client.user}')


@bot.client.event
async def on_message(message):
    if message.author == bot.client.user:
        return

    lower_content = message.content.lower()
    upper_content = message.content.upper()

    # DashieGames that fucking bird that i hate
    if len(message.content) <= 40 and random.random() < 0.0005:
        if message.content:
            small_msg = "".join(map(lambda a: tiny_text[a] if a in tiny_text.keys() else a, lower_content))
            big_msg = "**" + upper_content + "**"
            bird_msg = small_msg + "\n" + small_msg + "\n" + big_msg
            await message.channel.send(bird_msg)
            return

    # you are a father
    if lower_content.find('im ') >= 0 and len(message.content) < 25:
        index = lower_content.find('im ')
        if index == 0 or lower_content[index - 1] == ' ':
            hi_msg = 'hi ' + message.content[index + 3:]
            await message.channel.send(hi_msg)


bot.client.run(botsecrets.token)

if __name__ == '__main__':
    pass
