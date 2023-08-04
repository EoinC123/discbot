import os
import asyncio
import json

import discord
from discord.ext import commands

# bot setup (load cogs, set intents and establish command prefix
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = commands.Bot(command_prefix='!', intents=intents)

# Open the config file for token
with open("./config.json") as f:
    configData = json.load(f)


# load cogs from dir ./cogs
async def load():
    for filename in os.listdir("./cogs"):
        if filename == "__pycache__.py":
            continue
        if filename.endswith(".py"):
            await client.load_extension(f'cogs.{filename[:-3]}')
            print(f'cog {filename} has been loaded')


@client.event
async def main():
    await load()
    await client.start(configData["Token"])


asyncio.run(main())
