import discord
import pymongo
import botsecrets

# init discord bot instance
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)


# mongodb connection
mg_client = pymongo.MongoClient(botsecrets.mongo_uri)

"""
TODO:
chain quotes
format quote footer timestamp
display quote videos/embeds

image links but not embeds do not display

maybe
improve the im hi command
"""