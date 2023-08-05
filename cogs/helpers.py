from discord.ext import commands
from discord import Message, utils
import asyncio
import random
import settings


class helpers(commands.Cog):
    def __init__(self, client):
        self.client = client

    @classmethod
    def string_to_emoji(cls, string_to_change):
        string_words = string_to_change.split(" ")
        changed = ""
        for word in string_words:
            for char in word:
                changed += settings.REACTIONS.get(char.lower(), "") + " "
            changed += "    "
        return changed

    @classmethod
    async def add_reaction(cls, message: Message, reaction: str) -> None:
        if reaction.lower() in settings.REACTIONS:
            await message.add_reaction(settings.REACTIONS.get(reaction))
        else:
            settings.LOGGER.error(f"Unknown reaction {reaction}")

    @commands.command()
    async def emojify(self, ctx, *message):
        full_message = " ".join(message)
        await ctx.channel.send(helpers.string_to_emoji(full_message))

    @commands.command()
    async def king(self, ctx):
        king_emoji = utils.get(self.client.emojis, name='K_diamonds')
        await ctx.channel.send(f"{king_emoji} for a king")
        await ctx.message.add_reaction(king_emoji)

    @commands.command()
    async def purge(self, ctx, query):
        """
        Cleans up bot's messages. `purge 3` will delete the last 3 messages from channel from which this was invoked
        """
        try:
            num_to_delete = abs(int(query))
            messages = []
            async for message in ctx.channel.history(limit=100, oldest_first=False):
                if message.author.id == self.client.user.id:
                    messages += [message]

            for message in messages:
                if num_to_delete > 0:
                    await message.delete()
                    num_to_delete -= 1
                else:
                    break

        except ValueError as ve:
            await handle_bad_entry(ctx=ctx, exception=ve)

        await asyncio.sleep(2)
        await ctx.message.delete()

    @commands.command()
    async def purge_me(self, ctx, query):
        """
        Cleans up caller's messages. `purge 3` will delete the last 3 messages from channel from which this was invoked
        """
        try:
            num_to_delete = abs(int(query))
            messages = []
            async for message in ctx.channel.history(limit=100, oldest_first=False):
                if message.author.id == ctx.author.id:
                    messages += [message]

            for message in messages:
                if num_to_delete > 0:
                    await message.delete()
                    num_to_delete -= 1
                else:
                    break

        except ValueError as ve:
            await handle_bad_entry(ctx=ctx, exception=ve)
            await ctx.channel.send(f'You need to pass me an integer', delete_after=2)

    @commands.command()
    async def roll(self, ctx, query):
        """
        Random number generator. `roll <int1>-<in2>` will return a random number between <int1> and <in2> inclusive
        """
        try:
            query = query.strip().replace(" ", "")
            limits = query.split("-")

            roll_result = random.randint(int(limits[0]), int(limits[1]))
            await ctx.channel.send(f"{ctx.message.author.mention} rolled {roll_result}")

        except Exception as e:
            await handle_bad_entry(ctx=ctx, exception=e)
            await ctx.channel.send(f'{ctx.message.author.mention} ?', delete_after=20)

    @commands.command()
    async def flip(self, ctx, side=""):
        """
        Flips a coin. Optionally, provide a `side`, and you'll be told if you guessed right or wrong
        """
        coin_options = ["HEADS", "TAILS", "HEAD", "TAIL"]
        coin_result = coin_options[random.randint(0, 1)]
        if side.upper() in coin_options:
            eng_result = "WON" if side.upper() in coin_result else "LOST"
            await ctx.channel.send(f"{ctx.message.author.mention} flipped {coin_result}. You have {eng_result}")
        else:
            await ctx.channel.send(f"{ctx.message.author.mention} flipped {coin_result}")


async def handle_bad_entry(ctx, exception: Exception = None) -> None:
    if exception:
        settings.LOGGER.exception(exception)
    await helpers.add_reaction(message=ctx.message, reaction="wheelchair_sign")
    await helpers.add_reaction(message=ctx.message, reaction="crying_laughing")


def setup(client):
    client.add_cog(helpers(client))
