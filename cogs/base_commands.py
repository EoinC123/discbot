from discord.ext import commands


class base_commands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Square Bot Online")

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Latency is currently {round(self.client.latency * 1000)}ms')

    @commands.command()
    async def riddle(self, ctx):
        await ctx.send('no')


async def setup(client):
    await client.add_cog(base_commands(client))
