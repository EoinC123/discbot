from discord.ext import commands
import requests
import json


class riddle(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def riddle(self, ctx):
        riddle_obj = requests.get('https://riddles-api.vercel.app/random')
        json_riddle_obj = riddle_obj.json()
        await ctx.send(json_riddle_obj["riddle"])
        await ctx.user.send(json_riddle_obj["anwser"])


async def setup(client):
    await client.add_cog(riddle(client))
