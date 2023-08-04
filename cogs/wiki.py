from discord.ext import commands
import wikipedia


class wiki(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    async def wikisearch(self, ctx, query: str):
        result = wikipedia.summary(query)
        await ctx.message.channel.send(result)


async def setup(client):
    await client.add_cog(wiki(client))
