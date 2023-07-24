import discord
from discord.ext import commands
import configparser


intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix='!', intents=intents)


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        await message.channel.send('Hello!')


client.run("MTEzMzE3NTI4OTk3NTkzOTE4Mw.G3KBQB.RMs1WYTmdYqAi9MExHbxp0qE6-yp9Pjm7lQ95o")
