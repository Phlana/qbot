import discord
import pymongo
import botsecrets

# discord bot instance
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)


# mongodb connection
mg_client = pymongo.MongoClient(botsecrets.mongo_uri)
mg_db = mg_client["Vewem"]
mg_quotes = mg_db["quotes"]
