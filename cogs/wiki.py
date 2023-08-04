import discord
from discord.ext import commands
import wikipedia


class wiki(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def getwikipage(self, ctx, query):
        result = wikipedia.summary(query)
        await ctx.channel.send(result)
